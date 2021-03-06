# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mattcowley/PycharmProjects/PyDMXControl/PyDMXControl/web/_routes.py
# Compiled at: 2019-06-26 14:49:14
# Size of source mod 2**32: 8665 bytes
__doc__ = '\n *  PyDMXControl: A Python 3 module to control DMX using uDMX.\n *                Featuring fixture profiles, built-in effects and a web control panel.\n *  <https://github.com/MattIPv4/PyDMXControl/>\n *  Copyright (C) 2019 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)\n'
from re import compile as re_compile
from typing import List, Union, Tuple, Dict, Callable
from flask import Blueprint, render_template, current_app, redirect, url_for, jsonify
from .. import Colors
from ..profiles.defaults import Fixture, Vdim
routes = Blueprint('', __name__, url_prefix='/')

def fixture_channels(this_fixture: Fixture) -> List[Tuple[(str, int)]]:
    chans = [(f['name'], fixture_channel_value(this_fixture, f['name'])) for f in this_fixture.channels.values()]
    if issubclass(type(this_fixture), Vdim):
        chans.append(('dimmer', fixture_channel_value(this_fixture, 'dimmer')))
    return chans


def fixture_channel_value(this_fixture: Fixture, this_channel: Union[(str, int)]) -> int:
    if issubclass(type(this_fixture), Vdim):
        return this_fixture.get_channel_value(this_channel, False)[0]
    else:
        return this_fixture.get_channel_value(this_channel)[0]


helpers = [
 'on', 'off', 'locate']

def fixture_helpers(this_fixture: Fixture) -> Dict[(str, Callable)]:
    return {f:this_fixture.__getattribute__(f) for f in helpers if hasattr(this_fixture, f)}


@routes.route('', methods=['GET'])
def home():
    return render_template('index.jinja2', helpers=helpers)


@routes.route('intensity/<int:val>', methods=['GET'])
def global_intensity(val: int):
    if val < 0 or val > 255:
        return (jsonify({'error': 'Value {} is invalid'.format(val)}), 400)
    else:
        current_app.parent.controller.all_dim(val)
        return (
         jsonify({'message': 'All dimmers updated to {}'.format(val)}), 200)


@routes.route('fixture/<int:fid>', methods=['GET'])
def fixture(fid: int):
    this_fixture = current_app.parent.controller.get_fixture(fid)
    if not this_fixture:
        return redirect(url_for('.home'))
    else:
        return render_template('fixture.jinja2', fixture=this_fixture, fixture_channels=fixture_channels, colors=Colors,
          helpers=helpers)


@routes.route('fixture/<int:fid>/channel/<int:cid>', methods=['GET'])
def channel(fid: int, cid: int):
    this_fixture = current_app.parent.controller.get_fixture(fid)
    if not this_fixture:
        return redirect(url_for('.home'))
    else:
        chan = this_fixture.get_channel_id(cid)
        if chan == -1:
            return redirect(url_for('.fixture', fid=(this_fixture.id)))
        this_channel = fixture_channels(this_fixture)[chan]
        return render_template('channel.jinja2', fixture=this_fixture, channel=this_channel, cid=chan)


@routes.route('fixture/<int:fid>/channel/<int:cid>/<int:val>', methods=['GET'])
def channel_val(fid: int, cid: int, val: int):
    this_fixture = current_app.parent.controller.get_fixture(fid)
    if not this_fixture:
        return (jsonify({'error': 'Fixture {} not found'.format(fid)}), 404)
    chan = this_fixture.get_channel_id(cid)
    if chan == -1:
        return (jsonify({'error': 'Channel {} not found'.format(cid)}), 404)
    if val < 0 or val > 255:
        return (jsonify({'error': 'Value {} is invalid'.format(val)}), 400)
    else:
        this_fixture.set_channel(chan, val)
        val = fixture_channel_value(this_fixture, chan)
        data = {'message':'Channel {} {} updated to {}'.format(chan + 1, this_fixture.channels[(chan + 1)]['name'], val),  'elements':{'channel-{}-value'.format(chan): val, 
          'value': val, 
          'slider_value': val}}
        if chan == this_fixture.get_channel_id('dimmer'):
            data['elements']['intensity_value'] = val
        return (jsonify(data), 200)


