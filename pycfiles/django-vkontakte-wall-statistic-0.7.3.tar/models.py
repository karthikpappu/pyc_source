# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-vkontakte-wall-statistic/vkontakte_wall_statistic/models.py
# Compiled at: 2015-06-18 19:12:52
import logging
from django.db import models
from django.utils.translation import ugettext as _
from vkontakte_api.models import VkontakteManager, VkontakteModel
from vkontakte_groups.models import Group
from vkontakte_wall.models import Post
log = logging.getLogger('vkontakte_wall_statistic')

class PostStatisticRemoteManager(VkontakteManager):

    def fetch(self, post, date_from, date_to, *args, **kwargs):
        kwargs['date_from'] = date_from
        kwargs['date_to'] = date_to
        kwargs['group_id'] = post.owner.remote_id
        kwargs['post_id'] = post.remote_id_short
        kwargs['extra_fields'] = {'post_id': post.id}
        return super(PostStatisticRemoteManager, self).fetch(*args, **kwargs)


class PostReachRemoteManager(VkontakteManager):

    def fetch(self, post, *args, **kwargs):
        kwargs['owner_id'] = post.owner.remote_id
        if isinstance(post.owner, Group):
            kwargs['owner_id'] *= -1
        kwargs['post_id'] = post.remote_id_short
        kwargs['extra_fields'] = {'post_id': post.id}
        return super(PostReachRemoteManager, self).fetch(*args, **kwargs)

    def parse_response(self, response, extra_fields=None):
        return self.parse_response_dict(response[0], extra_fields)


class PostStatisticAbstract(models.Model):
    reach = models.PositiveIntegerField('Полный охват', default=0)
    reach_subscribers = models.PositiveIntegerField('Охват подписчиков', default=0)
    link_clicks = models.PositiveIntegerField('Клики по ссылкам', default=0)
    reach_males = models.PositiveIntegerField('Охват по мужчинам', default=0)
    reach_females = models.PositiveIntegerField('Охват по женщинам', default=0)
    reach_age_18 = models.PositiveIntegerField('Охват по возрасту до 18', default=0)
    reach_age_18_21 = models.PositiveIntegerField('Охват по возрасту от 18 до 21', default=0)
    reach_age_21_24 = models.PositiveIntegerField('Охват по возрасту от 21 до 24', default=0)
    reach_age_24_27 = models.PositiveIntegerField('Охват по возрасту от 24 до 27', default=0)
    reach_age_27_30 = models.PositiveIntegerField('Охват по возрасту от 27 до 30', default=0)
    reach_age_30_35 = models.PositiveIntegerField('Охват по возрасту от 30 до 35', default=0)
    reach_age_35_45 = models.PositiveIntegerField('Охват по возрасту от 35 до 45', default=0)
    reach_age_45 = models.PositiveIntegerField('Охват по возрасту от 45', default=0)
    reach_males_age_18 = models.PositiveIntegerField('Охват по мужчинам до 18', default=0)
    reach_males_age_18_21 = models.PositiveIntegerField('Охват по мужчинам от 18 до 21', default=0)
    reach_males_age_21_24 = models.PositiveIntegerField('Охват по мужчинам от 21 до 24', default=0)
    reach_males_age_24_27 = models.PositiveIntegerField('Охват по мужчинам от 24 до 27', default=0)
    reach_males_age_27_30 = models.PositiveIntegerField('Охват по мужчинам от 27 до 30', default=0)
    reach_males_age_30_35 = models.PositiveIntegerField('Охват по мужчинам от 30 до 35', default=0)
    reach_males_age_35_45 = models.PositiveIntegerField('Охват по мужчинам от 35 до 45', default=0)
    reach_males_age_45 = models.PositiveIntegerField('Охват по мужчинам от 45', default=0)
    reach_females_age_18 = models.PositiveIntegerField('Охват по женщинам до 18', default=0)
    reach_females_age_18_21 = models.PositiveIntegerField('Охват по женщинам от 18 до 21', default=0)
    reach_females_age_21_24 = models.PositiveIntegerField('Охват по женщинам от 21 до 24', default=0)
    reach_females_age_24_27 = models.PositiveIntegerField('Охват по женщинам от 24 до 27', default=0)
    reach_females_age_27_30 = models.PositiveIntegerField('Охват по женщинам от 27 до 30', default=0)
    reach_females_age_30_35 = models.PositiveIntegerField('Охват по женщинам от 30 до 35', default=0)
    reach_females_age_35_45 = models.PositiveIntegerField('Охват по женщинам от 35 до 45', default=0)
    reach_females_age_45 = models.PositiveIntegerField('Охват по женщинам от 45', default=0)

    class Meta:
        abstract = True


