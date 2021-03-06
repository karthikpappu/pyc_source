# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cmsplugin_team/cms_plugins.py
# Compiled at: 2013-03-19 04:13:06
from django.contrib import admin
from django.db import models
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from cmsplugin_team.models import TeamPlugin, TeamMember, SocialLink
from editor.admin import EditorAdmin

class SocialLinkInline(admin.TabularInline):
    model = SocialLink


class TeamMemberAdmin(EditorAdmin):
    inlines = [
     SocialLinkInline]
    list_display = ['name', 'position']


class CMSTeamPlugin(CMSPluginBase):
    model = TeamPlugin
    name = 'Team'

    def render(self, context, instance, placeholder):
        self.render_template = instance.template
        print instance.members.all()
        context.update({'instance': instance, 
           'members': instance.members.all(), 
           'name': instance.name})
        return context


plugin_pool.register_plugin(CMSTeamPlugin)
admin.site.register(TeamMember, TeamMemberAdmin)