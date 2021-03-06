# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/visuals/text/text.py
# Compiled at: 2016-11-03 01:40:19
from __future__ import division
import numpy as np
from copy import deepcopy
import sys
from ._sdf import SDFRenderer
from ...gloo import TextureAtlas, IndexBuffer, VertexBuffer
from ...gloo import context
from ...gloo.wrappers import _check_valid
from ...ext.six import string_types
from ...util.fonts import _load_glyph
from ..transforms import STTransform
from ...color import Color
from ..visual import Visual
from ...io import load_spatial_filters

class TextureFont(object):
    """Gather a set of glyphs relative to a given font name and size

    Parameters
    ----------
    font : dict
        Dict with entries "face", "size", "bold", "italic".
    renderer : instance of SDFRenderer
        SDF renderer to use.
    """

    def __init__(self, font, renderer):
        self._atlas = TextureAtlas()
        self._atlas.wrapping = 'clamp_to_edge'
        self._kernel, _ = load_spatial_filters()
        self._renderer = renderer
        self._font = deepcopy(font)
        self._font['size'] = 256
        self._lowres_size = 64
        assert self._font['size'] % self._lowres_size == 0
        self._spread = 32
        assert self._spread % self.ratio == 0
        self._glyphs = {}

    @property
    def ratio(self):
        """Ratio of the initial high-res to final stored low-res glyph"""
        return self._font['size'] // self._lowres_size

    @property
    def slop(self):
        """Extra space along each glyph edge due to SDF borders"""
        return self._spread // self.ratio

    def __getitem__(self, char):
        if not (isinstance(char, string_types) and len(char) == 1):
            raise TypeError('index must be a 1-character string')
        if char not in self._glyphs:
            self._load_char(char)
        return self._glyphs[char]

    def _load_char(self, char):
        """Build and store a glyph corresponding to an individual character

        Parameters
        ----------
        char : str
            A single character to be represented.
        """
        assert isinstance(char, string_types) and len(char) == 1
        assert char not in self._glyphs
        _load_glyph(self._font, char, self._glyphs)
        glyph = self._glyphs[char]
        bitmap = glyph['bitmap']
        data = np.zeros((bitmap.shape[0] + 2 * self._spread,
         bitmap.shape[1] + 2 * self._spread), np.uint8)
        data[self._spread:-self._spread, self._spread:-self._spread] = bitmap
        height = data.shape[0] // self.ratio
        width = data.shape[1] // self.ratio
        region = self._atlas.get_free_region(width + 2, height + 2)
        if region is None:
            raise RuntimeError('Cannot store glyph')
        x, y, w, h = region
        x, y, w, h = (x + 1, y + 1, w - 2, h - 2)
        self._renderer.render_to_texture(data, self._atlas, (x, y), (w, h))
        u0 = x / float(self._atlas.shape[1])
        v0 = y / float(self._atlas.shape[0])
        u1 = (x + w) / float(self._atlas.shape[1])
        v1 = (y + h) / float(self._atlas.shape[0])
        texcoords = (u0, v0, u1, v1)
        glyph.update(dict(size=(w, h), texcoords=texcoords))
        return


class FontManager(object):
    """Helper to create TextureFont instances and reuse them when possible"""

    def __init__(self):
        self._fonts = {}
        self._renderer = SDFRenderer()

    def get_font(self, face, bold=False, italic=False):
        """Get a font described by face and size"""
        key = '%s-%s-%s' % (face, bold, italic)
        if key not in self._fonts:
            font = dict(face=face, bold=bold, italic=italic)
            self._fonts[key] = TextureFont(font, self._renderer)
        return self._fonts[key]