@routes.route('fixture/<int:fid>/color/<string:val>', methods=['GET'])
def color(fid: int, val: str):
    this_fixture = current_app.parent.controller.get_fixture(fid)
    if not this_fixture:
        return (jsonify({'error': 'Fixture {} not found'.format(fid)}), 404)
    else:
        pattern = re_compile('^\\s*(\\d{1,3})\\s*[, ]\\s*(\\d{1,3})\\s*[, ]\\s*(\\d{1,3})\\s*(?:[, ]\\s*(\\d{1,3})\\s*)*$')
        match = pattern.match(val)
        if not match:
            return (jsonify({'error': 'Invalid color {} supplied'.format(val)}), 400)
        this_color = [int(f) for f in match.groups() if f]
        this_fixture.color(this_color)
        return (
         jsonify({'message':'Color updated to {}'.format(this_color),  'elements':dict({'value': Colors.to_hex(this_fixture.get_color())}, **)}), 200)


@routes.route('fixture/<int:fid>/intensity/<int:val>', methods=['GET'])
def intensity(fid: int, val: int):
    this_fixture = current_app.parent.controller.get_fixture(fid)
    if not this_fixture:
        return (jsonify({'error': 'Fixture {} not found'.format(fid)}), 404)
    chan = this_fixture.get_channel_id('dimmer')
    if chan == -1:
        return (jsonify({'error': 'Dimmer channel not found'}), 404)
    else:
        if val < 0 or val > 255:
            return (jsonify({'error': 'Value {} is invalid'.format(val)}), 400)
        this_fixture.set_channel(chan, val)
        val = fixture_channel_value(this_fixture, chan)
        return (
         jsonify({'message':'Dimmer updated to {}'.format(val),  'elements':{'channel-{}-value'.format(chan): val, 
           'intensity_value': val}}),
         200)


@routes.route('fixture/<int:fid>/helper/<string:val>', methods=['GET'])
def helper(fid: int, val: str):
    this_fixture = current_app.parent.controller.get_fixture(fid)
    if not this_fixture:
        return (jsonify({'error': 'Fixture {} not found'.format(fid)}), 404)
    val = val.lower()
    this_helpers = fixture_helpers(this_fixture)
    if val not in this_helpers.keys():
        return (jsonify({'error': 'Helper {} not found'.format(val)}), 404)
    try:
        this_helpers[val]()
    except Exception:
        return (
         jsonify({'error': 'Helper {} failed to execute'.format(val)}), 500)
    else:
        return (jsonify({'message':'Helper {} executed'.format(val),  'elements':dict(
           {'value':Colors.to_hex(this_fixture.get_color()), 
            'intensity_value':this_fixture.get_channel_value(this_fixture.get_channel_id('dimmer'))[0]}, **)}), 200)


@routes.route('callback/<string:cb>', methods=['GET'])
def callback(cb: str):
    if cb not in current_app.parent.callbacks.keys():
        return (jsonify({'error': 'Callback {} not found'.format(cb)}), 404)
    else:
        try:
            current_app.parent.callbacks[cb]()
        except Exception:
            return (
             jsonify({'error': 'Callback {} failed to execute'.format(cb)}), 500)

        return (jsonify({'message': 'Callback {} executed'.format(cb)}), 200)


@routes.route('timed_event/<string:te>', methods=['GET'])
def timed_event(te: str):
    if te not in current_app.parent.timed_events.keys():
        return redirect(url_for('.home'))
    else:
        return render_template('timed_event.jinja2', te=te)


@routes.route('timed_event/<string:te>/data', methods=['GET'])
def timed_event_data(te: str):
    if te not in current_app.parent.timed_events.keys():
        return (jsonify({'error': 'Timed Event {} not found'.format(te)}), 404)
    else:
        return (
         jsonify({'data': current_app.parent.timed_events[te].data}), 200)


@routes.route('timed_event/<string:te>/run', methods=['GET'])
def run_timed_event(te: str):
    if te not in current_app.parent.timed_events.keys():
        return (jsonify({'error': 'Timed Event {} not found'.format(te)}), 404)
    else:
        try:
            current_app.parent.timed_events[te].run()
        except Exception:
            return (
             jsonify({'error': 'Timed Event {} failed to fire'.format(te)}), 500)

        return (jsonify({'message':'Timed Event {} fired'.format(te),  'elements':{te + '-state': 'Running'}}), 200)


@routes.route('timed_event/<string:te>/stop', methods=['GET'])
def stop_timed_event(te: str):
    if te not in current_app.parent.timed_events.keys():
        return (jsonify({'error': 'Timed Event {} not found'.format(te)}), 404)
    else:
        try:
            current_app.parent.timed_events[te].stop()
        except Exception:
            return (
             jsonify({'error': 'Timed Event {} failed to stop'.format(te)}), 500)

        return (jsonify({'message':'Timed Event {} stopped'.format(te),  'elements':{te + '-state': 'Stopped'}}), 200)