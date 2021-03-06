# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/bokeh_templating/factory.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 5380 bytes
"""
Created on Mon Feb 20 14:05:03 2017

@author: gkanarek
"""
from bokeh.io import curdoc
from .keyword_map import bokeh_mappings as mappings, bokeh_sequences as sequences
Figure = mappings.pop('Figure')
del sequences['figure']

def mapping_factory(tool, element_type):

    def mapping_constructor(loader, node):
        fmt = tool.formats.get(element_type, {})
        value = loader.construct_mapping(node, deep=True)
        ref = value.pop('ref', '')
        callback = value.pop('on_change', [])
        selection_callback = value.pop('selection_on_change', [])
        onclick = value.pop('on_click', None)
        fmt.update(value)
        if element_type == 'Slider':
            fmt['start'], fmt['end'], fmt['step'] = fmt.pop('range', [0, 1, 0.1])
        else:
            arg = fmt.pop('arg', None)
            if arg is not None:
                obj = (mappings[element_type])(*arg, **fmt)
            else:
                obj = (mappings[element_type])(**fmt)
        if ref:
            tool.refs[ref] = obj
        if callback:
            (obj.on_change)(*callback)
        if onclick:
            obj.on_click(onclick)
        if selection_callback:
            (obj.selected.on_change)(*selection_callback)
        yield obj

    mapping_constructor.__name__ = element_type.lower() + '_' + mapping_constructor.__name__
    return mapping_constructor


def sequence_factory(tool, element_type):

    def sequence_constructor(loader, node):
        fmt = tool.formats.get(element_type, {})
        value = loader.construct_sequence(node, deep=True)
        obj = (sequences[element_type])(*value, **fmt)
        yield obj

    sequence_constructor.__name__ = element_type.lower() + '_' + sequence_constructor.__name__
    return sequence_constructor


def document_constructor(tool, loader, node):
    layout = loader.construct_sequence(node, deep=True)
    for element in layout:
        curdoc().add_root(element)

    tool.document = curdoc()
    yield tool.document


def figure_constructor(tool, loader, node):
    fig = loader.construct_mapping(node, deep=True)
    fmt = tool.formats.get('Figure', {})
    elements = fig.pop('elements', [])
    cmds = []
    ref = fig.pop('ref', '')
    callback = fig.pop('on_change', [])
    axis = tool.formats.get('Axis', {})
    axis.update(fig.pop('axis', {}))
    for key in fig:
        val = fig[key]
        if key in ('text', 'add_tools', 'js_on_event'):
            cmds.append((key, val))
        else:
            fmt[key] = val

    figure = Figure(**fmt)
    for key, cmd in cmds:
        if key == 'add_tools':
            (figure.add_tools)(*cmd)
        else:
            if key == 'text':
                (figure.text)(*cmd.pop('loc'), **cmd)
            else:
                if key == 'js_on_event':
                    for event in cmd:
                        (figure.js_on_event)(*event)

    for element in elements:
        key = element.pop('kind')
        shape = {'line':('Line', figure.line),  'circle':(
          'Circle', figure.circle), 
         'diamond':(
          'Diamond', figure.diamond), 
         'triangle':(
          'Triangle', figure.triangle), 
         'square':(
          'Square', figure.square), 
         'asterisk':(
          'Asterisk', figure.asterisk), 
         'x':(
          'XGlyph', figure.x), 
         'vbar':(
          'VBar', figure.vbar)}
        if key in shape:
            fmt_key, glyph = shape[key]
            shape_fmt = tool.formats.get(fmt_key, {})
            shape_fmt.update(element)
            x = shape_fmt.pop('x', 'x')
            y = shape_fmt.pop('y', 'y')
            glyph(x, y, **shape_fmt)
        elif key == 'rect':
            rect_fmt = tool.formats.get('Rect', {})
            rect_fmt.update(element)
            (figure.rect)(*('rx', 'ry', 'rw', 'rh'), **rect_fmt)
        else:
            if key == 'quad':
                quad_fmt = tool.formats.get('Quad', {})
                quad_fmt.update(element)
                (figure.quad)(**quad_fmt)
            else:
                if key == 'image':
                    image_fmt = tool.formats.get('Image', {})
                    image_fmt.update(element)
                    arg = image_fmt.pop('image', None)
                    (figure.image)(arg, **image_fmt)
                else:
                    if key == 'image_rgba':
                        image_fmt = tool.formats.get('ImageRGBA', {})
                        image_fmt.update(element)
                        arg = image_fmt.pop('image', None)
                        (figure.image_rgba)(arg, **image_fmt)
                    else:
                        if key == 'multi_line':
                            multi_fmt = tool.formats.get('MultiLine', {})
                            multi_fmt.update(element)
                            (figure.multi_line)(**multi_fmt)
                        elif key == 'layout':
                            obj = element.pop('obj', None)
                            (figure.add_layout)(obj, **element)

    for attr, val in axis.items():
        setattr(figure.axis, attr, val)

    if ref:
        tool.refs[ref] = figure
    if callback:
        (figure.on_change)(*callback)
    yield figure