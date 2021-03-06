# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/esalazar/git/teleceptor/teleceptor/whisperUtils.py
# Compiled at: 2014-09-04 23:45:49
"""
    (c) 2014 Visgence, Inc.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""
import whisper, os, errno
from time import time
PATH = os.path.abspath(os.path.dirname(__file__))
from teleceptor import WHISPER_DATA
from teleceptor import WHISPER_ARCHIVES

def createDs(uuid):
    archives = [ whisper.parseRetentionDef(retentionDef) for retentionDef in WHISPER_ARCHIVES ]
    dataFile = os.path.join(WHISPER_DATA, str(uuid) + '.wsp')
    try:
        os.makedirs(WHISPER_DATA)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    try:
        whisper.create(dataFile, archives, xFilesFactor=0.5, aggregationMethod='average')
    except whisper.WhisperException as exc:
        raise SystemExit('[ERROR] %s' % str(exc))


def insertReading(uuid, value, timestamp=None):
    dataFile = os.path.join(WHISPER_DATA, str(uuid) + '.wsp')
    try:
        whisper.update(dataFile, value, timestamp)
    except whisper.WhisperException as exc:
        raise SystemExit('[ERROR] %s' % str(exc))


def getReadings(uuid, start, end):
    assert time() - int(start) >= 60
    dataFile = os.path.join(WHISPER_DATA, str(uuid) + '.wsp')
    try:
        timeInfo, values = whisper.fetch(dataFile, start, end)
    except whisper.WhisperException as exc:
        raise SystemExit('[ERROR] %s' % str(exc))

    start, end, step = timeInfo
    data = []
    t = start
    for value in values:
        if value is not None:
            data.append((t, value))
        t += step

    return data