# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/cachedownloader.py
# Compiled at: 2011-05-10 14:38:51
VERSION = 14
VERSION_DATE = '2011-05-07'
try:
    import json
    json.dumps
except (ImportError, AttributeError):
    import simplejson as json

from geocaching import GeocacheCoordinate
import datetime, geo, os, threading, logging
logger = logging.getLogger('cachedownloader')
try:
    import Image
except:
    Image = None
    logger.info('Not using image resize feature')

import re, gobject

class HTMLManipulations(object):
    COMMENT_REGEX = re.compile('<!--.*?-->', re.DOTALL)

    @staticmethod
    def _strip_html(text, soft=False):
        if not soft:
            return re.sub('<[^>]*?>', '', text)
        else:
            return re.sub('<[^>]*?>', ' ', text)

    @staticmethod
    def strip_html_visual(text, image_replace_callback):
        text = text.replace('\n', ' ')
        text = re.sub('(?i)<img[^>]+alt=["\']?([^\'"> ]+)[^>]+>', image_replace_callback, text)
        text = re.sub('(?i)<(br|p)[^>]*?>', '\n', text)
        text = re.sub('<[^>]*?>', '', text)
        text = HTMLManipulations._decode_htmlentities(text)
        text = re.sub('[\\n\\r]+\\s*[\\n\\r]+', '\n', text)
        return text.strip()

    @staticmethod
    def _replace_br(text):
        return re.sub('<[bB][rR]\\s*/?>|</?[pP]>', '\n', text)

    @staticmethod
    def _decode_htmlentities(string):

        def substitute_entity(match):
            from htmlentitydefs import name2codepoint as n2cp
            ent = match.group(3)
            if match.group(1) == '#':
                if match.group(2) == '':
                    return unichr(int(ent))
                if match.group(2) == 'x':
                    return unichr(int('0x' + ent, 16))
            else:
                cp = n2cp.get(ent)
                if cp:
                    return unichr(cp)
                return match.group()

        entity_re = re.compile('&(#?)(x?)(\\w+);')
        return entity_re.subn(substitute_entity, string)[0]