class PostStatistic(VkontakteModel, PostStatisticAbstract):
    """
    Post statistic model collecting information
    """
    methods_namespace = 'stats'
    post = models.ForeignKey(Post, verbose_name='Сообщение', related_name='statistics')
    date = models.DateField('Дата', db_index=True)
    period = models.PositiveSmallIntegerField('Период', choices=((1, 'День'), (30, 'Месяц')), default=1, db_index=True)
    objects = models.Manager()
    remote = PostStatisticRemoteManager(remote_pk=('post', 'date'), methods={'get': 'getPostStats'})

    class Meta:
        verbose_name = _('Vkontakte post statistic')
        verbose_name_plural = _('Vkontakte post statistics')
        unique_together = ('post', 'date', 'period')

    def parse(self, response):
        """
        Transform response for correct parsing it in parent method
        """
        response['date'] = response.pop('day')
        fields_map = {'sex': {'f': 'females', 
                   'm': 'males'}, 
           'age': {'12-18': 'age_18', 
                   '18-21': 'age_18_21', 
                   '21-24': 'age_21_24', 
                   '24-27': 'age_24_27', 
                   '27-30': 'age_27_30', 
                   '30-35': 'age_30_35', 
                   '35-45': 'age_35_45', 
                   '45-100': 'age_45'}, 
           'sex_age': {'f;12-18': 'females_age_18', 
                       'f;18-21': 'females_age_18_21', 
                       'f;21-24': 'females_age_21_24', 
                       'f;24-27': 'females_age_24_27', 
                       'f;27-30': 'females_age_27_30', 
                       'f;30-35': 'females_age_30_35', 
                       'f;35-45': 'females_age_35_45', 
                       'f;45-100': 'females_age_45', 
                       'm;12-18': 'males_age_18', 
                       'm;18-21': 'males_age_18_21', 
                       'm;21-24': 'males_age_21_24', 
                       'm;24-27': 'males_age_24_27', 
                       'm;27-30': 'males_age_27_30', 
                       'm;30-35': 'males_age_30_35', 
                       'm;35-45': 'males_age_35_45', 
                       'm;45-100': 'males_age_45'}}
        for response_field in ['sex', 'age', 'sex_age']:
            for item in response.pop(response_field, []):
                if 'value' in item and 'reach' in item:
                    response['reach_' + fields_map[response_field][item['value']]] = item['reach']

        return super(PostStatistic, self).parse(response)


class PostReach(VkontakteModel):
    """
    Post reach model
    """
    methods_namespace = 'stats'
    post = models.OneToOneField(Post, verbose_name='Сообщение', related_name='reach', primary_key=True)
    hide = models.PositiveIntegerField()
    join_group = models.PositiveIntegerField()
    links = models.PositiveIntegerField()
    reach_subscribers = models.PositiveIntegerField()
    reach_total = models.PositiveIntegerField()
    report = models.PositiveIntegerField()
    to_group = models.PositiveIntegerField()
    unsubscribe = models.PositiveIntegerField()
    objects = models.Manager()
    remote = PostReachRemoteManager(remote_pk=('post', ), methods={'get': 'getPostReach'})

    class Meta:
        verbose_name = _('Vkontakte post reach')
        verbose_name_plural = _('Vkontakte post reaches')