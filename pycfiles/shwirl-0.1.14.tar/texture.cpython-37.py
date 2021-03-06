# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/gloo/texture.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 33257 bytes
import math, numpy as np, warnings
from .globject import GLObject
from ext.six import string_types
from .util import check_enum

class BaseTexture(GLObject):
    __doc__ = "\n    A Texture is used to represent a topological set of scalar values.\n\n    Parameters\n    ----------\n    data : ndarray | tuple | None\n        Texture data in the form of a numpy array (or something that\n        can be turned into one). A tuple with the shape of the texture\n        can also be given.\n    format : str | enum | None\n        The format of the texture: 'luminance', 'alpha',\n        'luminance_alpha', 'rgb', or 'rgba'. If not given the format\n        is chosen automatically based on the number of channels.\n        When the data has one channel, 'luminance' is assumed.\n    resizable : bool\n        Indicates whether texture can be resized. Default True.\n    interpolation : str | None\n        Interpolation mode, must be one of: 'nearest', 'linear'.\n        Default 'nearest'.\n    wrapping : str | None\n        Wrapping mode, must be one of: 'repeat', 'clamp_to_edge',\n        'mirrored_repeat'. Default 'clamp_to_edge'.\n    shape : tuple | None\n        Optional. A tuple with the shape of the texture. If ``data``\n        is also a tuple, it will override the value of ``shape``.\n    internalformat : str | None\n        Internal format to use.\n    resizeable : None\n        Deprecated version of `resizable`.\n    "
    _ndim = 2
    _formats = {1:'luminance', 
     2:'luminance_alpha', 
     3:'rgb', 
     4:'rgba'}
    _inv_formats = {'luminance':1, 
     'alpha':1, 
     'red':1, 
     'luminance_alpha':2, 
     'rg':2, 
     'rgb':3, 
     'rgba':4}
    _inv_internalformats = dict([(base + suffix, channels) for base, channels in (('r', 1),
                                                                                  ('rg', 2),
                                                                                  ('rgb', 3),
                                                                                  ('rgba', 4)) for suffix in ('8',
                                                                                                              '16',
                                                                                                              '16f',
                                                                                                              '32f')] + [
     ('luminance', 1),
     ('alpha', 1),
     ('red', 1),
     ('luminance_alpha', 2),
     ('rg', 2),
     ('rgb', 3),
     ('rgba', 4)])

    def __init__(self, data=None, format=None, resizable=True, interpolation=None, wrapping=None, shape=None, internalformat=None, resizeable=None):
        GLObject.__init__(self)
        if resizeable is not None:
            resizable = resizeable
            warnings.warn('resizeable has been deprecated in favor of resizable and will be removed next release', DeprecationWarning)
        else:
            self._resizable = True
            self._shape = tuple([0 for i in range(self._ndim + 1)])
            self._format = format
            self._internalformat = internalformat
            self.interpolation = interpolation or 'nearest'
            self.wrapping = wrapping or 'clamp_to_edge'
            if isinstance(data, tuple):
                shape, data = data, None
            elif data is not None:
                if shape is not None:
                    raise ValueError('Texture needs data or shape, not both.')
                data = np.array(data, copy=False)
                self._resize(data.shape, format, internalformat)
                self._set_data(data)
            else:
                if shape is not None:
                    self._resize(shape, format, internalformat)
                else:
                    raise ValueError('Either data or shape must be given')
        self._resizable = bool(resizable)

    def _normalize_shape(self, data_or_shape):
        if isinstance(data_or_shape, np.ndarray):
            data = data_or_shape
            shape = data.shape
        else:
            assert isinstance(data_or_shape, tuple)
            data = None
            shape = data_or_shape
        if shape:
            if len(shape) < self._ndim:
                raise ValueError('Too few dimensions for texture')
            else:
                if len(shape) > self._ndim + 1:
                    raise ValueError('Too many dimensions for texture')
                else:
                    if len(shape) == self._ndim:
                        shape = shape + (1, )
                    else:
                        if shape[(-1)] > 4:
                            raise ValueError('Too many channels for texture')
        if data is not None:
            return data.reshape(shape)
        return shape

    @property
    def shape(self):
        """ Data shape (last dimension indicates number of color channels)
        """
        return self._shape

    @property
    def format(self):
        """ The texture format (color channels).
        """
        return self._format

    @property
    def wrapping(self):
        """ Texture wrapping mode """
        value = self._wrapping
        if all([v == value[0] for v in value]):
            return value[0]
        return value

    @wrapping.setter
    def wrapping(self, value):
        if isinstance(value, int) or isinstance(value, string_types):
            value = (
             value,) * self._ndim
        else:
            if isinstance(value, (tuple, list)):
                if len(value) != self._ndim:
                    raise ValueError('Texture wrapping needs 1 or %i values' % self._ndim)
            else:
                raise ValueError('Invalid value for wrapping: %r' % value)
        valid = ('repeat', 'clamp_to_edge', 'mirrored_repeat')
        value = tuple([check_enum(value[i], 'tex wrapping', valid) for i in range(self._ndim)])
        self._wrapping = value
        self._glir.command('WRAPPING', self._id, value)

    @property
    def interpolation(self):
        """ Texture interpolation for minification and magnification. """
        value = self._interpolation
        if value[0] == value[1]:
            return value[0]
        return value

    @interpolation.setter
    def interpolation(self, value):
        if isinstance(value, int) or isinstance(value, string_types):
            value = (
             value,) * 2
        else:
            if isinstance(value, (tuple, list)):
                if len(value) != 2:
                    raise ValueError('Texture interpolation needs 1 or 2 values')
            else:
                raise ValueError('Invalid value for interpolation: %r' % value)
        valid = ('nearest', 'linear')
        value = (check_enum(value[0], 'tex interpolation', valid),
         check_enum(value[1], 'tex interpolation', valid))
        self._interpolation = value
        (self._glir.command)('INTERPOLATION', self._id, *value)

    def resize(self, shape, format=None, internalformat=None):
        """Set the texture size and format

        Parameters
        ----------
        shape : tuple of integers
            New texture shape in zyx order. Optionally, an extra dimention
            may be specified to indicate the number of color channels.
        format : str | enum | None
            The format of the texture: 'luminance', 'alpha',
            'luminance_alpha', 'rgb', or 'rgba'. If not given the format
            is chosen automatically based on the number of channels.
            When the data has one channel, 'luminance' is assumed.
        internalformat : str | enum | None
            The internal (storage) format of the texture: 'luminance',
            'alpha', 'r8', 'r16', 'r16f', 'r32f'; 'luminance_alpha',
            'rg8', 'rg16', 'rg16f', 'rg32f'; 'rgb', 'rgb8', 'rgb16',
            'rgb16f', 'rgb32f'; 'rgba', 'rgba8', 'rgba16', 'rgba16f',
            'rgba32f'.  If None, the internalformat is chosen
            automatically based on the number of channels.  This is a
            hint which may be ignored by the OpenGL implementation.
        """
        return self._resize(shape, format, internalformat)

    def _resize(self, shape, format=None, internalformat=None):
        """Internal method for resize.
        """
        shape = self._normalize_shape(shape)
        if not self._resizable:
            raise RuntimeError('Texture is not resizable')
        elif format is None:
            format = self._formats[shape[(-1)]]
            if self._format:
                if self._inv_formats[self._format] == self._inv_formats[format]:
                    format = self._format
                else:
                    format = check_enum(format)
            if internalformat is None:
                if self._internalformat and self._inv_internalformats[self._internalformat] == shape[(-1)]:
                    internalformat = self._internalformat
        else:
            internalformat = check_enum(internalformat)
        if format not in self._inv_formats:
            raise ValueError('Invalid texture format: %r.' % format)
        else:
            if shape[(-1)] != self._inv_formats[format]:
                raise ValueError('Format does not match with given shape. (format expects %d elements, data has %d)' % (
                 self._inv_formats[format], shape[(-1)]))
            elif internalformat is None:
                pass
            elif internalformat not in self._inv_internalformats:
                raise ValueError('Invalid texture internalformat: %r. Allowed formats: %r' % (
                 internalformat, self._inv_internalformats))
            else:
                if shape[(-1)] != self._inv_internalformats[internalformat]:
                    raise ValueError('Internalformat does not match with given shape.')
            self._shape = shape
            self._format = format
            self._internalformat = internalformat
            self._glir.command('SIZE', self._id, self._shape, self._format, self._internalformat)

    def set_data(self, data, offset=None, copy=False):
        """Set texture data

        Parameters
        ----------
        data : ndarray
            Data to be uploaded
        offset: int | tuple of ints
            Offset in texture where to start copying data
        copy: bool
            Since the operation is deferred, data may change before
            data is actually uploaded to GPU memory. Asking explicitly
            for a copy will prevent this behavior.

        Notes
        -----
        This operation implicitely resizes the texture to the shape of
        the data if given offset is None.
        """
        return self._set_data(data, offset, copy)

    def _set_data(self, data, offset=None, copy=False):
        """Internal method for set_data.
        """
        data = np.array(data, copy=copy)
        data = self._normalize_shape(data)
        if offset is None:
            self._resize(data.shape)
        else:
            if all([i == 0 for i in offset]):
                if data.shape == self._shape:
                    self._resize(data.shape)
        offset = offset or tuple([0 for i in range(self._ndim)])
        assert len(offset) == self._ndim
        for i in range(len(data.shape) - 1):
            if offset[i] + data.shape[i] > self._shape[i]:
                raise ValueError('Data is too large')

        self._glir.command('DATA', self._id, offset, data)

    def __setitem__(self, key, data):
        """ x.__getitem__(y) <==> x[y] """
        if isinstance(key, (int, slice)) or key == Ellipsis:
            key = (
             key,)
        else:
            shape = self._shape
            slices = [slice(0, shape[i]) for i in range(len(shape))]
            keys = key[::1]
            dims = range(0, len(key))
            if key[0] == Ellipsis:
                keys = key[::-1]
                dims = range(len(self._shape) - 1, len(self._shape) - 1 - len(keys), -1)
            for k, dim in zip(keys, dims):
                size = self._shape[dim]
                if isinstance(k, int):
                    if k < 0:
                        k += size
                    if k < 0 or k > size:
                        raise IndexError('Texture assignment index out of range')
                    start, stop = k, k + 1
                    slices[dim] = slice(start, stop, 1)
                elif isinstance(k, slice):
                    start, stop, step = k.indices(size)
                    if step != 1:
                        raise IndexError('Cannot access non-contiguous data')
                    if stop < start:
                        start, stop = stop, start
                    slices[dim] = slice(start, stop, step)
                else:
                    if k == Ellipsis:
                        continue
                    raise TypeError('Texture indices must be integers')

            offset = tuple([s.start for s in slices])[:self._ndim]
            shape = tuple([s.stop - s.start for s in slices])
            size = np.prod(shape) if len(shape) > 0 else 1
            data = isinstance(data, np.ndarray) or np.array(data, copy=False)
        if data.shape != shape:
            data = np.resize(data, shape)
        self._set_data(data=data, offset=offset, copy=False)

    def __repr__(self):
        return '<%s shape=%r format=%r at 0x%x>' % (
         self.__class__.__name__, self._shape, self._format, id(self))