class CacheDownloader(gobject.GObject):
    __gsignals__ = {'finished-overview': (gobject.SIGNAL_RUN_FIRST,
                           gobject.TYPE_NONE,
                           (
                            gobject.TYPE_PYOBJECT,)), 
       'progress': (
                  gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (str, int, int)), 
       'download-error': (
                        gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)), 
       'already-downloading-error': (
                                   gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)), 
       'finished-single': (
                         gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)), 
       'finished-multiple': (
                           gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))}
    lock = threading.Lock()

    @staticmethod
    def _rot13(text):
        return text.encode('rot13')

    def __init__(self, downloader, path, download_images, resize=None):
        gobject.GObject.__init__(self)
        self.downloader = downloader
        self.path = path
        self.download_images = download_images
        self.resize = resize
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except:
                raise Exception('Path does not exist: %s' % path)

    def _init_images(self):
        self.downloaded_images = {}
        self.current_image = 0
        self.images = {}

    def _download_image(self, url):
        global Image
        logger.info('Checking download for %s' % url)
        if url in self.downloaded_images:
            return self.downloaded_images[url]
        else:
            ext = url.rsplit('.', 1)[1]
            if not re.match('^[a-zA-Z0-9]+$', ext):
                ext = 'img'
            filename = ''
            id = '%s-image%d.%s' % (self.current_cache.name, self.current_image, ext)
            if self.download_images:
                try:
                    filename = os.path.join(self.path, id)
                    logger.info('Downloading %s to %s' % (url, filename))
                    f = open(filename, 'wb')
                    f.write(self.downloader.get_reader(url).read())
                    f.close()
                    if Image != None and self.resize != None and self.resize > 0:
                        im = Image.open(filename)
                        im.thumbnail((self.resize, self.resize), Image.ANTIALIAS)
                        im.save(filename)
                except Exception, e:
                    logger.exception('Could not download %s: %s' % (url, e))
                    return

            self.downloaded_images[url] = id
            self.current_image += 1
            return id

    def update_coordinates(self, coordinates):
        i = 0
        c = []
        if len(coordinates) > self.MAX_DOWNLOAD_NUM:
            self.emit('download-error', Exception('Downloading of more than %d descriptions is not supported.' % self.MAX_DOWNLOAD_NUM))
            return
        for cache in coordinates:
            self.emit('progress', cache.name, i, len(coordinates))
            u = self.update_coordinate(cache)
            c.append(u)
            i += 1

        self.emit('finished-multiple', c)
        return c

    def update_coordinate(self, coordinate, outfile=None):
        if not CacheDownloader.lock.acquire(False):
            self.emit('already-downloading-error', Exception("There's a download in progress. Please wait."))
            return
        else:
            self._init_images()
            coordinate = coordinate.clone()
            self.current_cache = coordinate
            try:
                logger.info('Downloading %s...' % coordinate.name)
                response = self._get_cache_page(coordinate.name)
                if outfile != None:
                    f = open(outfile, 'w')
                    f.write(response.read())
                    f.close()
                    response = open(outfile)
                u = self._parse_cache_page(response, coordinate)
            except Exception, e:
                CacheDownloader.lock.release()
                self.emit('download-error', e)
                return self.current_cache

            CacheDownloader.lock.release()
            self.emit('finished-single', u)
            return u

    def get_geocaches(self, location, rec_depth=0):
        if not CacheDownloader.lock.acquire(False):
            self.emit('already-downloading-error', Exception("There's a download in progress. Please wait."))
            logger.warning('Download in progress')
            return
        else:
            if rec_depth > self.MAX_REC_DEPTH:
                raise Exception('Please select a smaller part of the map.')
                CacheDownloader.lock.release()
                return []
            try:
                content = self._get_overview(location)
            except Exception, e:
                self.emit('download-error', e)
                CacheDownloader.lock.release()
                return []

            if content == None:
                return []
            try:
                points = self._parse_overview(content, location, rec_depth)
            except Exception, e:
                if rec_depth == 0:
                    self.emit('download-error', e)
                    CacheDownloader.lock.release()
                    return []
                raise e

            self.emit('finished-overview', points)
            CacheDownloader.lock.release()
            return points


