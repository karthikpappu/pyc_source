# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pepperedform/handler.py
# Compiled at: 2012-06-24 14:59:25
"""
Hooks for use with the Handler class in formprocess.
"""
from peppercorn import parse

def parse_with_peppercorn(handler_instance, unsafe_params, state):
    """
    Extract form params in the peppercorn format into structured params.

    Note: This should be used as a default_filter_hook in a formprocess
        handler.
    """
    return parse(unsafe_params.items())


def renderer_state_injector(form_renderer, inject_at_key='renderer_state'):
    """
    Wrap a closure around the given form_renderer that creates a form
    renderer state and places it in the fill kwargs at the given
    key.
    """

    def inject_renderer_state(handler_instance, defaults, errors, state, fill_kwargs):
        fill_kwargs[inject_at_key] = form_renderer.form_renderer_state(defaults, errors)
        return fill_kwargs

    return inject_renderer_state