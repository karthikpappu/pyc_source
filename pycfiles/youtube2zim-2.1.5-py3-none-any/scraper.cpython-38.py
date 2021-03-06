# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/youtube/youtube2zim/scraper.py
# Compiled at: 2020-04-23 05:40:03
# Size of source mod 2**32: 34859 bytes
"""
    create project on Google Developer console
    Add Youtube Data API v3 to it
    Create credentials (Other non-UI, Public Data)
"""
import os, json, locale, shutil, datetime, functools
from pathlib import Path
import concurrent.futures
from gettext import gettext as _
import jinja2, youtube_dl
from pif import get_public_ip
from babel.dates import format_date
from dateutil import parser as dt_parser
from kiwixstorage import KiwixStorage
from zimscraperlib.download import save_file
from zimscraperlib.zim import ZimInfo, make_zim_file
from zimscraperlib.fix_ogvjs_dist import fix_source_dir
from zimscraperlib.imaging import resize_image, get_colors, is_hex_color
from zimscraperlib.i18n import get_language_details, setlocale
from .youtube import get_channel_json, credentials_ok, Playlist, get_channel_playlists_json, get_videos_json, get_videos_authors_info, save_channel_branding, skip_deleted_videos, skip_outofrange_videos
from .converter import post_process_video
from .utils import clean_text, load_json, save_json, get_slug
from .constants import logger, ROOT_DIR, CHANNEL, PLAYLIST, USER, SCRAPER, ENCODER_VERSION