class GeocachingComCacheDownloader(CacheDownloader):
    MAX_REC_DEPTH = 2
    MAX_DOWNLOAD_NUM = 20
    user_token = None
    CTIDS = {2: GeocacheCoordinate.TYPE_REGULAR, 
       3: GeocacheCoordinate.TYPE_MULTI, 
       4: GeocacheCoordinate.TYPE_VIRTUAL, 
       6: GeocacheCoordinate.TYPE_EVENT, 
       8: GeocacheCoordinate.TYPE_MYSTERY, 
       11: GeocacheCoordinate.TYPE_WEBCAM, 
       137: GeocacheCoordinate.TYPE_EARTH}

    @staticmethod
    def login_callback(username, password):
        url = 'http://www.geocaching.com/login/default.aspx'
        values = {'ctl00$SiteContent$tbUsername': username, 'ctl00$SiteContent$tbPassword': password, 
           'ctl00$SiteContent$cbRememberMe': 'on', 
           'ctl00$SiteContent$btnSignIn': 'Login', 
           '__EVENTTARGET': '', 
           '__EVENTARGUMENT': ''}
        return (
         url, values)

    def _get_overview(self, location):
        if self.user_token == None:
            self._get_user_token()
        (c1, c2) = location
        url = 'http://www.geocaching.com/map/default.aspx/MapAction?lat=9&lng=6'
        data = (
         'application/json', '{"dto":{"data":{"c":1,"m":"","d":"%f|%f|%f|%f"},"ut":"%s"}}' % (max(c1.lat, c2.lat), min(c1.lat, c2.lat), max(c1.lon, c2.lon), min(c1.lon, c2.lon), self.user_token))
        try:
            response = self.downloader.get_reader(url, data=data)
            the_page = response.read()
        except Exception, e:
            CacheDownloader.lock.release()
            self.emit('download-error', e)
            return

        return the_page

    def _get_user_token(self):
        page = self.downloader.get_reader('http://www.geocaching.com/map/default.aspx?lat=6&lng=9')
        for line in page:
            if line.startswith('var uvtoken'):
                self.user_token = re.compile("userToken[ =]+'([^']+)'").search(line).group(1)
                page.close()
                return

        raise Exception('Website contents unexpected. Please check connection.')

    def _parse_overview(self, content, location, rec_depth=0):
        (c1, c2) = location
        full = json.loads(content)
        a = json.loads(full['d'])
        points = []
        if 'cc' not in a['cs']:
            if 'count' in a['cs'] and 'count' != 0:
                mlat = (c1.lat + c2.lat) / 2
                nc1 = geo.Coordinate(min(c1.lat, c2.lat), min(c1.lon, c2.lon))
                mc1 = geo.Coordinate(mlat, max(c1.lon, c2.lon))
                mc2 = geo.Coordinate(mlat, min(c1.lon, c2.lon))
                nc2 = geo.Coordinate(max(c1.lat, c2.lat), max(c1.lon, c2.lon))
                CacheDownloader.lock.release()
                points += self.get_geocaches((nc1, mc1), rec_depth + 1)
                points += self.get_geocaches((mc2, nc2), rec_depth + 1)
                CacheDownloader.lock.acquire(False)
            return points
        for b in a['cs']['cc']:
            c = GeocacheCoordinate(b['lat'], b['lon'], b['gc'])
            c.title = b['nn']
            if b['ctid'] in self.CTIDS:
                c.type = self.CTIDS[b['ctid']]
            else:
                c.type = GeocacheCoordinate.TYPE_UNKNOWN
            c.found = b['f']
            if not b['ia']:
                c.status = GeocacheCoordinate.STATUS_DISABLED
            points.append(c)

        return points

    def _get_cache_page(self, cacheid):
        return self.downloader.get_reader('http://www.geocaching.com/seek/cache_details.aspx?wp=%s' % cacheid)

    def _parse_cache_page(self, cache_page, coordinate):
        section = ''
        prev_section = ''
        shortdesc = desc = coords = hints = waypoints = images = logs = owner = head = ''
        logger.debug('Start parsing...')
        for line in cache_page:
            line = line.strip()
            if section == '' and line.startswith('<meta name="og:site_name" '):
                section = 'head'
            elif section == 'head' and line.startswith('<form name="aspnetForm"'):
                section = 'after-head'
            elif section == 'after-head' and line.startswith('<a id="ctl00_ContentBody_lnkConversions"'):
                coords = line
            elif section == 'after-head' and line.startswith('<span id="ctl00_ContentBody_ShortDescription">'):
                section = 'shortdesc'
            elif (section == 'after-head' or section == 'shortdesc') and line.startswith('<span id="ctl00_ContentBody_LongDescription">'):
                section = 'desc'
            elif (section == 'desc' or section == 'shortdesc') and line.startswith('Additional Hints'):
                section = 'after-desc'
            elif section == 'after-desc' and line.startswith('<div id="div_hint" class="HalfLeft">'):
                section = 'hints'
            elif section == 'hints' and line.startswith("<div id='dk'"):
                section = 'after-hints'
            elif (section == 'after-hints' or section == 'after-desc') and line.startswith('<div class="CacheDetailNavigationWidget">'):
                section = 'pre-waypoints'
            elif section == 'pre-waypoints' and line.startswith('<table class="Table" id="ctl00_ContentBody_Waypoints">'):
                section = 'waypoints'
            elif section == 'waypoints' and line.startswith('</tbody> </table>'):
                section = 'after-waypoints'
            elif (section == 'pre-waypoints' or section == 'after-waypoints') and line.startswith('<span id="ctl00_ContentBody_Images">'):
                section = 'images'
            elif section == 'images' and line.startswith('<table class="LogsTable'):
                section = 'logs'
            if section != prev_section:
                logger.debug("Now in Section '%s', with line %s" % (section, line[:20:]))
            prev_section = section
            if section == 'head':
                head = '%s%s\n' % (head, line)
            elif section == 'shortdesc':
                shortdesc = '%s%s\n' % (shortdesc, line)
            elif section == 'desc':
                desc = '%s%s\n' % (desc, line)
            elif section == 'hints':
                hints = '%s%s ' % (hints, line)
            elif section == 'waypoints':
                waypoints = '%s%s  ' % (waypoints, line)
            elif section == 'images':
                images = '%s%s ' % (images, line)
            elif section == 'logs':
                logs = '%s%s' % (logs, line)
                if line.endswith('</tr></table>'):
                    break

        logger.debug('finished parsing, converting...')
        head = unicode(head, 'utf-8', errors='ignore')
        shortdesc = unicode(shortdesc, 'utf-8', errors='ignore')
        hints = unicode(hints, 'utf-8', errors='ignore')
        waypoints = unicode(waypoints, 'utf-8', errors='ignore')
        logs = unicode(logs, 'utf-8', errors='ignore')
        images = unicode(images, 'utf-8', errors='ignore')
        logger.debug('finished converting, reading...')
        (coordinate.size, coordinate.difficulty, coordinate.terrain, coordinate.owner, coordinate.lat, coordinate.lon) = self.__parse_head(head, coords)
        coordinate.shortdesc = self.__treat_shortdesc(shortdesc)
        coordinate.desc = self.__treat_desc(desc)
        coordinate.hints = self.__treat_hints(hints)
        coordinate.set_waypoints(self.__treat_waypoints(waypoints))
        coordinate.set_logs(self.__treat_logs(logs))
        self.__treat_images(images)
        coordinate.set_images(self.images)
        logger.debug('finished reading.')
        return coordinate

    def __parse_head(self, head, coords):
        size_diff_terr = re.compile('was created by (?P<owner>.+?) on .+? a (?P<size>[a-zA-Z ]+) size geocache, with difficulty of (?P<diff>[0-9.]+?), terrain of (?P<terr>[0-9.]+?). ').search(head)
        sizestring = size_diff_terr.group('size').lower()
        if sizestring == 'micro':
            size = 1
        elif sizestring == 'small':
            size = 2
        elif sizestring == 'regular':
            size = 3
        elif sizestring == 'large' or sizestring == 'big':
            size = 4
        elif sizestring == 'not chosen' or sizestring == 'other':
            size = 5
        else:
            logger.warning('Size not known: %s' % sizestring)
            size = 5
        diff = float(size_diff_terr.group('diff')) * 10
        terr = float(size_diff_terr.group('terr')) * 10
        owner = HTMLManipulations._decode_htmlentities(size_diff_terr.group('owner'))
        coords = re.compile('lat=([0-9.-]+)&amp;lon=([0-9.-]+)&amp;').search(coords)
        lat = float(coords.group(1))
        lon = float(coords.group(2))
        return (
         size, diff, terr, owner, lat, lon)

    def __treat_hints(self, hints):
        hints = HTMLManipulations._strip_html(HTMLManipulations._replace_br(hints)).strip()
        hints = self._rot13(hints)
        hints = re.sub('\\[([^\\]]+)\\]', lambda match: self._rot13(match.group(0)), hints)
        hints = hints.replace('&aofc;', '').strip()
        return hints

    def __treat_desc(self, desc):
        desc = self.__treat_html(desc.rsplit('\n', 5)[0])
        return desc.strip()

    def __treat_shortdesc(self, desc):
        if desc.strip() == '':
            return ''
        desc = self.__treat_html(desc.rsplit('\n', 3)[0])
        return desc

    def __treat_html(self, html):
        html = HTMLManipulations.COMMENT_REGEX.sub('', html)
        html = self.__replace_images(html)
        return html

    @staticmethod
    def __from_dm(direction, decimal, minutes):
        if direction == None or decimal == None or minutes == None:
            return -1
        else:
            if direction in 'SsWw':
                sign = -1
            else:
                sign = 1
            return (float(decimal) + float(minutes) / 60.0) * sign

    def __treat_waypoints(self, data):
        logger.debug('Waypoints: %s' % data)
        data.replace('</td>', '')
        data.replace('</tr>', '')
        lines = data.split('<tr')
        waypoints = []
        for line in lines:
            tds = re.split('<td[^>]*>', line)
            logger.debug('TDs: %s' % repr(tds))
            if len(tds) <= 1:
                continue
            elif len(tds) > 4:
                id = ('').join(HTMLManipulations._strip_html(x).strip() for x in tds[4:6])
                name = HTMLManipulations._decode_htmlentities(HTMLManipulations._strip_html(tds[6])).strip()
                m = re.compile('(\\?\\?\\?|(?P<lat_sign>N|S) (?P<lat_d>\\d+)° (?P<lat_m>[0-9\\.]+) (?P<lon_sign>E|W) (?P<lon_d>\\d+)° (?P<lon_m>[0-9\\.]+))').search(tds[7])
                lat = self.__from_dm(m.group('lat_sign'), m.group('lat_d'), m.group('lat_m'))
                lon = self.__from_dm(m.group('lon_sign'), m.group('lon_d'), m.group('lon_m'))
            else:
                comment = HTMLManipulations._decode_htmlentities(HTMLManipulations._strip_html(HTMLManipulations._replace_br(tds[3]))).strip()
                waypoints.append({'lat': lat, 'lon': lon, 'id': id, 'name': name, 'comment': comment})

        return waypoints

    def __treat_images(self, data):
        finder = re.finditer('<a href="([^"]+)" rel="lightbox" class="lnk"><img src="/images/stockholm/16x16/images.gif" />(.+?)</a><br /><br />', data)
        for m in finder:
            if m.group(1) == None:
                continue
            id = self._download_image(url=m.group(1))
            if id != None:
                self.__add_image(id, HTMLManipulations._decode_htmlentities(HTMLManipulations._strip_html(m.group(2))))

        return

    def __treat_logs(self, logs):
        lines = logs.split('<tr>')
        output = []
        for l in lines:
            m = re.match('<td[^>]+><strong><img src="http://www\\.geocaching\\.com/images/icons/(?:icon_(?P<icon>[a-z]+)|(?P<icon2>coord_update))\\.gif"[^>]*/>' + '&nbsp;(?P<month>[^ ]+) (?P<day>\\d+)(, (?P<year>\\d+))? by <a[^>]+>(?P<finder>[^<]+)</a></strong>&nbsp;\\(\\d+ found\\)<br ?/><br ?/>(?P<text>.+)' + '<br ?/><br ?/><small>', l, re.DOTALL)
            if m == None:
                logger.debug('Ignoring following log line:-----\n%s\n------' % l)
            else:
                type = m.group('icon') if m.group('icon') != None else m.group('icon2')
                month = self.__month_to_number(m.group('month'))
                day = m.group('day')
                year = m.group('year')
                if year == '' or year == None:
                    year = datetime.datetime.now().year
                finder = m.group('finder')
                text = HTMLManipulations._decode_htmlentities(HTMLManipulations._strip_html(HTMLManipulations._replace_br(m.group('text')), True))
                output.append(dict(type=type, month=month, day=day, year=year, finder=finder, text=text))

        return output

    def __replace_images(self, data):
        return re.sub('(?is)(<img[^>]+src=\\n?["\']?)([^ >"\']+)([^>]+?/?>)', self.__replace_image_callback, data)

    def __replace_image_callback(self, m):
        url = m.group(2)
        if not url.startswith('http://'):
            return m.group(0)
        else:
            id = self._download_image(url)
            if id == None:
                return m.group(0)
            self.__add_image(id)
            return '[[img:%s]]' % id
            return

    def __add_image(self, id, description=''):
        if id in self.images and len(description) > len(self.images[id]) or id not in self.images:
            self.images[id] = description

    @staticmethod
    def __month_to_number(text):
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        if text in months:
            return months.index(text) + 1
        logger.warning('Unknown month: ' + text)
        return 0