class Texture1D(BaseTexture):
    __doc__ = " One dimensional texture\n\n    Parameters\n    ----------\n    data : ndarray | tuple | None\n        Texture data in the form of a numpy array (or something that\n        can be turned into one). A tuple with the shape of the texture\n        can also be given.\n    format : str | enum | None\n        The format of the texture: 'luminance', 'alpha',\n        'luminance_alpha', 'rgb', or 'rgba'. If not given the format\n        is chosen automatically based on the number of channels.\n        When the data has one channel, 'luminance' is assumed.\n    resizable : bool\n        Indicates whether texture can be resized. Default True.\n    interpolation : str | None\n        Interpolation mode, must be one of: 'nearest', 'linear'.\n        Default 'nearest'.\n    wrapping : str | None\n        Wrapping mode, must be one of: 'repeat', 'clamp_to_edge',\n        'mirrored_repeat'. Default 'clamp_to_edge'.\n    shape : tuple | None\n        Optional. A tuple with the shape of the texture. If ``data``\n        is also a tuple, it will override the value of ``shape``.\n    internalformat : str | None\n        Internal format to use.\n    resizeable : None\n        Deprecated version of `resizable`.\n    "
    _ndim = 1
    _GLIR_TYPE = 'Texture1D'

    def __init__(self, data=None, format=None, resizable=True, interpolation=None, wrapping=None, shape=None, internalformat=None, resizeable=None):
        BaseTexture.__init__(self, data, format, resizable, interpolation, wrapping, shape, internalformat, resizeable)

    @property
    def width(self):
        """ Texture width """
        return self._shape[0]

    @property
    def glsl_type(self):
        """ GLSL declaration strings required for a variable to hold this data.
        """
        return ('uniform', 'sampler1D')

    @property
    def glsl_sampler_type(self):
        """ GLSL type of the sampler.
        """
        return 'sampler1D'

    @property
    def glsl_sample(self):
        """ GLSL function that samples the texture.
        """
        return 'texture1D'


