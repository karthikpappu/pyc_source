# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/models/userprofile.py
# Compiled at: 2014-08-27 19:26:12
from datetime import datetime
import itertools
from django.conf import settings
from django.db import models
from django.db.models.loading import get_model
from django.core.urlresolvers import reverse
from shortuuidfield import ShortUUIDField
from validators import is_number_from_study_area, is_mobile_number, is_landline
from study import StudySite, Study
from reply import Reply
from observation import Observation
from signalbox import phone_field

class UserProfile(models.Model):
    """Extension of the User model; accessible via profile."""
    uuid = ShortUUIDField(auto=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    landline = phone_field.PhoneNumberField(blank=True, null=True, validators=[
     is_number_from_study_area, is_landline])
    mobile = phone_field.PhoneNumberField(blank=True, null=True, verbose_name='Mobile telephone number', validators=[
     is_number_from_study_area], help_text='mobile phone number, with international prefix')

    def formatted_mobile(self):
        return phone_field.international_string(self.mobile)

    prefer_mobile = models.BooleanField(default=True, help_text='Make calls to mobile telephone number where possible. Unticking this\n        means the user prefers calls on their landline.')
    address_1 = models.CharField(blank=True, null=True, max_length=200)
    address_2 = models.CharField(blank=True, null=True, max_length=200)
    address_3 = models.CharField(blank=True, null=True, max_length=200)
    postcode = models.CharField(blank=True, null=True, max_length=10, help_text='This is the postcode of your current address.')
    county = models.CharField(blank=True, null=True, max_length=50)
    site = models.ForeignKey('signalbox.StudySite', blank=True, null=True)
    title = models.CharField(blank=True, null=True, max_length=20, choices=settings.TITLE_CHOICES)
    professional_registration_number = models.CharField(blank=True, null=True, max_length=200, help_text='A registration number for health professionals.')
    organisation = models.CharField(blank=True, null=True, max_length=200, help_text='e.g. the\n        name of the surgery or hospital to which you are attached')

    def can_login_from_observation_token(self):
        """Determines which users can login from an observation token.

        For example, via an email survey. We always prevent staff and clinicians
        from doing this because it might be unsafe, but for some studies we do
        let users do it because it's convenient.
        """
        notstaff = not self.user.is_staff
        notclinician = 'Clinicians' not in [ i.name for i in self.user.groups.all() ]
        return bool(notstaff and notclinician)

    def get_required_fields_for_studies(self):
        studies = [ i.study for i in self.user.membership_set.all() ]
        return set(itertools.chain(*[ i.profile_fields_dict()['required'] for i in studies ]))

    def get_visible_fields_for_studies(self):
        studies = [ i.study for i in self.user.membership_set.all() ]
        return set(itertools.chain(*[ i.userprofile_fields_dict()['visible'] for i in studies ]))

    def has_all_required_details(self, studies=None):
        required = set(settings.DEFAULT_USER_PROFILE_FIELDS).union(set(self.get_required_fields_for_studies()))
        for i in filter(bool, required):
            if not getattr(self, i, None):
                return False

        return True

    def get_voice_number(self):
        if not self.prefer_mobile:
            return self.landline or self.mobile
        else:
            return self.mobile or self.landline

    def current_memberships(self):
        memberships = [ m for m in self.user.membership_set.all() if m.is_current() ]
        return memberships

    def previous_reply_set(self):
        """Returns a list of replies to be shown on the user's dashboard.

        Not just any reply will appear. The script it relates to must be
        marked as creating replies suitable for display in the dashboard
        (although this is the default).
        """
        return Reply.objects.filter(user=self.user).exclude(observation__created_by_script__show_replies_on_dashboard__isnull=True).order_by('observation__dyad', 'started')

    def dashboard_studies(self):
        return Study.objects.all()

    def has_observation_expiring_today(self):
        return sum([ i.has_observation_expiring_today() for i in self.current_memberships() ])

    def other_memberships(self):
        memberships = [ m for m in self.user.membership_set.all() if not m.is_current() ]
        return memberships

    def address_components(self):
        """Returns a list of address components."""
        items = (
         self.address_1, self.address_2, self.address_3, self.postcode.upper(),
         self.county)
        return [ i for i in items if i ]

    def ad_hoc_scripts_available(self):
        studies = set(self.user.membership_set.all().values_list('study__id', flat=True))
        return bool(sum([ i.ad_hoc_scripts.all().count() for i in Study.objects.filter(id__in=studies)
                        ]))

    def tasklist_observations(self):
        """Returns Observations due for this User."""
        obs = Observation.objects.filter(dyad__in=self.user.membership_set.all()).order_by('dyad__study')
        obs = [ i for i in obs if i.ready_to_send() and i.show_in_tasklist() and i.can_add_answers()
              ]
        return obs

    def obs_by_study(self):
        """Returns list of tuples with Studies and Observations due for this User."""
        obs = self.tasklist_observations()
        obs_by_study = [ (i, list(j)) for i, j in itertools.groupby(obs, lambda x: x.dyad.study)
                       ]
        obs_by_study = [ (i, j) for i, j in obs_by_study if len(j) ]
        obs_by_study = [ (i, sorted(j, key=lambda x: x.due)) for i, j in obs_by_study
                       ]
        return obs_by_study

    def participant_admin_overview(self):
        return reverse('edit_participant', args=(self.user.id,))

    class Meta:
        app_label = 'signalbox'

    def __unicode__(self):
        return '%s %s (%s)' % (self.user.first_name, self.user.last_name, self.user.username)