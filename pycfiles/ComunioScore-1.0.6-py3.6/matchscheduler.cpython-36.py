# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/matchscheduler.py
# Compiled at: 2020-05-01 18:27:16
# Size of source mod 2**32: 2036 bytes
import logging, datetime
from ComunioScore import Scheduler

class MatchScheduler:
    __doc__ = ' class MatchScheduler to schedule match events\n\n    USAGE:\n            matchscheduler = MatchScheduler()\n            matchscheduler.register_livedata_event_handler(func=livedata.fetch)\n            matchscheduler.new_event(time.time(), 2, 103388, "team1", "team2")\n    '
    livedata_event_handler = None

    def __init__(self):
        self.logger = logging.getLogger('ComunioScore')
        self.logger.info('Create class MatchScheduler')
        self.scheduler = Scheduler()
        self.new_events_allowed = True

    @classmethod
    def register_livedata_event_handler(cls, func):
        """ registers a new livedata event handler

        :param func: event handler for the livedata
        """
        cls.livedata_event_handler = func

    def new_event(self, event_ts, match_day, match_id, home_team, away_team):
        """ schedules a new match event with given match data

        """
        if self.livedata_event_handler:
            current_tasks_len = len(self.scheduler.get_tasks())
            if current_tasks_len == 9:
                self.new_events_allowed = False
            else:
                if current_tasks_len < 9:
                    if self.scheduler.is_tasks_empty():
                        self.new_events_allowed = True
            if current_tasks_len < 10:
                if self.new_events_allowed:
                    self.logger.info('Register new event {} for match day {}: {} vs. {}'.format(match_id, match_day, home_team, away_team))
                    event_ts = datetime.datetime.fromtimestamp(int(event_ts))
                    self.scheduler.schedule(self.livedata_event_handler, event_ts, match_day, match_id, home_team, away_team)
            self.logger.error('9 match events are scheduled already. Wait...')
        else:
            self.logger.error('No livedata_event_handler configured!')