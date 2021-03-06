# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/actors/tts.py
# Compiled at: 2011-04-23 08:43:29
import subprocess, logging, gobject
logger = logging.getLogger('tts')

class TTS(gobject.GObject):
    MIN_DISTANCE = 20
    MAX_INTERVAL_DISTANCE = 1000
    MIN_INTERVAL = 5
    MAX_INTERVAL = 50
    DEFAULT_INTERVAL = 10
    __gsignals__ = {'error': (
               gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))}

    def __init__(self, core):
        gobject.GObject.__init__(self)
        self.gps_target_bearing_abs = None
        self.gps_target_distance = None
        self.gps_data = None
        self.proc = None
        self.timeout_event_id = None
        self.automatic_interval = False
        core.connect('good-fix', self.__on_good_fix)
        core.connect('no-fix', self.__on_no_fix)
        core.connect('settings-changed', self.__on_settings_changed)
        return

    def __on_settings_changed(self, caller, settings, source):
        if 'tts_interval' in settings:
            self.__set_enabled(settings['tts_interval'])

    def __set_enabled(self, interval):
        if interval == -1:
            interval = self.__calculate_automatic_interval(self.gps_target_distance)
            self.automatic_interval = True
            logger.info('Setting interval to %d' % interval)
        else:
            self.automatic_interval = False
        if self.timeout_event_id != None:
            gobject.source_remove(self.timeout_event_id)
            self.timeout_event_id = None
        if interval > 0:
            self.timeout_event_id = gobject.timeout_add_seconds(interval, self.__tell)
            self.__connect()
        else:
            self.__disconnect()
        return

    @staticmethod
    def __calculate_automatic_interval(d):
        if d == None:
            return TTS.DEFAULT_INTERVAL
        else:
            if d > TTS.MAX_INTERVAL_DISTANCE:
                return TTS.MAX_INTERVAL
            else:
                if d <= TTS.MIN_DISTANCE:
                    return TTS.MIN_INTERVAL
                return int(round(TTS.MAX_INTERVAL + (TTS.MAX_INTERVAL_DISTANCE - d) * (float(TTS.MIN_INTERVAL - TTS.MAX_INTERVAL) / float(TTS.MAX_INTERVAL_DISTANCE - TTS.MIN_DISTANCE))))
            return

    def __connect(self):
        if self.proc != None:
            return
        else:
            logger.info('Starting espeak...')
            try:
                self.proc = subprocess.Popen('espeak', stdin=subprocess.PIPE)
                self.proc.stdin.write('Espeak ready.\n')
            except:
                self.proc = None
                self.emit('error', Exception("Please install the 'espeak' package from the package manager to get text-to-speech functionality."))

            return

    def __disconnect(self):
        logger.info('Stopping espeak...')
        if self.proc != None:
            self.proc.stdin.write('Stopping espeak.\n')
            self.proc = None
        return

    def __on_good_fix(self, caller, gps_data, distance, bearing):
        self.gps_target_distance = distance
        self.gps_target_bearing_abs = bearing - gps_data.bearing
        self.gps_data = gps_data

    def __tell(self):
        output = '%s\n%s\n' % (self.__format_distance(), self.__format_bearing())
        logger.info('Espeak: %s' % repr(output.strip()))
        self.proc.stdin.write(output)
        if self.automatic_interval:
            self.__set_enabled(-1)
            return False
        return True

    def __format_distance(self):
        distance = self.gps_target_distance
        if distance == None:
            return 'No Fix. '
        else:
            if distance >= 1000:
                return '%d kilometers. ' % round(distance / 1000.0)
            else:
                if distance >= 10:
                    return '%d meters. ' % round(distance)
                return '%.1f meters. ' % round(distance, 1)
            return

    def __format_bearing(self):
        if self.gps_target_bearing_abs == None:
            return ''
        else:
            if self.gps_data == None or self.gps_data.error_bearing > 179:
                return ''
            return "%d o'clock." % self.__degree_to_hour(self.gps_target_bearing_abs)

    def __on_no_fix(self, caller, fix, msg):
        self.gps_target_distance = None
        self.gps_target_bearing_abs = None
        self.gps_data = None
        return

    @staticmethod
    def __degree_to_hour(degree):
        ret = round(degree % 360 / 30.0)
        if ret != 0:
            return ret
        return 12

    @staticmethod
    def test():
        print 'Testing of coordinate-to-hour conversion:'
        for i in xrange(360):
            print '%3d -> %d' % (i, TTS.__degree_to_hour(i))

        print
        print 'Testing of interval calculation:'
        for z in xrange(1050, 0, -3):
            print '%4d m -> %d seconds' % (z, TTS.__calculate_automatic_interval(z))


if __name__ == '__main__':
    TTS.test()