# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/social/models.py
# Compiled at: 2010-09-19 02:55:46
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from social.constants import SOCIAL_GROUPS
from friends.models import Friendship

def resolve_is_member_method(name):
    options = {'Everyone': is_member_everyone, 
       'Nobody': is_member_nobody, 
       'Friends': is_member_friends, 
       'Friends of Friends': is_member_friends_of_friends}
    return options[name]


def is_member_everyone(target_user, requesting_user):
    """
    Always return True. All users are part of 'Everyone'.
    """
    return True


def is_member_nobody(target_user, requesting_user):
    """
    Always return False. No users are part of 'Nobody'.
    """
    return False


def is_member_friends(target_user, requesting_user):
    """
    Return true if requesting user is a friend of target user
    """
    if requesting_user.is_anonymous():
        return False
    return Friendship.objects.are_friends(target_user, requesting_user)


def is_member_friends_of_friends(target_user, requesting_user):
    """
    Return true if requesting user is a friend of target user
    or is a friend of any of target user's friends.
    """
    if requesting_user.is_anonymous():
        return False
    if Friendship.objects.are_friends(target_user, requesting_user):
        return True
    else:
        friends = Friendship.objects.friends_for_user(target_user)
        for friend in friends:
            if Friendship.objects.are_friends(friend['friend'], requesting_user):
                return True

    return False


class SocialObjectPermission(models.Model):
    user = models.ForeignKey(User)
    can_view = models.BooleanField(default=False)
    can_change = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    social_group = models.IntegerField(choices=SOCIAL_GROUPS)
    content_type = models.ForeignKey(ContentType)

    def is_member(self, target_user, requesting_user):
        """
        Determine if the requesting user is part of the social group this permission applies to.
        """
        return resolve_is_member_method(SOCIAL_GROUPS[self.social_group][1])(target_user, requesting_user)


class SocialObjectFieldPermission(models.Model):
    user = models.ForeignKey(User)
    can_view = models.BooleanField(default=False)
    can_change = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    social_group = models.IntegerField(choices=SOCIAL_GROUPS)
    content_type = models.ForeignKey(ContentType)
    field_name = models.CharField(max_length=128)

    def is_member(self, target_user, requesting_user):
        """
        Determine if the requesting user is part of the social group this permission applies to.
        """
        return resolve_is_member_method(SOCIAL_GROUPS[self.social_group][1])(target_user, requesting_user)