def _text_to_vbo(text, font, anchor_x, anchor_y, lowres_size):
    """Convert text characters to VBO"""
    canvas = context.get_current_canvas()
    canvas.context.flush_commands()
    text_vtype = np.dtype([('a_position', np.float32, 2),
     (
      'a_texcoord', np.float32, 2)])
    vertices = np.zeros(len(text) * 4, dtype=text_vtype)
    prev = None
    width = height = ascender = descender = 0
    ratio, slop = 1.0 / font.ratio, font.slop
    x_off = -slop
    if sys.version[0] == '2' and isinstance(text, str):
        text = text.decode('utf-8')
    orig_viewport = canvas.context.get_viewport()
    for ii, char in enumerate(text):
        glyph = font[char]
        kerning = glyph['kerning'].get(prev, 0.0) * ratio
        x0 = x_off + glyph['offset'][0] * ratio + kerning
        y0 = glyph['offset'][1] * ratio + slop
        x1 = x0 + glyph['size'][0]
        y1 = y0 - glyph['size'][1]
        u0, v0, u1, v1 = glyph['texcoords']
        position = [[x0, y0], [x0, y1], [x1, y1], [x1, y0]]
        texcoords = [[u0, v0], [u0, v1], [u1, v1], [u1, v0]]
        vi = ii * 4
        vertices['a_position'][vi:(vi + 4)] = position
        vertices['a_texcoord'][vi:(vi + 4)] = texcoords
        x_move = glyph['advance'] * ratio + kerning
        x_off += x_move
        ascender = max(ascender, y0 - slop)
        descender = min(descender, y1 + slop)
        width += x_move
        height = max(height, glyph['size'][1] - 2 * slop)
        prev = char

    for char in 'hy':
        glyph = font[char]
        y0 = glyph['offset'][1] * ratio + slop
        y1 = y0 - glyph['size'][1]
        ascender = max(ascender, y0 - slop)
        descender = min(descender, y1 + slop)
        height = max(height, glyph['size'][1] - 2 * slop)

    if orig_viewport is not None:
        canvas.context.set_viewport(*orig_viewport)
    width -= glyph['advance'] * ratio - (glyph['size'][0] - 2 * slop)
    dx = dy = 0
    if anchor_y == 'top':
        dy = -ascender
    elif anchor_y in ('center', 'middle'):
        dy = -(height / 2 + descender)
    elif anchor_y == 'bottom':
        dy = -descender
    if anchor_x == 'right':
        dx = -width
    elif anchor_x == 'center':
        dx = -width / 2.0
    vertices['a_position'] += (dx, dy)
    vertices['a_position'] /= lowres_size
    return vertices