class Texture2D(BaseTexture):
    __doc__ = " Two dimensional texture\n\n    Parameters\n    ----------\n    data : ndarray\n        Texture data shaped as W, or a tuple with the shape for\n        the texture (W).\n    format : str | enum | None\n        The format of the texture: 'luminance', 'alpha',\n        'luminance_alpha', 'rgb', or 'rgba'. If not given the format\n        is chosen automatically based on the number of channels.\n        When the data has one channel, 'luminance' is assumed.\n    resizable : bool\n        Indicates whether texture can be resized. Default True.\n    interpolation : str\n        Interpolation mode, must be one of: 'nearest', 'linear'.\n        Default 'nearest'.\n    wrapping : str\n        Wrapping mode, must be one of: 'repeat', 'clamp_to_edge',\n        'mirrored_repeat'. Default 'clamp_to_edge'.\n    shape : tuple\n        Optional. A tuple with the shape HxW. If ``data``\n        is also a tuple, it will override the value of ``shape``.\n    internalformat : str | None\n        Internal format to use.\n    resizeable : None\n        Deprecated version of `resizable`.\n    "
    _ndim = 2
    _GLIR_TYPE = 'Texture2D'

    def __init__(self, data=None, format=None, resizable=True, interpolation=None, wrapping=None, shape=None, internalformat=None, resizeable=None):
        BaseTexture.__init__(self, data, format, resizable, interpolation, wrapping, shape, internalformat, resizeable)

    @property
    def height(self):
        """ Texture height """
        return self._shape[0]

    @property
    def width(self):
        """ Texture width """
        return self._shape[1]

    @property
    def glsl_type(self):
        """ GLSL declaration strings required for a variable to hold this data.
        """
        return ('uniform', 'sampler2D')

    @property
    def glsl_sampler_type(self):
        """ GLSL type of the sampler.
        """
        return 'sampler2D'

    @property
    def glsl_sample(self):
        """ GLSL function that samples the texture.
        """
        return 'texture2D'