class Youtube2Zim(object):

    def __init__(self, collection_type, youtube_id, api_key, video_format, low_quality, nb_videos_per_page, all_subtitles, autoplay, output_dir, no_zim, fname, debug, keep_build_dir, skip_download, max_concurrency, youtube_store, language, locale_name, tags, dateafter, use_any_optimized_version, s3_url_with_credentials, title=None, description=None, creator=None, publisher=None, name=None, profile_image=None, banner_image=None, main_color=None, secondary_color=None, only_test_branding=None):
        self.collection_type = collection_type
        self.youtube_id = youtube_id
        self.api_key = api_key
        self.dateafter = dateafter
        self.video_format = video_format
        self.low_quality = low_quality
        self.nb_videos_per_page = nb_videos_per_page
        self.all_subtitles = all_subtitles
        self.autoplay = autoplay
        self.fname = fname
        self.language = language
        self.tags = [t.strip() for t in tags.split(',')]
        self.title = title
        self.description = description
        self.creator = creator
        self.publisher = publisher
        self.name = name
        self.profile_image = profile_image
        self.banner_image = banner_image
        self.main_color = main_color
        self.secondary_color = secondary_color
        self.output_dir = Path(output_dir).expanduser().resolve()
        self.playlists = []
        self.uploads_playlist_id = None
        self.videos_ids = []
        self.main_channel_id = None
        self.only_test_branding = only_test_branding
        self.no_zim = no_zim
        self.debug = debug
        self.keep_build_dir = keep_build_dir
        self.skip_download = skip_download
        self.max_concurrency = max_concurrency
        self.build_dir = self.output_dir.joinpath('build')
        self.zim_info = ZimInfo(language=language,
          tags=tags,
          title=title,
          description=description,
          creator=creator,
          publisher=publisher,
          name=name,
          scraper=SCRAPER,
          favicon='favicon.jpg')
        youtube_store.update(build_dir=(self.build_dir),
          api_key=(self.api_key),
          cache_dir=(self.cache_dir))
        self.s3_url_with_credentials = s3_url_with_credentials
        self.use_any_optimized_version = use_any_optimized_version
        self.video_quality = 'low' if self.low_quality else 'high'
        self.s3_storage = None
        locale_name = locale_name or get_language_details(self.language)['iso-639-1']
        try:
            self.locale = setlocale(ROOT_DIR, locale_name)
        except locale.Error:
            logger.error(f"No locale for {locale_name}. Use --locale to specify it. defaulting to en_US")
            self.locale = setlocale(ROOT_DIR, 'en')

    @property
    def root_dir(self):
        return ROOT_DIR

    @property
    def templates_dir(self):
        return self.root_dir.joinpath('templates')

    @property
    def assets_src_dir(self):
        return self.templates_dir.joinpath('assets')

    @property
    def assets_dir(self):
        return self.build_dir.joinpath('assets')

    @property
    def channels_dir(self):
        return self.build_dir.joinpath('channels')

    @property
    def cache_dir(self):
        return self.build_dir.joinpath('cache')

    @property
    def videos_dir(self):
        return self.build_dir.joinpath('videos')

    @property
    def profile_path(self):
        return self.build_dir.joinpath('profile.jpg')

    @property
    def banner_path(self):
        return self.build_dir.joinpath('banner.jpg')

    @property
    def is_user(self):
        return self.collection_type == USER

    @property
    def is_channel(self):
        return self.collection_type == CHANNEL

    @property
    def is_playlist(self):
        return self.collection_type == PLAYLIST

    @property
    def is_single_channel(self):
        if self.is_channel or self.is_user:
            return True
        return len(list(set([pl.creator_id for pl in self.playlists]))) == 1

    @property
    def sorted_playlists(self):
        """ sorted list of playlists (by title) but with Uploads one at first if any """
        if len(self.playlists) < 2:
            return self.playlists
        sorted_playlists = sorted((self.playlists), key=(lambda x: x.title))
        index = 0
        if self.uploads_playlist_id:
            try:
                index = [index for index, p in enumerate(sorted_playlists) if p.playlist_id == self.uploads_playlist_id][(-1)]
            except Exception:
                index = 0

        return [
         sorted_playlists[index]] + sorted_playlists[0:index] + sorted_playlists[index + 1:]

    def run(self):
        """ execute the scraper step by step """
        self.validate_dateafter_input()
        logger.info(f"starting youtube scraper for {self.collection_type}#{self.youtube_id}")
        logger.info('preparing build folder at {}'.format(self.build_dir.resolve()))
        if not self.keep_build_dir:
            if self.build_dir.exists():
                shutil.rmtree((self.cache_dir), ignore_errors=True)
                shutil.rmtree(self.build_dir)
        self.make_build_folder()
        logger.info('testing Youtube credentials')
        if not credentials_ok():
            raise ValueError('Unable to connect to Youtube API v3. check `API_KEY`.')
        if self.s3_url_with_credentials:
            if not self.s3_credentials_ok():
                raise ValueError('Unable to connect to Optimization Cache. Check its URL.')
        self.check_branding_values()
        logger.info('compute playlists list to retrieve')
        self.extract_playlists()
        logger.info('.. {} playlists:\n   {}'.format(len(self.playlists), '\n   '.join([p.playlist_id for p in self.playlists])))
        if self.only_test_branding:
            logger.info('update general metadata')
            self.update_metadata()
            logger.info('building fake homepage with branding')
            self.make_test_html_file()
            logger.info('done.')
            return None
        logger.info('compute list of videos')
        self.extract_videos_list()
        nb_videos_msg = f".. {len(self.videos_ids)} videos"
        if self.dateafter.start.year != 1:
            nb_videos_msg += f" in date range: {self.dateafter.start} - {datetime.date.today()}"
        logger.info(f"{nb_videos_msg}.")
        logger.info(f"downloading all videos, subtitles and thumbnails (concurrency={self.max_concurrency})")
        logger.info(f"  format: {self.video_format}")
        logger.info(f"  quality: {self.video_quality}")
        logger.info(f"  generated-subtitles: {self.all_subtitles}")
        if self.s3_storage:
            logger.info(f"  using cache: {self.s3_storage.url.netloc} with bucket: {self.s3_storage.bucket_name}")
        succeeded, failed = self.skip_download or self.download_video_files(max_concurrency=(self.max_concurrency))
        if failed:
            logger.error(f"{len(failed)} video(s) failed to download: {failed}")
            if len(failed) >= len(succeeded):
                logger.critical('More than half of videos failed. exiting')
                raise IOError('Too much videos failed to download')
        logger.info('retrieve channel-info for all videos (author details)')
        get_videos_authors_info(succeeded)
        logger.info("download all author's profile pictures")
        self.download_authors_branding()
        logger.info('update general metadata')
        self.update_metadata()
        logger.info('creating HTML files')
        self.make_html_files(succeeded)
        period = self.no_zim or datetime.datetime.now().strftime('%Y-%m')
        self.fname = Path(self.fname if self.fname else f"{self.name}_{period}.zim")
        logger.info('building ZIM file')
        print(self.zim_info.to_zimwriterfs_args())
        make_zim_file(self.build_dir, self.output_dir, self.fname, self.zim_info)
        logger.info('removing HTML folder')
        if not self.keep_build_dir:
            shutil.rmtree((self.build_dir), ignore_errors=True)
        logger.info('all done!')

    def s3_credentials_ok(self):
        logger.info('testing S3 Optimization Cache credentials')
        self.s3_storage = KiwixStorage(self.s3_url_with_credentials)
        if not self.s3_storage.check_credentials(list_buckets=True,
          bucket=True,
          write=True,
          read=True,
          failsafe=True):
            logger.error('S3 cache connection error testing permissions.')
            logger.error(f"  Server: {self.s3_storage.url.netloc}")
            logger.error(f"  Bucket: {self.s3_storage.bucket_name}")
            logger.error(f"  Key ID: {self.s3_storage.params.get('keyid')}")
            logger.error(f"  Public IP: {get_public_ip()}")
            return False
        return True

    def validate_dateafter_input(self):
        try:
            self.dateafter = youtube_dl.DateRange(self.dateafter)
        except Exception as exc:
            try:
                logger.error('Invalid dateafter input. Valid dateafter format: YYYYMMDD or (now|today)[+-][0-9](day|week|month|year)(s).')
                raise ValueError(f"Invalid dateafter input: {exc}")
            finally:
                exc = None
                del exc

    def make_build_folder(self):
        """ prepare build folder before we start downloading data """
        os.makedirs((self.build_dir), exist_ok=True)
        if self.assets_dir.exists():
            shutil.rmtree(self.assets_dir)
        shutil.copytree(self.assets_src_dir, self.assets_dir)
        fix_source_dir(self.assets_dir, 'assets')
        self.cache_dir.mkdir(exist_ok=True)
        self.videos_dir.mkdir(exist_ok=True)
        self.channels_dir.mkdir(exist_ok=True)

    def check_branding_values(self):
        """ checks that user-supplied images and colors are valid (so to fail early)

            Images are checked for existence or downloaded then resized
            Colors are check for validity """
        if not sum([bool(x) for x in (
         self.profile_image,
         self.banner_image,
         self.main_color,
         self.secondary_color)]):
            return
            logger.info('checking your branding files and values')
            if self.profile_image:
                if self.profile_image.startswith('http'):
                    save_file(self.profile_image, self.profile_path)
                else:
                    if not self.profile_image.exists():
                        raise IOError(f"--profile image could not be found: {self.profile_image}")
                    shutil.move(self.profile_image, self.profile_path)
                resize_image((self.profile_path), width=100, height=100, method='thumbnail')
            if self.banner_image:
                if self.banner_image.startswith('http'):
                    save_file(self.banner_image, self.banner_path)
                else:
                    if not self.banner_image.exists():
                        raise IOError(f"--banner image could not be found: {self.banner_image}")
                    shutil.move(self.banner_image, self.banner_path)
                resize_image((self.banner_path), width=1060, height=175, method='thumbnail')
        else:
            if self.main_color and not is_hex_color(self.main_color):
                raise ValueError(f"--main-color is not a valid hex color: {self.main_color}")
            if self.secondary_color and not is_hex_color(self.secondary_color):
                raise ValueError(f"--secondary_color-color is not a valid hex color: {self.secondary_color}")

    def extract_playlists(self):
        """ prepare a list of Playlist from user request

            USER: we fetch the hidden channel associate to it
            CHANNEL (and USER): we grab all playlists + `uploads` playlist
            PLAYLIST: we retrieve from the playlist Id(s) """
        if self.is_user or self.is_channel:
            if self.is_user:
                channel_json = get_channel_json((self.youtube_id), for_username=True)
            else:
                channel_json = get_channel_json(self.youtube_id)
            self.main_channel_id = channel_json['id']
            playlist_ids = [p['id'] for p in get_channel_playlists_json(self.main_channel_id)]
            playlist_ids += [
             channel_json['contentDetails']['relatedPlaylists']['uploads']]
            self.uploads_playlist_id = playlist_ids[(-1)]
        else:
            if self.is_playlist:
                playlist_ids = self.youtube_id.split(',')
                self.main_channel_id = Playlist.from_id(playlist_ids[0]).creator_id
            else:
                raise NotImplementedError('unsupported collection_type')
        self.playlists = [Playlist.from_id(playlist_id) for playlist_id in list(set(playlist_ids))]

    def extract_videos_list(self):
        all_videos = load_json(self.cache_dir, 'videos')
        if all_videos is None:
            all_videos = {}
            for playlist in self.playlists:
                videos_json = get_videos_json(playlist.playlist_id)
                skip_outofrange = functools.partial(skip_outofrange_videos, self.dateafter)
                filter_videos = filter(skip_outofrange, videos_json)
                filter_videos = filter(skip_deleted_videos, filter_videos)
                all_videos.update({v:v['contentDetails']['videoId'] for v in filter_videos})
            else:
                save_json(self.cache_dir, 'videos', all_videos)

        self.videos_ids = [
         *all_videos.keys()]

    def download_video_files(self, max_concurrency):
        audext, vidext = {'webm':('webm', 'webm'), 
         'mp4':('m4a', 'mp4')}[self.video_format]
        options = {'cachedir':self.videos_dir, 
         'writethumbnail':True, 
         'write_all_thumbnails':True, 
         'writesubtitles':True, 
         'allsubtitles':True, 
         'subtitlesformat':'vtt', 
         'keepvideo':False, 
         'ignoreerrors':False, 
         'retries':20, 
         'fragment-retries':50, 
         'skip-unavailable-fragments':True, 
         'outtmpl':str(self.videos_dir.joinpath('%(id)s', 'video.%(ext)s')), 
         'preferredcodec':self.video_format, 
         'format':f"best[ext={vidext}]/bestvideo[ext={vidext}]+bestaudio[ext={audext}]/best", 
         'y2z_video_format':self.video_format, 
         'y2z_low_quality':self.low_quality, 
         'y2z_videos_dir':self.videos_dir}
        if self.all_subtitles:
            options.update({'writeautomaticsub': True})
        nb_videos = len(self.videos_ids)
        concurrency = nb_videos if nb_videos < max_concurrency else max_concurrency
        if concurrency <= 1:
            return self.download_video_files_batch(options, self.videos_ids)

        def get_slot():
            n = 0
            while True:
                (yield n)
                n += 1
                if n >= concurrency:
                    n = 0

        batches = [[] for _ in range(0, concurrency)]
        slot = get_slot()
        for video_id in self.videos_ids:
            batches[next(slot)].append(video_id)
        else:
            overall_succeeded = []
            overall_failed = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as (executor):
                fs = [executor.submit(self.download_video_files_batch, options, videos_ids) for videos_ids in batches]
                done, not_done = concurrent.futures.wait(fs,
                  return_when=(concurrent.futures.ALL_COMPLETED))
                if not_done:
                    logger.critical('Not all video-processing batches completed. Cancelling…')
                    for future in not_done:
                        exc = future.exception()
                        if exc:
                            logger.exception(exc)
                            raise exc

                for future in done:
                    succeeded, failed = future.result()
                    overall_succeeded += succeeded
                    overall_failed += failed

            logger.debug(f"removing left-over files of {len(overall_failed)} failed videos")
            for video_id in overall_failed:
                shutil.rmtree((self.videos_dir.joinpath(video_id)), ignore_errors=True)
            else:
                return (
                 overall_succeeded, overall_failed)

    def download_from_cache--- This code section failed: ---

 L. 594         0  LOAD_FAST                'self'
                2  LOAD_ATTR                use_any_optimized_version
                4  POP_JUMP_IF_FALSE    30  'to 30'

 L. 595         6  LOAD_FAST                'self'
                8  LOAD_ATTR                s3_storage
               10  LOAD_METHOD              has_object
               12  LOAD_FAST                'key'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                s3_storage
               18  LOAD_ATTR                bucket_name
               20  CALL_METHOD_2         2  ''
               22  POP_JUMP_IF_TRUE     52  'to 52'

 L. 596        24  LOAD_CONST               False
               26  RETURN_VALUE     
               28  JUMP_FORWARD         52  'to 52'
             30_0  COME_FROM             4  '4'

 L. 598        30  LOAD_FAST                'self'
               32  LOAD_ATTR                s3_storage
               34  LOAD_ATTR                has_object_matching_meta

 L. 599        36  LOAD_FAST                'key'

 L. 599        38  LOAD_STR                 'encoder_version'

 L. 599        40  LOAD_GLOBAL              ENCODER_VERSION

 L. 598        42  LOAD_CONST               ('tag', 'value')
               44  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               46  POP_JUMP_IF_TRUE     52  'to 52'

 L. 601        48  LOAD_CONST               False
               50  RETURN_VALUE     
             52_0  COME_FROM            46  '46'
             52_1  COME_FROM            28  '28'
             52_2  COME_FROM            22  '22'

 L. 602        52  LOAD_FAST                'video_path'
               54  LOAD_ATTR                parent
               56  LOAD_ATTR                mkdir
               58  LOAD_CONST               True
               60  LOAD_CONST               True
               62  LOAD_CONST               ('parents', 'exist_ok')
               64  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               66  POP_TOP          

 L. 603        68  SETUP_FINALLY        88  'to 88'

 L. 604        70  LOAD_FAST                'self'
               72  LOAD_ATTR                s3_storage
               74  LOAD_METHOD              download_file
               76  LOAD_FAST                'key'
               78  LOAD_FAST                'video_path'
               80  CALL_METHOD_2         2  ''
               82  POP_TOP          
               84  POP_BLOCK        
               86  JUMP_FORWARD        148  'to 148'
             88_0  COME_FROM_FINALLY    68  '68'

 L. 605        88  DUP_TOP          
               90  LOAD_GLOBAL              Exception
               92  COMPARE_OP               exception-match
               94  POP_JUMP_IF_FALSE   146  'to 146'
               96  POP_TOP          
               98  STORE_FAST               'exc'
              100  POP_TOP          
              102  SETUP_FINALLY       134  'to 134'

 L. 606       104  LOAD_GLOBAL              logger
              106  LOAD_METHOD              error
              108  LOAD_FAST                'key'
              110  FORMAT_VALUE          0  ''
              112  LOAD_STR                 ' failed to download from cache: '
              114  LOAD_FAST                'exc'
              116  FORMAT_VALUE          0  ''
              118  BUILD_STRING_3        3 
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          

 L. 607       124  POP_BLOCK        
              126  POP_EXCEPT       
              128  CALL_FINALLY        134  'to 134'
              130  LOAD_CONST               False
              132  RETURN_VALUE     
            134_0  COME_FROM           128  '128'
            134_1  COME_FROM_FINALLY   102  '102'
              134  LOAD_CONST               None
              136  STORE_FAST               'exc'
              138  DELETE_FAST              'exc'
              140  END_FINALLY      
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM            94  '94'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM            86  '86'

 L. 608       148  LOAD_GLOBAL              logger
              150  LOAD_METHOD              info
              152  LOAD_STR                 'downloaded '
              154  LOAD_FAST                'video_path'
              156  FORMAT_VALUE          0  ''
              158  LOAD_STR                 ' from cache at '
              160  LOAD_FAST                'key'
              162  FORMAT_VALUE          0  ''
              164  BUILD_STRING_4        4 
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          

 L. 609       170  LOAD_CONST               True
              172  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 128

    def upload_to_cache--- This code section failed: ---

 L. 613         0  SETUP_FINALLY        28  'to 28'

 L. 614         2  LOAD_FAST                'self'
                4  LOAD_ATTR                s3_storage
                6  LOAD_ATTR                upload_file

 L. 615         8  LOAD_FAST                'video_path'

 L. 615        10  LOAD_FAST                'key'

 L. 615        12  LOAD_STR                 'encoder_version'
               14  LOAD_GLOBAL              ENCODER_VERSION
               16  BUILD_MAP_1           1 

 L. 614        18  LOAD_CONST               ('meta',)
               20  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               22  POP_TOP          
               24  POP_BLOCK        
               26  JUMP_FORWARD         88  'to 88'
             28_0  COME_FROM_FINALLY     0  '0'

 L. 617        28  DUP_TOP          
               30  LOAD_GLOBAL              Exception
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    86  'to 86'
               36  POP_TOP          
               38  STORE_FAST               'exc'
               40  POP_TOP          
               42  SETUP_FINALLY        74  'to 74'

 L. 618        44  LOAD_GLOBAL              logger
               46  LOAD_METHOD              error
               48  LOAD_FAST                'key'
               50  FORMAT_VALUE          0  ''
               52  LOAD_STR                 ' failed to upload to cache: '
               54  LOAD_FAST                'exc'
               56  FORMAT_VALUE          0  ''
               58  BUILD_STRING_3        3 
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L. 619        64  POP_BLOCK        
               66  POP_EXCEPT       
               68  CALL_FINALLY         74  'to 74'
               70  LOAD_CONST               False
               72  RETURN_VALUE     
             74_0  COME_FROM            68  '68'
             74_1  COME_FROM_FINALLY    42  '42'
               74  LOAD_CONST               None
               76  STORE_FAST               'exc'
               78  DELETE_FAST              'exc'
               80  END_FINALLY      
               82  POP_EXCEPT       
               84  JUMP_FORWARD         88  'to 88'
             86_0  COME_FROM            34  '34'
               86  END_FINALLY      
             88_0  COME_FROM            84  '84'
             88_1  COME_FROM            26  '26'

 L. 620        88  LOAD_GLOBAL              logger
               90  LOAD_METHOD              info
               92  LOAD_STR                 'uploaded '
               94  LOAD_FAST                'video_path'
               96  FORMAT_VALUE          0  ''
               98  LOAD_STR                 ' to cache at '
              100  LOAD_FAST                'key'
              102  FORMAT_VALUE          0  ''
              104  BUILD_STRING_4        4 
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          

 L. 621       110  LOAD_CONST               True
              112  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 68

    def download_video_files_batch(self, options, videos_ids):
        succeeded = []
        failed = []
        for video_id in videos_ids:
            options_copy = options.copy()
            video_location = options_copy['y2z_videos_dir'].joinpath(video_id)
            downloaded_from_cache = False
            if self.s3_storage:
                s3_key = f"{self.video_format}/{self.video_quality}/{video_id}"
                video_path = video_location.joinpath(f"video.{self.video_format}")
                downloaded_from_cache = self.download_from_cache(s3_key, video_path)
                options_copy['skip_download'] = downloaded_from_cache

        try:
            with youtube_dl.YoutubeDL(options_copy) as (ydl):
                ydl.download([video_id])
            post_process_video(video_location,
              video_id,
              (options_copy['y2z_video_format']),
              (options_copy['y2z_low_quality']),
              skip_recompress=downloaded_from_cache)
            succeeded.append(video_id)
        except (youtube_dl.utils.DownloadError, FileNotFoundError):
            failed.append(video_id)
        else:
            if self.s3_storage:
                downloaded_from_cache or self.upload_to_cache(s3_key, video_path)
            return (
             succeeded, failed)

    def download_authors_branding(self):
        videos_channels_json = load_json(self.cache_dir, 'videos_channels')
        uniq_channel_ids = list(set([chan['channelId'] for chan in videos_channels_json.values()]))
        for channel_id in uniq_channel_ids:
            save_channel_branding((self.channels_dir), channel_id, save_banner=False)

    def update_metadata(self):
        main_channel_json = get_channel_json(self.main_channel_id)
        save_channel_branding((self.channels_dir), (self.main_channel_id), save_banner=True)
        auto_title = self.playlists[0].title if (self.is_playlist and len(self.playlists) == 1) else (main_channel_json['snippet']['title'].strip())
        auto_description = clean_text(self.playlists[0].description) if (self.is_playlist and len(self.playlists) == 1) else (clean_text(main_channel_json['snippet']['description']))
        self.title = self.title or auto_title or '-'
        self.description = self.description or auto_description or '-'
        if self.creator is None:
            if self.is_single_channel:
                self.creator = _('Youtube Channel “{title}”').format(title=(main_channel_json['snippet']['title']))
            else:
                self.creator = _('Youtube Channels')
        self.publisher = self.publisher or 'Kiwix'
        self.tags = self.tags or ['youtube']
        if '_videos:yes' not in self.tags:
            self.tags.append('_videos:yes')
        self.zim_info.update(title=(self.title),
          description=(self.description),
          creator=(self.creator),
          publisher=(self.publisher),
          name=(self.name),
          tags=(self.tags))
        if not self.profile_path.exists():
            shutil.copy(self.channels_dir.joinpath(self.main_channel_id, 'profile.jpg'), self.profile_path)
        if not self.banner_path.exists():
            shutil.copy(self.channels_dir.joinpath(self.main_channel_id, 'banner.jpg'), self.banner_path)
        if self.main_color is None or self.secondary_color is None:
            profile_main, profile_secondary = get_colors(self.profile_path)
        self.main_color = self.main_color or profile_main
        self.secondary_color = self.secondary_color or profile_secondary
        resize_image((self.profile_path),
          width=48,
          height=48,
          method='thumbnail',
          to=(self.build_dir.joinpath('favicon.jpg')))

    def make_test_html_file(self):
        video_id = 'aaaabbbccddd'
        video_dir = self.videos_dir.joinpath(video_id)
        video_dir.mkdir(exist_ok=True)
        shutil.copy(self.assets_dir.joinpath('sample.jpg'), video_dir.joinpath('video.jpg'))
        env = jinja2.Environment(loader=(jinja2.FileSystemLoader(str(self.templates_dir))),
          autoescape=True)
        html = env.get_template('home.html').render(playlists=(self.sorted_playlists),
          video_format=(self.video_format),
          title=(self.title),
          description=(self.description),
          color=(self.main_color),
          background_color=(self.secondary_color),
          page_label=(_('Page {current}/{total}')),
          back_label=(_('Back to top')))
        with open((self.build_dir.joinpath('home.html')), 'w', encoding='utf-8') as (fp):
            fp.write(html)
        with open((self.assets_dir.joinpath('db.js')), 'w', encoding='utf-8') as (fp):
            fp.write(env.get_template('assets/db.js').render(NB_VIDEOS_PER_PAGE=(self.nb_videos_per_page)))
        with open((self.assets_dir.joinpath('data.js')), 'w', encoding='utf-8') as (fp):
            videos = [{'id':video_id, 
             'title':'A Sample Title', 
             'slug':'a-sample-title', 
             'description':'A sample description of video', 
             'subtitles':[],  'thumbnail':str(Path('videos').joinpath(video_id, 'video.jpg'))} for _ in range(0, 6)]
            fp.write('var json_{slug} = {json_str};\n'.format(slug=(self.sorted_playlists[0].slug),
              json_str=json.dumps(videos, indent=4)))

    def make_html_files(self, actual_videos_ids):
        """ make up HTML structure to read the content

        /home.html                                  Homepage

        for each video:
            - <slug-title>.html                     HTML article
            - videos/<videoId>/video.<ext>          video file
            - videos/<videoId>/video.<lang>.vtt     subtititle(s)
            - videos/<videoId>/video.jpg            template
        """

        def remove_unused_videos(videos):
            video_ids = [video['contentDetails']['videoId'] for video in videos]
            for path in self.videos_dir.iterdir():
                if path.is_dir() and path.name not in video_ids:
                    logger.debug(f"Removing unused video {path.name}")
                    shutil.rmtree(path, ignore_errors=True)

        def is_present(video):
            return video['contentDetails']['videoId'] in actual_videos_ids

        def video_has_channel(videos_channels, video):
            return video['contentDetails']['videoId'] in videos_channels

        def get_subtitles(video_id):
            video_dir = self.videos_dir.joinpath(video_id)
            languages = [x.stem.split('.')[1] for x in video_dir.iterdir() if x.is_file() if x.name.endswith('.vtt')]
            return [get_language_details(language) for language in languages]

        env = jinja2.Environment(loader=(jinja2.FileSystemLoader(str(self.templates_dir))),
          autoescape=True)
        videos = load_json(self.cache_dir, 'videos').values()
        videos = list(filter(is_present, videos))
        videos_channels = load_json(self.cache_dir, 'videos_channels')
        has_channel = functools.partial(video_has_channel, videos_channels)
        videos = list(filter(has_channel, videos))
        for video in videos:
            video_id = video['contentDetails']['videoId']
            title = video['snippet']['title']
            slug = get_slug(title)
            description = video['snippet']['description']
            publication_date = dt_parser.parse(video['contentDetails']['videoPublishedAt'])
            author = videos_channels[video_id]
            subtitles = get_subtitles(video_id)
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            html = env.get_template('article.html').render(video_id=video_id,
              video_format=(self.video_format),
              author=author,
              title=title,
              description=description,
              date=format_date(publication_date, format='medium', locale=(self.locale)),
              subtitles=subtitles,
              url=video_url,
              channel_id=(video['snippet']['channelId']),
              color=(self.main_color),
              background_color=(self.secondary_color),
              autoplay=(self.autoplay))
            with open((self.build_dir.joinpath(f"{slug}.html")),
              'w', encoding='utf-8') as (fp):
                fp.write(html)
        else:
            html = env.get_template('home.html').render(playlists=(self.playlists),
              video_format=(self.video_format),
              title=(self.title),
              description=(self.description),
              color=(self.main_color),
              background_color=(self.secondary_color),
              page_label=(_('Page {current}/{total}')),
              back_label=(_('Back to top')))
            with open((self.build_dir.joinpath('home.html')), 'w', encoding='utf-8') as (fp):
                fp.write(html)
            with open((self.assets_dir.joinpath('app.js')), 'w', encoding='utf-8') as (fp):
                fp.write(env.get_template('assets/app.js').render(video_format=(self.video_format)))
            with open((self.assets_dir.joinpath('db.js')), 'w', encoding='utf-8') as (fp):
                fp.write(env.get_template('assets/db.js').render(NB_VIDEOS_PER_PAGE=(self.nb_videos_per_page)))

            def to_data_js(video):
                return {'id':video['contentDetails']['videoId'], 
                 'title':video['snippet']['title'], 
                 'slug':get_slug(video['snippet']['title']), 
                 'description':video['snippet']['description'], 
                 'subtitles':get_subtitles(video['contentDetails']['videoId']), 
                 'thumbnail':str(Path('videos').joinpath(video['contentDetails']['videoId'], 'video.jpg'))}

            with open((self.assets_dir.joinpath('data.js')), 'w', encoding='utf-8') as (fp):
                for playlist in self.playlists:
                    playlist_videos = load_json(self.cache_dir, f"playlist_{playlist.playlist_id}_videos")
                    playlist_videos = list(filter(skip_deleted_videos, playlist_videos))
                    playlist_videos = list(filter(is_present, playlist_videos))
                    playlist_videos = list(filter(has_channel, playlist_videos))
                    playlist_videos.sort(key=(lambda v: v['snippet']['position']))
                    fp.write('var json_{slug} = {json_str};\n'.format(slug=(playlist.slug),
                      json_str=json.dumps((list(map(to_data_js, playlist_videos))),
                      indent=4)))

            with open((self.build_dir.joinpath('metadata.json')),
              'w', encoding='utf-8') as (fp):
                json.dump({'video_format': self.video_format}, fp, indent=4)
            remove_unused_videos(videos)