class TextVisual(Visual):
    """Visual that displays text

    Parameters
    ----------
    text : str | list of str
        Text to display. Can also be a list of strings.
        Note: support for list of str might be removed soon
        in favor of text collections.
    color : instance of Color
        Color to use.
    bold : bool
        Bold face.
    italic : bool
        Italic face.
    face : str
        Font face to use.
    font_size : float
        Point size to use.
    pos : tuple | list of tuple
        Position (x, y) or (x, y, z) of the text.
        Can also be a list of tuple if `text` is a list.
    rotation : float
        Rotation (in degrees) of the text clockwise.
    anchor_x : str
        Horizontal text anchor.
    anchor_y : str
        Vertical text anchor.
    font_manager : object | None
        Font manager to use (can be shared if the GLContext is shared).
    """
    VERTEX_SHADER = '\n        uniform float u_rotation;  // rotation in rad\n        attribute vec2 a_position; // in point units\n        attribute vec2 a_texcoord;\n        attribute vec3 a_pos;  // anchor position\n        varying vec2 v_texcoord;\n\n        void main(void) {\n            // Eventually "rot" should be handled by SRTTransform or so...\n            mat4 rot = mat4(cos(u_rotation), -sin(u_rotation), 0, 0,\n                            sin(u_rotation), cos(u_rotation), 0, 0,\n                            0, 0, 1, 0, 0, 0, 0, 1);\n            vec4 pos = $transform(vec4(a_pos, 1.0)) +\n                       $text_scale(rot * vec4(a_position, 0, 0));\n            gl_Position = pos;\n            v_texcoord = a_texcoord;\n        }\n        '
    FRAGMENT_SHADER = '\n        #include "misc/spatial-filters.frag"\n        // Adapted from glumpy with permission\n        const float M_SQRT1_2 = 0.707106781186547524400844362104849039;\n\n        uniform sampler2D u_font_atlas;\n        uniform vec2 u_font_atlas_shape;\n        uniform vec4 u_color;\n        uniform float u_npix;\n\n        varying vec2 v_texcoord;\n        const float center = 0.5;\n\n        float contour(in float d, in float w)\n        {\n            return smoothstep(center - w, center + w, d);\n        }\n\n        float sample(sampler2D texture, vec2 uv, float w)\n        {\n            return contour(texture2D(texture, uv).r, w);\n        }\n\n        void main(void) {\n            vec4 color = u_color;\n            vec2 uv = v_texcoord.xy;\n            vec4 rgb;\n\n            // Use interpolation at high font sizes\n            if(u_npix >= 50.0)\n                rgb = CatRom(u_font_atlas, u_font_atlas_shape, uv);\n            else\n                rgb = texture2D(u_font_atlas, uv);\n            float distance = rgb.r;\n\n            // GLSL\'s fwidth = abs(dFdx(uv)) + abs(dFdy(uv))\n            float width = 0.5 * fwidth(distance);  // sharpens a bit\n\n            // Regular SDF\n            float alpha = contour(distance, width);\n\n            if (u_npix < 30.) {\n                // Supersample, 4 extra points\n                // Half of 1/sqrt2; you can play with this\n                float dscale = 0.5 * M_SQRT1_2;\n                vec2 duv = dscale * (dFdx(v_texcoord) + dFdy(v_texcoord));\n                vec4 box = vec4(v_texcoord-duv, v_texcoord+duv);\n                float asum = sample(u_font_atlas, box.xy, width)\n                           + sample(u_font_atlas, box.zw, width)\n                           + sample(u_font_atlas, box.xw, width)\n                           + sample(u_font_atlas, box.zy, width);\n                // weighted average, with 4 extra points having 0.5 weight\n                // each, so 1 + 0.5*4 = 3 is the divisor\n                alpha = (alpha + 0.5 * asum) / 3.0;\n            }\n\n            gl_FragColor = vec4(color.rgb, color.a * alpha);\n        }\n        '

    def __init__(self, text=None, color='black', bold=False, italic=False, face='OpenSans', font_size=12, pos=[0, 0, 0], rotation=0.0, anchor_x='center', anchor_y='center', font_manager=None):
        Visual.__init__(self, vcode=self.VERTEX_SHADER, fcode=self.FRAGMENT_SHADER)
        valid_keys = ('top', 'center', 'middle', 'baseline', 'bottom')
        _check_valid('anchor_y', anchor_y, valid_keys)
        valid_keys = ('left', 'center', 'right')
        _check_valid('anchor_x', anchor_x, valid_keys)
        self._font_manager = font_manager or FontManager()
        self._font = self._font_manager.get_font(face, bold, italic)
        self._vertices = None
        self._anchors = (anchor_x, anchor_y)
        self.color = color
        self.text = text
        self.font_size = font_size
        self.pos = pos
        self.rotation = rotation
        self._text_scale = STTransform()
        self._draw_mode = 'triangles'
        self.set_gl_state(blend=True, depth_test=False, cull_face=False, blend_func=('src_alpha',
                                                                                     'one_minus_src_alpha'))
        self.freeze()
        return

    @property
    def text(self):
        """The text string"""
        return self._text

    @text.setter
    def text(self, text):
        assert isinstance(text, list) and all(isinstance(t, string_types) for t in text)
        if text is None:
            text = []
        self._text = text
        self._vertices = None
        self._pos_changed = True
        self.update()
        return

    @property
    def anchors(self):
        return self._anchors

    @anchors.setter
    def anchors(self, a):
        self._anchors = a
        self._vertices = None
        self._pos_changed = True
        self.update()
        return

    @property
    def font_size(self):
        """ The font size (in points) of the text
        """
        return self._font_size

    @font_size.setter
    def font_size(self, size):
        self._font_size = max(0.0, float(size))
        self.update()

    @property
    def color(self):
        """ The color of the text
        """
        return self._color

    @color.setter
    def color(self, color):
        self._color = Color(color)
        self.update()

    @property
    def rotation(self):
        """ The rotation of the text (clockwise, in degrees)
        """
        return self._rotation * 180.0 / np.pi

    @rotation.setter
    def rotation(self, rotation):
        self._rotation = float(rotation) * np.pi / 180.0
        self.update()

    @property
    def pos(self):
        """ The position of the text anchor in the local coordinate frame
        """
        return self._pos

    @pos.setter
    def pos(self, pos):
        pos = np.atleast_2d(pos).astype(np.float32)
        if pos.shape[1] == 2:
            pos = np.concatenate((pos,
             np.zeros((pos.shape[0], 1), np.float32)), axis=1)
        elif pos.shape[1] != 3:
            raise ValueError('pos must have 2 or 3 elements')
        elif pos.shape[0] == 0:
            raise ValueError('at least one position must be given')
        self._pos = pos
        self._pos_changed = True
        self.update()

    def _prepare_draw(self, view):
        if len(self.text) == 0:
            return False
        else:
            if self._vertices is None:
                text = self.text
                if isinstance(text, string_types):
                    text = [
                     text]
                n_char = sum(len(t) for t in text)
                self._vertices = np.concatenate([ _text_to_vbo(t, self._font, self._anchors[0], self._anchors[1], self._font._lowres_size) for t in text
                                                ])
                self._vertices = VertexBuffer(self._vertices)
                idx = np.array([0, 1, 2, 0, 2, 3], np.uint32) + np.arange(0, 4 * n_char, 4, dtype=np.uint32)[:, np.newaxis]
                self._index_buffer = IndexBuffer(idx.ravel())
                self.shared_program.bind(self._vertices)
                self._configure_gl_state()
            if self._pos_changed:
                text = self.text
                repeats = isinstance(text, string_types) or [ 4 * len(t) for t in text ]
                text = ('').join(text)
            else:
                repeats = [
                 4 * len(text)]
            n_text = len(repeats)
            pos = self.pos
            if pos.shape[0] < n_text:
                pos = np.repeat(pos, [1] * (len(pos) - 1) + [n_text - len(pos) + 1], axis=0)
            pos = np.repeat(pos[:n_text], repeats, axis=0)
            if not pos.shape[0] == self._vertices.size:
                raise AssertionError
                self.shared_program['a_pos'] = pos
                self._pos_changed = False
            transforms = self.transforms
            n_pix = self._font_size / 72.0 * transforms.dpi
            tr = transforms.get_transform('document', 'render')
            px_scale = (tr.map((1, 0)) - tr.map((0, 1)))[:2]
            self._text_scale.scale = px_scale * n_pix
            self.shared_program.vert['text_scale'] = self._text_scale
            self.shared_program['u_npix'] = n_pix
            self.shared_program['u_kernel'] = self._font._kernel
            self.shared_program['u_rotation'] = self._rotation
            self.shared_program['u_color'] = self._color.rgba
            self.shared_program['u_font_atlas'] = self._font._atlas
            self.shared_program['u_font_atlas_shape'] = self._font._atlas.shape[:2]
            return

    def _prepare_transforms(self, view):
        self._pos_changed = True
        tr = view.transforms.get_transform()
        view.view_program.vert['transform'] = tr

    def _compute_bounds(self, axis, view):
        return (
         self._pos[:, axis].min(), self._pos[:, axis].max())