class Texture3D(BaseTexture):
    __doc__ = " Three dimensional texture\n\n    Parameters\n    ----------\n    data : ndarray | tuple | None\n        Texture data in the form of a numpy array (or something that\n        can be turned into one). A tuple with the shape of the texture\n        can also be given.\n    format : str | enum | None\n        The format of the texture: 'luminance', 'alpha',\n        'luminance_alpha', 'rgb', or 'rgba'. If not given the format\n        is chosen automatically based on the number of channels.\n        When the data has one channel, 'luminance' is assumed.\n    resizable : bool\n        Indicates whether texture can be resized. Default True.\n    interpolation : str | None\n        Interpolation mode, must be one of: 'nearest', 'linear'.\n        Default 'nearest'.\n    wrapping : str | None\n        Wrapping mode, must be one of: 'repeat', 'clamp_to_edge',\n        'mirrored_repeat'. Default 'clamp_to_edge'.\n    shape : tuple | None\n        Optional. A tuple with the shape of the texture. If ``data``\n        is also a tuple, it will override the value of ``shape``.\n    internalformat : str | None\n        Internal format to use.\n    resizeable : None\n        Deprecated version of `resizable`.\n    "
    _ndim = 3
    _GLIR_TYPE = 'Texture3D'

    def __init__(self, data=None, format=None, resizable=True, interpolation=None, wrapping=None, shape=None, internalformat=None, resizeable=None):
        BaseTexture.__init__(self, data, format, resizable, interpolation, wrapping, shape, internalformat, resizeable)

    @property
    def width(self):
        """ Texture width """
        return self._shape[2]

    @property
    def height(self):
        """ Texture height """
        return self._shape[1]

    @property
    def depth(self):
        """ Texture depth """
        return self._shape[0]

    @property
    def glsl_type(self):
        """ GLSL declaration strings required for a variable to hold this data.
        """
        return ('uniform', 'sampler3D')

    @property
    def glsl_sampler_type(self):
        """ GLSL type of the sampler.
        """
        return 'sampler3D'

    @property
    def glsl_sample(self):
        """ GLSL function that samples the texture.
        """
        return 'texture3D'


