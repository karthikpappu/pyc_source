# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tele/client.py
# Compiled at: 2011-01-15 06:24:55
from __future__ import unicode_literals
from urllib import urlencode
from io import StringIO
from datetime import timedelta
import os, hashlib, time
from lxml import html
from pytz import utc
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.web.client import getPage
import pytz
from channel import Channel
from channel import ChannelList
from show import Show
from show import ShowList

def _init_cache(cache):
    """
    Creates the cache (or fails at this) and returns the **absolute** path of
    the directory you should use to cache, or None on failure.
    """
    try:
        if not os.path.isdir(cache):
            os.makedirs(cache)
        return os.path.abspath(cache)
    except OSError:
        return

    return


def _get_page(url, get, cache):
    """
    Gets a page parsed as lxml HTML from the url or the cache if that already
    exists. This returns a Deferred that gets the <html>-Element as lxml
    Element as first parameter.
    """
    if get:
        url += b'?' + urlencode(get)
    if cache:
        file = os.path.join(cache, hashlib.sha1(url).hexdigest())
        if os.path.isfile(file):
            url = b'file://' + file
            file = None
    else:
        file = None
    if url.startswith(b'file://'):
        defer = Deferred()
        try:
            with open(url[6:]) as (fp):
                defer.callback(fp.read())
        except IOError, ioe:
            defer.errback(ioe)

    else:
        defer = getPage(str(url), timeout=10)

    def on_success(htmlstr):
        if file:
            try:
                with open(file, b'w') as (fp):
                    fp.write(htmlstr)
            except:
                if os.path.isfile(file):
                    os.unlink(file)
                raise

        return html.parse(StringIO(unicode(htmlstr, b'utf8'))).getroot()

    defer.addCallback(on_success)
    defer.addErrback(lambda failure: failure)
    return defer


class Client(object):
    """
    Client for interfacing http://tele.at/.
    """

    def __init__(self, url=b'http://tele.at/programmvorschau.php', cache=os.path.expanduser(os.path.join(b'~', b'.libtele_cache'))):
        self.url = url
        self.cache = _init_cache(cache)

    def get_channels(self):
        """
        Gets a list of all TV channels supported by this source. This returns
        a defer that gets a ``ChannelList`` as its first parameter in the
        callback.
        """

        def parse(html):
            CSS = b'select[name=channels] optgroup[label!=Alphabetisch] option'
            channels = ChannelList()
            for elem in html.cssselect(CSS):
                values = elem.attrib[b'value'].split(b']')[1].split(b',')
                texts = elem.text.split(b',')
                assert len(values) == len(texts)
                for i in xrange(len(values)):
                    channels.append(Channel(values[i].strip(), texts[i].strip()))

            return channels

        defer = _get_page(self.url, {}, self.cache)
        defer.addCallback(parse)
        defer.addErrback(lambda failure: failure)
        return defer

    def get_tele_day(self, channel, thetime):
        """
        Gets a list of the TV-shows of a day.
        
        **Important:** If you use dates too far in the past or too far in the
        future, or if you supply an invalid channel this function returns
        **strange results**!
        
        **Important:** A "Tele Day" starts and ends at 5 am (CET)! Just play
        around a bit with the API to understand it (or take a look at the unit
        tests).
        
        **Important:** The Tele servers are really bad, and sometimes return
        very strange DOM. If you use this method you should remove duplicates
        and handle timeouts. I suggest you to use the ``get_shows`` method.
        
        +------------------+------------------------+----------------------+
        | Value of ``day`` | Start time of the list | End time of the list |
        +==================+========================+======================+
        | 2010-01-20 14:00 | 2010-01-20 05:00       | 2010-01-21 04:59     |
        +------------------+------------------------+----------------------+
        | 2010-01-21 00:45 | 2010-01-20 05:00       | 2010-01-21 04:59     |
        +------------------+------------------------+----------------------+
        | 2010-01-20 04:00 | 2010-01-19 05:00       | 2010-01-20 04:59     |
        +------------------+------------------------+----------------------+
        
        :type channel: tele.channel.Channel
        :param channel: The channel you want the TV guide of.
        :type day: datetime.datetime
        :param day: Any datetime of the "Tele Day" you want the TV guide from,
                    this method will convert it into the correct format.
        """
        cet = pytz.timezone(b'CET')
        thetime = cet.normalize(thetime.astimezone(cet))
        if thetime.hour < 5:
            thetime = cet.normalize(thetime - timedelta(days=1))
        thetime = cet.localize(thetime.replace(hour=5, minute=0, second=0, microsecond=0, tzinfo=None), False)

        def parse(html, thetime):
            list = ShowList()
            for elem in html.cssselect(b'td.starttime'):
                (hour, minute) = elem.text.split(b':')
                hour = int(hour)
                minute = int(minute)
                time = cet.localize(thetime.replace(hour=hour, minute=minute, tzinfo=None), False)
                if hour < 5:
                    time = cet.normalize(time + timedelta(days=1))
                elem = elem.getnext()
                title = elem.cssselect(b'h5 a')[0].text
                episodetitle = elem.cssselect(b'span.episodetitle, span.subtitle')
                if episodetitle:
                    subtitle = episodetitle[0].text
                else:
                    subtitle = b''
                genre = elem.cssselect(b'span.genre')[0].text
                list.append(Show(time, title, subtitle, genre))

            return list

        tsstart = str(int(time.mktime(thetime.timetuple())))
        get = {b'channels': channel.key, b'tsstart': tsstart}
        defer = _get_page(self.url, get, self.cache)
        defer.addCallback(parse, thetime)
        defer.addErrback(lambda failure: failure)
        return defer

    def get_shows(self, channel, fromtime, totime):
        """
        Gets a list of shows in the given period of time. This method returns
        a Deferred. The callback gets one parameter, the ``ChannelList`` of
        the period of time. The errback is called on an error with the
        failure.
        
        The first show will be the one **before** (or equal) fromtime and the
        last one will be the last show **before** (or equal) totime.
        
        ``frotime`` and ``totime`` will be handeled correctly if it is not in
        UTC time.
        """

        def parse_day(shows, fromtime, totime, defer, result, channel):
            ready = False
            while len(shows) > 1 and shows[1].time <= fromtime:
                shows = shows[1:]
                ready = True

            showlist = ShowList()
            for show in shows:
                if show.time <= totime:
                    showlist.append(show)
                else:
                    break

            i = 0
            for show in showlist:
                result.insert(i, show)
                i += 1

            if ready:
                defer.callback(result)
            else:
                yesterday = self.get_tele_day(channel, shows[0].time - timedelta(days=1))
                yesterday.addCallback(parse_day, fromtime, totime, defer, result, channel)
                yesterday.addErrback(defer.errback)

        fromtime = utc.normalize(fromtime.astimezone(utc))
        totime = utc.normalize(totime.astimezone(utc))
        defer = Deferred()
        result = ShowList()
        last_defer = self.get_tele_day(channel, totime)
        last_defer.addCallback(parse_day, fromtime, totime, defer, result, channel)
        last_defer.addErrback(defer.errback)
        return defer