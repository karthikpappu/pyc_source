# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/subaligner/media_helper.py
# Compiled at: 2020-04-27 04:30:52
# Size of source mod 2**32: 12023 bytes
import subprocess, os
from pysrt import SubRipFile
from decimal import Decimal
from .embedder import FeatureEmbedder
from .exception import TerminalException
from .logger import Logger

class MediaHelper(object):
    __doc__ = ' Utility for processing media assets including audio, video and\n    subtitle files.\n    '
    AUDIO_FILE_EXTENSION = [
     '.wav', '.aac']
    _MediaHelper__LOGGER = Logger().get_logger(__name__)
    _MediaHelper__MIN_SECS_PER_WORD = 0.414
    _MediaHelper__MIN_GAP_IN_SECS = 1
    _MediaHelper__CMD_TIME_OUT = 600

    @staticmethod
    def extract_audio(video_file_path, decompress=False, freq=16000):
        """Extract audio track from the video file and save it to a WAV file.

        Arguments:
            video_file_path {string} -- The input video file path.
        Keyword Arguments:
            decompress {bool} -- Extract WAV if True otherwise extract AAC (default: {False}).
            freq {int} -- The audio sample frequency (default: {16000}).
        Returns:
            string -- The file path of the extracted audio.
        """
        root, extension = os.path.splitext(video_file_path)
        if decompress:
            assert freq is not None, 'Frequency is needed for decompression'
            audio_file_path = '{0}{1}{2}'.format(root, extension, MediaHelper.AUDIO_FILE_EXTENSION[0])
        else:
            audio_file_path = '{0}{1}{2}'.format(root, extension, MediaHelper.AUDIO_FILE_EXTENSION[1])
        command = 'ffmpeg -y -xerror -i {0}{1} -ac 2 -ar {2} -vn {3}'.format(root, extension, freq, audio_file_path) if decompress else 'ffmpeg -y -xerror -i {0}{1} -vn -acodec copy {2}'.format(root, extension, audio_file_path)
        MediaHelper._MediaHelper__LOGGER.debug('Running: {}'.format(command))
        with subprocess.Popen((command.split()),
          shell=False,
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE),
          close_fds=True) as (process):
            try:
                try:
                    _, std_err = process.communicate(timeout=(MediaHelper._MediaHelper__CMD_TIME_OUT))
                    MediaHelper._MediaHelper__LOGGER.debug(std_err.decode('utf-8').strip())
                    if process.returncode != 0:
                        raise TerminalException('Cannot extract audio from video: {}'.format(video_file_path))
                except subprocess.TimeoutExpired as te:
                    try:
                        process.kill()
                        process.wait()
                        if os.path.exists(audio_file_path):
                            os.remove(audio_file_path)
                        raise TerminalException('Timeout on extracting audio from video: {}'.format(video_file_path)) from te
                    finally:
                        te = None
                        del te

                except Exception as e:
                    try:
                        process.kill()
                        process.wait()
                        if os.path.exists(audio_file_path):
                            os.remove(audio_file_path)
                        elif isinstance(e, TerminalException):
                            raise e
                        else:
                            raise TerminalException('Cannot extract audio from video: {}'.format(video_file_path)) from e
                    finally:
                        e = None
                        del e

            finally:
                os.system('stty sane')

        MediaHelper._MediaHelper__LOGGER.info('Extracted audio file:{}'.format(audio_file_path))
        return audio_file_path

    @staticmethod
    def get_duration_in_seconds(start, end):
        """Get the duration in seconds between a start time and an end time.

        Arguments:
            start {string} -- The start time (e.g., 00:00:00,750).
            end {string} -- The end time (e.g., 00:00:10,230).

        Returns:
            float -- The duration in seconds.
        """
        if start is None:
            start = '00:00:00,000'
        if end is None:
            return
        start = start.replace(',', '.')
        end = end.replace(',', '.')
        start_h, start_m, start_s = map(Decimal, start.split(':'))
        end_h, end_m, end_s = map(Decimal, end.split(':'))
        return float(end_h * 3600 + end_m * 60 + end_s - (start_h * 3600 + start_m * 60 + start_s))

    @staticmethod
    def extract_audio_from_start_to_end(audio_file_path, start, end=None):
        """Extract audio based on the start time and the end time and save it to a temporary file.

        Arguments:
            audio_file_path {string} -- The path of the audio file.
            start {string} -- The start time (e.g., 00:00:00,750).

        Keyword Arguments:
            end {string} -- The end time (e.g., 00:00:10,230) (default: {None}).

        Returns:
            tuple -- The file path to the extracted audio and its duration.
        """
        segement_duration = MediaHelper.get_duration_in_seconds(start, end)
        root, extension = os.path.splitext(audio_file_path)
        start = start.replace(',', '.')
        if end is not None:
            end = end.replace(',', '.')
        else:
            segment_path = '{0}_{1}_{2}{3}'.format(root, str(start), str(end), extension)
            if end is not None:
                command = 'ffmpeg -y -xerror -i {0} -ss {1} -to {2} -acodec copy {3}'.format(audio_file_path, start, end, segment_path)
            else:
                command = 'ffmpeg -y -xerror -i {0} -ss {1} -acodec copy {2}'.format(audio_file_path, start, segment_path)
        MediaHelper._MediaHelper__LOGGER.debug('Running: {}'.format(command))
        with subprocess.Popen((command.split()),
          shell=False,
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE),
          close_fds=True) as (process):
            try:
                try:
                    _, std_err = process.communicate(timeout=(MediaHelper._MediaHelper__CMD_TIME_OUT))
                    MediaHelper._MediaHelper__LOGGER.debug(std_err.decode('utf-8').strip())
                    if process.returncode != 0:
                        raise TerminalException('Cannot extract audio from audio: {}'.format(audio_file_path))
                except subprocess.TimeoutExpired as te:
                    try:
                        process.kill()
                        process.wait()
                        if os.path.exists(segment_path):
                            os.remove(segment_path)
                        raise TerminalException('Timeout on extracting audio from audio: {}'.format(audio_file_path)) from te
                    finally:
                        te = None
                        del te

                except Exception as e:
                    try:
                        process.kill()
                        process.wait()
                        if os.path.exists(segment_path):
                            os.remove(segment_path)
                        elif isinstance(e, TerminalException):
                            raise e
                        else:
                            raise TerminalException('Cannot extract audio from audio: {}'.format(audio_file_path)) from e
                    finally:
                        e = None
                        del e

            finally:
                os.system('stty sane')

        MediaHelper._MediaHelper__LOGGER.info('Extracted audio segment:{}'.format(segment_path))
        return (segment_path, segement_duration)

    @staticmethod
    def get_audio_segment_starts_and_ends(subs):
        """Group subtitle cues into larger segments in terms of silence gaps.

        Arguments:
            subs {list} -- A list of SupRip cues.

        Returns:
            tuple -- A list of start times, a list of end times and a list of grouped SubRip files.
        """
        segment_starts = []
        segment_ends = []
        combined = []
        new_subs = []
        current_start = str(subs[0].start)
        for i in range(len(subs)):
            if i != 0:
                if subs[i].start < subs[(i - 1)].end:
                    continue
            else:
                if i == len(subs) - 1:
                    combined.append(subs[i])
                    segment_starts.append(current_start)
                    segment_ends.append(str(subs[i].end))
                    new_subs.append(SubRipFile(combined))
                    del combined[:]
            duration = FeatureEmbedder.time_to_sec(subs[i].end) - FeatureEmbedder.time_to_sec(subs[i].start)
            if duration < MediaHelper._MediaHelper__MIN_SECS_PER_WORD:
                combined.append(subs[i])
                continue
            gap = FeatureEmbedder.time_to_sec(subs[(i + 1)].start) - FeatureEmbedder.time_to_sec(subs[i].end)
            if not subs[i].end == subs[(i + 1)].start:
                if gap < MediaHelper._MediaHelper__MIN_GAP_IN_SECS:
                    combined.append(subs[i])
                    continue
                combined.append(subs[i])
                segment_starts.append(current_start)
                segment_ends.append(str(subs[i].end))
                current_start = str(subs[i].end)
                new_subs.append(SubRipFile(combined))
                del combined[:]

        return (
         segment_starts, segment_ends, new_subs)

    @staticmethod
    def get_frame_rate(video_file_path):
        """Extract audio track from the video file and save it to a WAV file.

        Arguments:
            video_file_path {string} -- The input video file path.
        Returns:
            float -- The frame rate
        """
        with subprocess.Popen(('ffmpeg -i {} -f null /dev/null'.format(video_file_path).split()),
          shell=False,
          stderr=(subprocess.PIPE)) as (proc):
            with subprocess.Popen([
             'sed', '-n', 's/.*, \\(.*\\) fp.*/\\1/p'],
              shell=False,
              stdin=(proc.stderr),
              stdout=(subprocess.PIPE),
              stderr=(subprocess.PIPE)) as (process):
                try:
                    try:
                        std_out, std_err = process.communicate(timeout=(MediaHelper._MediaHelper__CMD_TIME_OUT))
                        if process.returncode != 0:
                            raise TerminalException('Cannot extract the frame rate from video: {}'.format(video_file_path))
                        fps = float(std_out.decode('utf-8').split('\n')[0])
                    except subprocess.TimeoutExpired as te:
                        try:
                            proc.kill()
                            proc.wait()
                            process.kill()
                            process.wait()
                            raise TerminalException('Timeout on extracting the frame rate from video: {}'.format(video_file_path)) from te
                        finally:
                            te = None
                            del te

                    except Exception as e:
                        try:
                            proc.kill()
                            proc.wait()
                            process.kill()
                            process.wait()
                            if isinstance(e, TerminalException):
                                raise e
                            else:
                                raise TerminalException('Cannot extract the frame rate from video: {}'.format(video_file_path)) from e
                        finally:
                            e = None
                            del e

                finally:
                    os.system('stty sane')

        MediaHelper._MediaHelper__LOGGER.info('Extracted frame rate:{} fps'.format(fps))
        return fps