class TextureEmulated3D(Texture2D):
    __doc__ = " Two dimensional texture that is emulating a three dimensional texture\n\n    Parameters\n    ----------\n    data : ndarray | tuple | None\n        Texture data in the form of a numpy array (or something that\n        can be turned into one). A tuple with the shape of the texture\n        can also be given.\n    format : str | enum | None\n        The format of the texture: 'luminance', 'alpha',\n        'luminance_alpha', 'rgb', or 'rgba'. If not given the format\n        is chosen automatically based on the number of channels.\n        When the data has one channel, 'luminance' is assumed.\n    resizable : bool\n        Indicates whether texture can be resized. Default True.\n    interpolation : str | None\n        Interpolation mode, must be one of: 'nearest', 'linear'.\n        Default 'nearest'.\n    wrapping : str | None\n        Wrapping mode, must be one of: 'repeat', 'clamp_to_edge',\n        'mirrored_repeat'. Default 'clamp_to_edge'.\n    shape : tuple | None\n        Optional. A tuple with the shape of the texture. If ``data``\n        is also a tuple, it will override the value of ``shape``.\n    internalformat : str | None\n        Internal format to use.\n    resizeable : None\n        Deprecated version of `resizable`.\n    "
    _glsl_sample_nearest = "\n        vec4 sample(sampler2D tex, vec3 texcoord) {\n            // Don't let adjacent frames be interpolated into this one\n            texcoord.x = min(texcoord.x * $shape.x, $shape.x - 0.5);\n            texcoord.x = max(0.5, texcoord.x) / $shape.x;\n            texcoord.y = min(texcoord.y * $shape.y, $shape.y - 0.5);\n            texcoord.y = max(0.5, texcoord.y) / $shape.y;\n\n            float index = floor(texcoord.z * $shape.z);\n\n            // Do a lookup in the 2D texture\n            float u = (mod(index, $r) + texcoord.x) / $r;\n            float v = (floor(index / $r) + texcoord.y) / $c;\n\n            return texture2D(tex, vec2(u,v));\n        }\n    "
    _glsl_sample_linear = "\n        vec4 sample(sampler2D tex, vec3 texcoord) {\n            // Don't let adjacent frames be interpolated into this one\n            texcoord.x = min(texcoord.x * $shape.x, $shape.x - 0.5);\n            texcoord.x = max(0.5, texcoord.x) / $shape.x;\n            texcoord.y = min(texcoord.y * $shape.y, $shape.y - 0.5);\n            texcoord.y = max(0.5, texcoord.y) / $shape.y;\n\n            float z = texcoord.z * $shape.z;\n            float zindex1 = floor(z);\n            float u1 = (mod(zindex1, $r) + texcoord.x) / $r;\n            float v1 = (floor(zindex1 / $r) + texcoord.y) / $c;\n\n            float zindex2 = zindex1 + 1.0;\n            float u2 = (mod(zindex2, $r) + texcoord.x) / $r;\n            float v2 = (floor(zindex2 / $r) + texcoord.y) / $c;\n\n            vec4 s1 = texture2D(tex, vec2(u1, v1));\n            vec4 s2 = texture2D(tex, vec2(u2, v2));\n\n            return s1 * (zindex2 - z) + s2 * (z - zindex1);\n        }\n    "
    _gl_max_texture_size = 1024

    def __init__(self, data=None, format=None, resizable=True, interpolation=None, wrapping=None, shape=None, internalformat=None, resizeable=None):
        from visuals.shaders import Function
        self._set_emulated_shape(data)
        Texture2D.__init__(self, self._normalize_emulated_shape(data), format, resizable, interpolation, wrapping, shape, internalformat, resizeable)
        if self.interpolation == 'nearest':
            self._glsl_sample = Function(self.__class__._glsl_sample_nearest)
        else:
            self._glsl_sample = Function(self.__class__._glsl_sample_linear)
        self._update_variables()

    def _set_emulated_shape(self, data_or_shape):
        if isinstance(data_or_shape, np.ndarray):
            self._emulated_shape = data_or_shape.shape
        else:
            assert isinstance(data_or_shape, tuple)
            self._emulated_shape = tuple(data_or_shape)
        depth, width = self._emulated_shape[0], self._emulated_shape[1]
        self._r = TextureEmulated3D._gl_max_texture_size // width
        self._c = depth // self._r
        if math.fmod(depth, self._r):
            self._c += 1

    def _normalize_emulated_shape(self, data_or_shape):
        if isinstance(data_or_shape, np.ndarray):
            new_shape = self._normalize_emulated_shape(data_or_shape.shape)
            new_data = np.empty(new_shape, dtype=(data_or_shape.dtype))
            for j in range(self._c):
                for i in range(self._r):
                    i0, i1 = i * self.width, (i + 1) * self.width
                    j0, j1 = j * self.height, (j + 1) * self.height
                    k = j * self._r + i
                    if k >= self.depth:
                        break
                    new_data[j0:j1, i0:i1] = data_or_shape[k]

            return new_data
        assert isinstance(data_or_shape, tuple)
        return (self._c * self.height, self._r * self.width) + data_or_shape[3:]

    def _update_variables(self):
        self._glsl_sample['shape'] = self.shape[:3][::-1]
        self._glsl_sample['c'] = self._c
        self._glsl_sample['r'] = self._r

    def set_data(self, data, offset=None, copy=False):
        """Set texture data

        Parameters
        ----------
        data : ndarray
            Data to be uploaded
        offset: int | tuple of ints
            Offset in texture where to start copying data
        copy: bool
            Since the operation is deferred, data may change before
            data is actually uploaded to GPU memory. Asking explicitly
            for a copy will prevent this behavior.

        Notes
        -----
        This operation implicitely resizes the texture to the shape of
        the data if given offset is None.
        """
        self._set_emulated_shape(data)
        Texture2D.set_data(self, self._normalize_emulated_shape(data), offset, copy)
        self._update_variables()

    def resize(self, shape, format=None, internalformat=None):
        """Set the texture size and format

        Parameters
        ----------
        shape : tuple of integers
            New texture shape in zyx order. Optionally, an extra dimention
            may be specified to indicate the number of color channels.
        format : str | enum | None
            The format of the texture: 'luminance', 'alpha',
            'luminance_alpha', 'rgb', or 'rgba'. If not given the format
            is chosen automatically based on the number of channels.
            When the data has one channel, 'luminance' is assumed.
        internalformat : str | enum | None
            The internal (storage) format of the texture: 'luminance',
            'alpha', 'r8', 'r16', 'r16f', 'r32f'; 'luminance_alpha',
            'rg8', 'rg16', 'rg16f', 'rg32f'; 'rgb', 'rgb8', 'rgb16',
            'rgb16f', 'rgb32f'; 'rgba', 'rgba8', 'rgba16', 'rgba16f',
            'rgba32f'.  If None, the internalformat is chosen
            automatically based on the number of channels.  This is a
            hint which may be ignored by the OpenGL implementation.
        """
        self._set_emulated_shape(shape)
        Texture2D.resize(self, self._normalize_emulated_shape(shape), format, internalformat)
        self._update_variables()

    @property
    def shape(self):
        """ Data shape (last dimension indicates number of color channels)
        """
        return self._emulated_shape

    @property
    def width(self):
        """ Texture width """
        return self._emulated_shape[2]

    @property
    def height(self):
        """ Texture height """
        return self._emulated_shape[1]

    @property
    def depth(self):
        """ Texture depth """
        return self._emulated_shape[0]

    @property
    def glsl_sample(self):
        """ GLSL function that samples the texture.
        """
        return self._glsl_sample


