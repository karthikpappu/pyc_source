# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.15/lib/python2.7/site-packages/coolamqp/attaches/channeler.py
# Compiled at: 2020-05-06 12:56:42
__doc__ = '\nBase class for consumer or publisher with the capabiility to\nset up and tear down channels\n'
from __future__ import print_function, absolute_import, division
import logging, typing as tp
from coolamqp.framing.definitions import ChannelOpen, ChannelOpenOk, ChannelClose, ChannelCloseOk, BasicCancel, BasicCancelOk
from coolamqp.framing.frames import AMQPMethodFrame
ST_OFFLINE = 0
ST_SYNCING = 1
ST_ONLINE = 2
logger = logging.getLogger(__name__)

class Attache(object):
    """
    Something that can be attached to connection.
    """
    __slots__ = ('cancelled', 'state', 'connection')

    def __init__(self):
        self.cancelled = False
        self.state = ST_OFFLINE
        self.connection = None
        return

    def attach(self, connection):
        """
        Attach to a connection.

        :param connection: Connection instance of any state
        """
        assert self.connection is None
        assert connection.state != ST_OFFLINE
        self.connection = connection
        return


class Channeler(Attache):
    """
    A base class for Consumer/Publisher implementing link set up and tear down.

    A channeler can be essentially in 4 states:
    - ST_OFFLINE (.channel is None): channel is closed, object is unusable. Requires an attach() a connection
                                     that is being established, or open, or whatever. Connection will notify
                                     this channeler that it's open.
    - ST_SYNCING: channeler is opening a channel/doing some other things related to it's setup.
                  it's going to be ST_ONLINE soon, or go back to ST_OFFLINE.
                  It has, for sure, acquired a channel number.
    - ST_ONLINE:  channeler is operational. It has a channel number and has declared everything
                  it needs to.

                  on_operational(True) will be called when a transition is made TO this state.
                  on_operational(False) will be called when a transition is made FROM this state.

    - ST_OFFLINE (.channel is not None): channeler is undergoing a close. It has not yet torn down the channel,
                                         but ordering it to do anything is pointless, because it will not get done
                                         until attach() with new connection is called.
    """
    __slots__ = ('channel_id', )

    def __init__(self):
        """
        [EXTEND ME!]
        """
        super(Channeler, self).__init__()
        self.channel_id = None
        return

    def attach(self, connection):
        """
        Attach this object to a live Connection.

        :param connection: Connection instance to use
        """
        super(Channeler, self).attach(connection)
        assert self.connection is not None
        connection.call_on_connected(self.on_uplink_established)
        return

    def on_operational(self, operational):
        """
        [EXTEND ME] Called by internal methods (on_*) when channel has achieved (or lost) operational status.

        If this is called with operational=True, then for sure it will be called with operational=False.

        This will, therefore, get called an even number of times.

        Called by Channeler, when:
            - Channeler.on_close gets called and state is ST_ONLINE
                on_close registers ChannelClose, ChannelCloseOk, BasicCancel

        :param operational: True if channel has just become operational, False if it has just become useless.
        """
        pass

    def on_close(self, payload=None):
        """
        [EXTEND ME] Handler for channeler destruction.

        Channeler registers this for:
            (None - socket dead)
            (BasicCancel, BasicCancelOk, ChannelCloseOk, ChannelClose)

        This method provides to send a response for ChannelClose

        This handles following situations:
        - payload is None: this means that connection has gone down hard, so our Connection object is
                           probably very dead. Transition to ST_OFFLINE (.channel is None)
        - payload is a ChannelClose: this means that a channel exception has occurred. Dispatch a ChannelCloseOk,
                                     attempt to log an exception, transition to ST_OFFLINE (.channel is None)
        - payload is a ChannelCloseOk: this means that it was us who attempted to close the channel. Return the channel
                                       to free pool, transition to ST_OFFLINE (.channel is None)

        If you need to handle something else, extend this. Take care that this DOES NOT HANDLE errors that happen
        while state is ST_SYNCING. You can expect this to handle a full channel close, therefore releasing all
        resources, so it mostly will do *the right thing*.

        If you need to do something else than just close a channel, please extend or modify as necessary.

        WARNING: THIS WILL GET CALLED TWICE.
            Once on ChannelClose - if so,
            Second with None - because socket dies.

            Be prepared!

        """
        if self.connection is None:
            return
        else:
            if self.state == ST_ONLINE:
                self.on_operational(False)
            self.state = ST_OFFLINE
            if not isinstance(payload, (ChannelClose, ChannelCloseOk)) and payload is not None:
                return
            if isinstance(payload, ChannelClose):
                self.method(ChannelCloseOk())
            if payload is not None:
                assert self.channel_id is not None
                self.connection.free_channels.append(self.channel_id)
                self.connection.unwatch_all(self.channel_id)
            self.connection = None
            self.channel_id = None
            if isinstance(payload, ChannelClose):
                logger.debug('Channel closed: %s %s', payload.reply_code, payload.reply_text.tobytes())
            return

    def methods(self, payloads):
        """
        Syntactic sugar for

            for payload in paylods:
                self.method(payload)

        But moar performant.
        """
        if self.channel_id is None:
            return
        else:
            frames = [ AMQPMethodFrame(self.channel_id, payload) for payload in payloads
                     ]
            self.connection.send(frames)
            return

    def method(self, payload):
        """
        Syntactic sugar for:

            self.connection.send([AMQPMethodFrame(self.channel_id, payload)])
        """
        self.methods([payload])

    def watch_for_method(self, method, callback, on_fail=None):
        """
        Syntactic sugar for

        >>> self.connection.watch_for_method(self.channel_id, method, callback, on_fail=on_fail)
        """
        assert self.channel_id is not None
        return self.connection.watch_for_method(self.channel_id, method, callback, on_fail=on_fail)

    def method_and_watch(self, method_payload, method_classes_to_watch, callable):
        """
        Syntactic sugar for

        >>> self.connection.method_and_watch(self.channel_id,
        >>>                                  method_payload,
        >>>                                  method_classes_to_watch,
        >>>                                  callable)
        """
        assert self.channel_id is not None
        self.connection.method_and_watch(self.channel_id, method_payload, method_classes_to_watch, callable)
        return

    def on_setup(self, payload):
        """
        [OVERRIDE ME!] Called with a method frame that signifies a part of setup.

        You must be prepared to handle at least a payload of ChannelOpenOk

        :param payload: AMQP method frame payload
        """
        raise Exception('Abstract method - override me!')

    def register_on_close_watch(self):
        """
        Register a watch for on_close.

        Since on_close is a one-shot, it will expire upon calling.

        To be called by on_close, when it needs to be notified just one more time.
        """
        self.connection.watch_for_method(self.channel_id, (
         ChannelClose, ChannelCloseOk, BasicCancel, BasicCancelOk), self.on_close, on_fail=self.on_close)

    def on_uplink_established(self):
        """Called by connection. Connection reports being ready to do things."""
        assert self.connection is not None
        assert self.connection.state == ST_ONLINE, repr(self)
        self.state = ST_SYNCING
        self.channel_id = self.connection.free_channels.pop()
        self.register_on_close_watch()
        self.connection.method_and_watch(self.channel_id, ChannelOpen(), ChannelOpenOk, self.on_setup)
        return