# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdjango/contrib/auth/models.py
# Compiled at: 2016-06-20 12:45:24
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from xdjango.db.models import PhoneNumberField, SafeManager
from xdjango.core.sms import send_sms

class EmailUserManager(BaseUserManager, SafeManager):
    """ Custom manager for EmailUser."""

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """ Create and save an EmailUser with the given email and password.
        :param str email: user email
        :param str password: user password
        :param bool is_staff: whether user staff or not
        :param bool is_superuser: whether user admin or not
        :return custom_user.models.EmailUser user: user
        :raise ValueError: email is not set
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        is_active = extra_fields.pop('is_active', True)
        user = self.model(email=email, is_staff=is_staff, is_active=is_active, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """ Create and save an EmailUser with the given email and password.
        :param str email: user email
        :param str password: user password
        :return custom_user.models.EmailUser user: regular user
        """
        is_staff = extra_fields.pop('is_staff', False)
        return self._create_user(email, password, is_staff, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """ Create and save an EmailUser with the given email and password.
        :param str email: user email
        :param str password: user password
        :return custom_user.models.EmailUser user: admin user
        """
        return self._create_user(email, password, True, True, **extra_fields)


class EmailPhoneUserManager(BaseUserManager):
    """ Custom manager for EmailPhoneUser."""
    silent_create_user = True

    def get_by_natural_key(self, username, silent=False):
        try:
            return self.get(email=username)
        except ObjectDoesNotExist:
            pass

        try:
            return self.get(pk=username)
        except:
            pass

        try:
            return self.get(phone_number=username)
        except:
            if not silent:
                raise

    def delete_user(self, username, silent=True):
        """
        Delete a user, if exists. Otherwise, nothing is done.
        :param username:
        :return:
        """
        user = self.get_by_natural_key(username, silent=silent)
        if user:
            user.delete()

    def _create_user(self, email, phone_number, password, is_staff, is_superuser, **extra_fields):
        """ Create and save an EmailPhoneUser with the given email and password.
        :param str email: user email
        :param str phone_number: user phone_number
        :param str password: user password
        :param bool is_staff: whether user staff or not
        :param bool is_superuser: whether user admin or not
        :return custom_user.models.EmailUser user: user
        :raise ValueError: email or phone_number is not set
        """
        now = timezone.now()
        if email is None and phone_number is None:
            raise ValueError('The given email or phone_number must be set')
        if email is not None:
            email = self.normalize_email(email)
        is_active = extra_fields.pop('is_active', True)
        user = self.model(email=email, is_staff=is_staff, is_active=is_active, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        if phone_number:
            user.phone_number = phone_number
        try:
            user.save(using=self._db)
        except IntegrityError:
            if self.silent_create_user:
                return
            raise

        return user

    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        """ Create and save an EmailUser with the given email and password.
        :param str email: user email
        :param str phone_number: user phone_number
        :param str password: user password
        :return custom_user.models.EmailPhoneUser user: regular user
        """
        is_staff = extra_fields.pop('is_staff', False)
        return self._create_user(email, phone_number, password, is_staff, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """ Create and save an EmailUser with the given email and password.
        :param str email: user email
        :param str password: user password
        :return custom_user.models.EmailPhoneUser user: admin user
        """
        return self._create_user(email, None, password, True, True, **extra_fields)

    def get_or_create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        """ Get or create and save an EmailUser with the given email and password.
        :param str email: user email
        :param str phone_number: user phone_number
        :param str password: user password
        :return custom_user.models.EmailPhoneUser user: regular user
        """
        try:
            user = self.get(email=email)
        except:
            try:
                user = self.get(phone_number=phone_number)
            except:
                user = None

        if user:
            return user
        else:
            return self.create_user(email, phone_number, password, **extra_fields)


class AbstractEmailUser(AbstractBaseUser, PermissionsMixin):
    """ Abstract User with the same behaviour as Django's default User.
    AbstractEmailUser does not have username field. Uses email as the
    USERNAME_FIELD for authentication.
    Use this if you need to extend EmailUser.
    Inherits from both the AbstractBaseUser and PermissionMixin.
    The following attributes are inherited from the superclasses:
        * password
        * last_login
        * is_superuser
    """
    email = models.EmailField(_('email address'), max_length=255, unique=True, db_index=True)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = EmailUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        """ Return the email."""
        return self.email

    def get_short_name(self):
        """ Return the email."""
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ Send an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def deactivate(self):
        """
        """
        self.is_active = False
        self.save()


class AbstractEmailPhoneUser(AbstractBaseUser, PermissionsMixin):
    """ Abstract User with the same behaviour as Django's default User.
    AbstractEmailUser does not have username field. Uses email as the
    USERNAME_FIELD for authentication.
    Use this if you need to extend EmailUser.
    Inherits from both the AbstractBaseUser and PermissionMixin.
    The following attributes are inherited from the superclasses:
        * password
        * last_login
        * is_superuser
    """
    email = models.EmailField(unique=True, db_index=True, null=True, default=None, blank=True)
    phone_number = PhoneNumberField(unique=True, db_index=True, null=True, default=None, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    failed_login_attempts = models.IntegerField(default=0)
    objects = EmailPhoneUserManager()
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def __unicode__(self):
        return unicode(self.id)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ Send an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def sms_user(self, message, sender=None, **kwargs):
        """ Send a sms to this User."""
        send_sms(message, sender, [self.phone_number], **kwargs)

    def has_email(self):
        return self.email

    def has_phone_number(self):
        return self.phone_number

    def increment_failed_attempts_counter(self):
        self.failed_login_attempts += 1
        self.save()

    def initialize_failed_attempts_counter(self):
        self.failed_login_attempts = 0
        self.save()