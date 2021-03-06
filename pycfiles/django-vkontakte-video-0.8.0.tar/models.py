# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-vkontakte-video/vkontakte_video/models.py
# Compiled at: 2015-06-02 11:53:10
import logging
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from vkontakte_api.decorators import fetch_all, atomic
from vkontakte_api.mixins import CountOffsetManagerMixin, AfterBeforeManagerMixin, OwnerableModelMixin, LikableModelMixin, ActionableModelMixin
from vkontakte_api.models import VkontaktePKModel
from vkontakte_comments.mixins import CommentableModelMixin
log = logging.getLogger('vkontakte_video')

class AlbumRemoteManager(CountOffsetManagerMixin):

    def get_timeline_date(self, instance):
        return instance.updated or instance.created or timezone.now()

    @atomic
    def fetch(self, owner=None, **kwargs):
        if not owner:
            raise ValueError('You must specify owner, which albums you want to fetch')
        kwargs['owner_id'] = self.model.get_owner_remote_id(owner)
        kwargs['extended'] = 1
        return super(AlbumRemoteManager, self).fetch(**kwargs)


class VideoRemoteManager(CountOffsetManagerMixin, AfterBeforeManagerMixin):

    @atomic
    @fetch_all
    def fetch(self, album=None, owner=None, ids=None, extended=1, **kwargs):
        if not (album or owner):
            raise ValueError('You must specify or video album or owner, which video you want to fetch')
        if owner:
            kwargs['owner_id'] = self.model.get_owner_remote_id(owner)
        if album:
            kwargs['owner_id'] = album.owner_remote_id
            kwargs['album_id'] = album.remote_id
            kwargs['extra_fields'] = {'album': album}
        if ids:
            videos = []
            owner_id = kwargs['owner_id']
            for id in ids:
                vid = '%s_%s' % (owner_id, id)
                videos.append(vid)

            kwargs['videos'] = (',').join(videos)
        kwargs['extended'] = extended
        return super(VideoRemoteManager, self).fetch(**kwargs)


@python_2_unicode_compatible
class Album(OwnerableModelMixin, VkontaktePKModel):
    photo_160 = models.URLField(max_length=255)
    videos_count = models.PositiveIntegerField('Кол-во видеозаписей')
    title = models.CharField(max_length=200)
    objects = models.Manager()
    remote = AlbumRemoteManager(remote_pk=('remote_id', ), version=5.27, methods_namespace='video', methods={'get': 'getAlbums'})

    class Meta:
        get_latest_by = 'remote_id'
        verbose_name = 'Альбом видеозаписей Вконтакте'
        verbose_name_plural = 'Альбомы видеозаписей Вконтакте'

    def __str__(self):
        return self.title

    @property
    def slug(self):
        return 'videos%s?section=album_%s' % (self.owner_remote_id, self.remote_id)

    def parse(self, response):
        response['videos_count'] = response.pop('count')
        super(Album, self).parse(response)

    @atomic
    def fetch_videos(self, *args, **kwargs):
        videos = Video.remote.fetch(album=self, *args, **kwargs)
        if videos.count() > self.videos_count:
            self.videos_count = videos.count()
            self.save()
        return videos


@python_2_unicode_compatible
class Video(OwnerableModelMixin, ActionableModelMixin, LikableModelMixin, CommentableModelMixin, VkontaktePKModel):
    comments_remote_related_name = 'video_id'
    likes_remote_type = 'video'
    album = models.ForeignKey(Album, null=True, related_name='videos')
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField('Продолжительность')
    views_count = models.PositiveIntegerField('Кол-во просмотров', default=0)
    photo_130 = models.URLField(max_length=255)
    player = models.URLField(max_length=255)
    date = models.DateTimeField(help_text='Дата создания', db_index=True)
    objects = models.Manager()
    remote = VideoRemoteManager(remote_pk=('remote_id', ), version=5.27, methods_namespace='video', methods={'get': 'get'})

    class Meta:
        get_latest_by = 'remote_id'
        verbose_name = 'Видеозапись Вконтакте'
        verbose_name_plural = 'Видеозаписи Вконтакте'

    def __str__(self):
        return self.title

    @property
    def slug(self):
        return 'video%s_%s' % (self.owner_remote_id, self.remote_id)

    def _substitute(self, old_instance):
        if old_instance.album_id:
            self.album_id = old_instance.album_id
        super(Video, self)._substitute(old_instance)

    def parse(self, response):
        response['views_count'] = response.pop('views')
        super(Video, self).parse(response)