if __name__ == '__main__':
    import sys, downloader
    outfile = None
    if len(sys.argv) == 2:
        print 'Reading from file %s' % sys.argv[1]
        inp = open(sys.argv[1])
        m = GeocacheCoordinate(0, 0, 'GC1N8G6')
        a = GeocachingComCacheDownloader(downloader.FileDownloader('dummy', 'dummy', '/tmp/cookies'), '/tmp/', True)
    else:
        (name, password) = sys.argv[1:3]
        a = GeocachingComCacheDownloader(downloader.FileDownloader(name, password, '/tmp/cookies', GeocachingComCacheDownloader.login_callback(name, password)), '/tmp/', True)
        print 'Using Username %s' % name

        def pcache(c):
            print "--------------------\nName: '%s'\nTitle: '%s'\nType: %s" % (c.name, c.title, c.type)


        coords = a.get_geocaches((geo.Coordinate(49.3513, 6.583), geo.Coordinate(49.352, 6.584)))
        print '# Found %d coordinates' % len(coords)
        for x in coords:
            pcache(x)
            if x.name == 'GC1N8G6':
                if x.type != GeocacheCoordinate.TYPE_REGULAR or x.title != 'Druidenpfad':
                    print '# Wrong type or title'
                    sys.exit()
                m = x
                break
        else:
            print "# Didn't find my own geocache :-("

        if len(sys.argv) == 4:
            print 'Writing to File %s' % sys.argv[3]
            outfile = sys.argv[3]
    res = a.update_coordinate(m, outfile)
    print res
    c = res
    if c.owner != 'webhamster':
        print "Owner doesn't match ('%s', expected webhamster)" % c.owner
    if c.title != 'Druidenpfad':
        print "Title doesn't match ('%s', expected 'Druidenpfad')" % c.title
    if c.get_terrain() != '3.0':
        print "Terrain doesn't match (%s, expected 3.0) " % c.get_terrain()
    if c.get_difficulty() != '2.0':
        print "Diff. doesn't match (%s, expected 2.0)" % c.get_difficulty()
    if len(c.desc) != 1980:
        print "Length of text doesn't match (%d, expected %d" % (len(c.desc), 1980)
    if len(c.shortdesc) != 238:
        print "Length of short description doesn't match (%d, expected %d" % (len(c.shortdesc), 238)
    if len(c.get_waypoints()) != 4:
        print 'Expected 4 waypoints, got %d' % len(c.get_waypoints())
    if len(c.hints) != 83:
        print 'Expected 83 characters of hints, got %d' % len(c.hints)
    if len(c.get_logs()) < 2:
        print 'Expected at least 2 logs, got %d' % len(c.get_logs())
    print c.get_logs()
    print 'Owner:%s\nTitle:%s\nTerrain:%s\nDifficulty:%s\nDescription:%s\nShortdesc:%s\nHints:%s' % (c.owner, c.title, c.get_terrain(), c.get_difficulty(), c.desc, c.shortdesc, c.hints)
    print c.get_waypoints()