class TextureAtlas(Texture2D):
    __doc__ = 'Group multiple small data regions into a larger texture.\n\n    The algorithm is based on the article by Jukka Jylänki : "A Thousand Ways\n    to Pack the Bin - A Practical Approach to Two-Dimensional Rectangle Bin\n    Packing", February 27, 2010. More precisely, this is an implementation of\n    the Skyline Bottom-Left algorithm based on C++ sources provided by Jukka\n    Jylänki at: http://clb.demon.fi/files/RectangleBinPack/.\n\n    Parameters\n    ----------\n    shape : tuple of int\n        Texture shape (optional).\n\n    Notes\n    -----\n    This creates a 2D texture that holds 1D float32 data.\n    An example of simple access:\n\n        >>> atlas = TextureAtlas()\n        >>> bounds = atlas.get_free_region(20, 30)\n        >>> atlas.set_region(bounds, np.random.rand(20, 30).T)\n    '

    def __init__(self, shape=(1024, 1024)):
        shape = np.array(shape, int)
        if not (shape.ndim == 1 and shape.size == 2):
            raise AssertionError
        shape = tuple(2 ** (np.log2(shape) + 0.5).astype(int)) + (3, )
        self._atlas_nodes = [(0, 0, shape[1])]
        data = np.zeros(shape, np.float32)
        super(TextureAtlas, self).__init__(data, interpolation='linear', wrapping='clamp_to_edge')

    def get_free_region(self, width, height):
        """Get a free region of given size and allocate it

        Parameters
        ----------
        width : int
            Width of region to allocate
        height : int
            Height of region to allocate

        Returns
        -------
        bounds : tuple | None
            A newly allocated region as (x, y, w, h) or None
            (if failed).
        """
        best_height = best_width = np.inf
        best_index = -1
        for i in range(len(self._atlas_nodes)):
            y = self._fit(i, width, height)
            if y >= 0:
                node = self._atlas_nodes[i]
                if not y + height < best_height:
                    if not y + height == best_height or node[2] < best_width:
                        best_height = y + height
                        best_index = i
                        best_width = node[2]
                        region = (node[0], y, width, height)

        if best_index == -1:
            return
        node = (
         region[0], region[1] + height, width)
        self._atlas_nodes.insert(best_index, node)
        i = best_index + 1
        while i < len(self._atlas_nodes):
            node = self._atlas_nodes[i]
            prev_node = self._atlas_nodes[(i - 1)]
            if node[0] < prev_node[0] + prev_node[2]:
                shrink = prev_node[0] + prev_node[2] - node[0]
                x, y, w = self._atlas_nodes[i]
                self._atlas_nodes[i] = (x + shrink, y, w - shrink)
                if self._atlas_nodes[i][2] <= 0:
                    del self._atlas_nodes[i]
                    i -= 1
                else:
                    break
            else:
                break
            i += 1

        i = 0
        while i < len(self._atlas_nodes) - 1:
            node = self._atlas_nodes[i]
            next_node = self._atlas_nodes[(i + 1)]
            if node[1] == next_node[1]:
                self._atlas_nodes[i] = (
                 node[0], node[1], node[2] + next_node[2])
                del self._atlas_nodes[i + 1]
            else:
                i += 1

        return region

    def _fit(self, index, width, height):
        """Test if region (width, height) fit into self._atlas_nodes[index]"""
        node = self._atlas_nodes[index]
        x, y = node[0], node[1]
        width_left = width
        if x + width > self._shape[1]:
            return -1
        i = index
        while width_left > 0:
            node = self._atlas_nodes[i]
            y = max(y, node[1])
            if y + height > self._shape[0]:
                return -1
            width_left -= node[2]
            i += 1

        return y