# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/tasks/integrations.py
# Compiled at: 2019-08-21 05:33:05
from __future__ import absolute_import
from time import time
from datetime import timedelta
import logging, six
from sentry import analytics, features
from sentry.models import Activity, ExternalIssue, Group, GroupLink, GroupStatus, Integration, Organization, ObjectStatus, OrganizationIntegration, Repository, User
from sentry.integrations.exceptions import ApiError, ApiUnauthorized, IntegrationError
from sentry.models.apitoken import generate_token
from sentry.tasks.base import instrumented_task, retry
logger = logging.getLogger('sentry.tasks.integrations')

def should_comment_sync(installation, external_issue):
    organization = Organization.objects.get(id=external_issue.organization_id)
    has_issue_sync = features.has('organizations:integrations-issue-sync', organization)
    return has_issue_sync and installation.should_sync('comment')


@instrumented_task(name='sentry.tasks.integrations.post_comment', queue='integrations', default_retry_delay=300, max_retries=5)
@retry(exclude=(ExternalIssue.DoesNotExist, Integration.DoesNotExist))
def post_comment(external_issue_id, data, user_id, **kwargs):
    external_issue = ExternalIssue.objects.get(id=external_issue_id)
    organization = Organization.objects.get(id=external_issue.organization_id)
    has_issue_sync = features.has('organizations:integrations-issue-sync', organization)
    if not has_issue_sync:
        return
    integration = Integration.objects.get(id=external_issue.integration_id)
    installation = integration.get_installation(organization_id=external_issue.organization_id)
    if installation.should_sync('comment'):
        installation.create_comment(external_issue.key, user_id, data['text'])
        analytics.record('integration.issue.comments.synced', provider=integration.provider, id=integration.id, organization_id=external_issue.organization_id, user_id=user_id)


@instrumented_task(name='sentry.tasks.integrations.create_comment', queue='integrations', default_retry_delay=300, max_retries=5)
@retry(exclude=(ExternalIssue.DoesNotExist, Integration.DoesNotExist))
def create_comment(external_issue_id, user_id, group_note_id, **kwargs):
    external_issue = ExternalIssue.objects.get(id=external_issue_id)
    installation = Integration.objects.get(id=external_issue.integration_id).get_installation(organization_id=external_issue.organization_id)
    if not should_comment_sync(installation, external_issue):
        return
    try:
        note = Activity.objects.get(type=Activity.NOTE, id=group_note_id)
    except Activity.DoesNotExist:
        return

    comment = installation.create_comment(external_issue.key, user_id, note)
    note.data['external_id'] = installation.get_comment_id(comment)
    note.save()
    analytics.record('integration.issue.comments.synced', provider=installation.model.provider, id=installation.model.id, organization_id=external_issue.organization_id, user_id=user_id)


@instrumented_task(name='sentry.tasks.integrations.update_comment', queue='integrations', default_retry_delay=300, max_retries=5)
@retry(exclude=(ExternalIssue.DoesNotExist, Integration.DoesNotExist))
def update_comment(external_issue_id, user_id, group_note_id, **kwargs):
    external_issue = ExternalIssue.objects.get(id=external_issue_id)
    installation = Integration.objects.get(id=external_issue.integration_id).get_installation(organization_id=external_issue.organization_id)
    if not should_comment_sync(installation, external_issue):
        return
    try:
        note = Activity.objects.get(type=Activity.NOTE, id=group_note_id)
    except Activity.DoesNotExist:
        return

    installation.update_comment(external_issue.key, user_id, note)
    analytics.record('integration.issue.comments.synced', provider=installation.model.provider, id=installation.model.id, organization_id=external_issue.organization_id, user_id=user_id)


@instrumented_task(name='sentry.tasks.integrations.jira.sync_metadata', queue='integrations', default_retry_delay=20, max_retries=5)
@retry(on=(IntegrationError,), exclude=(Integration.DoesNotExist,))
def sync_metadata(integration_id, **kwargs):
    integration = Integration.objects.get(id=integration_id)
    installation = integration.get_installation(None)
    installation.sync_metadata()
    return


@instrumented_task(name='sentry.tasks.integrations.sync_assignee_outbound', queue='integrations', default_retry_delay=300, max_retries=5)
@retry(exclude=(
 ExternalIssue.DoesNotExist,
 Integration.DoesNotExist,
 User.DoesNotExist,
 Organization.DoesNotExist))
def sync_assignee_outbound(external_issue_id, user_id, assign, **kwargs):
    external_issue = ExternalIssue.objects.get(id=external_issue_id)
    organization = Organization.objects.get(id=external_issue.organization_id)
    has_issue_sync = features.has('organizations:integrations-issue-sync', organization)
    if not has_issue_sync:
        return
    else:
        integration = Integration.objects.get(id=external_issue.integration_id)
        if user_id is None:
            user = None
        else:
            user = User.objects.get(id=user_id)
        installation = integration.get_installation(organization_id=external_issue.organization_id)
        if installation.should_sync('outbound_assignee'):
            installation.sync_assignee_outbound(external_issue, user, assign=assign)
            analytics.record('integration.issue.assignee.synced', provider=integration.provider, id=integration.id, organization_id=external_issue.organization_id)
        return


@instrumented_task(name='sentry.tasks.integrations.sync_status_outbound', queue='integrations', default_retry_delay=300, max_retries=5)
@retry(exclude=Integration.DoesNotExist)
def sync_status_outbound(group_id, external_issue_id, **kwargs):
    try:
        group = Group.objects.filter(id=group_id, status__in=[GroupStatus.UNRESOLVED, GroupStatus.RESOLVED])[0]
    except IndexError:
        return

    has_issue_sync = features.has('organizations:integrations-issue-sync', group.organization)
    if not has_issue_sync:
        return
    try:
        external_issue = ExternalIssue.objects.get(id=external_issue_id)
    except ExternalIssue.DoesNotExist:
        return

    integration = Integration.objects.get(id=external_issue.integration_id)
    installation = integration.get_installation(organization_id=external_issue.organization_id)
    if installation.should_sync('outbound_status'):
        installation.sync_status_outbound(external_issue, group.status == GroupStatus.RESOLVED, group.project_id)
        analytics.record('integration.issue.status.synced', provider=integration.provider, id=integration.id, organization_id=external_issue.organization_id)


@instrumented_task(name='sentry.tasks.integrations.kick_off_status_syncs', queue='integrations', default_retry_delay=300, max_retries=5)
@retry()
def kick_off_status_syncs(project_id, group_id, **kwargs):
    external_issue_ids = GroupLink.objects.filter(project_id=project_id, group_id=group_id, linked_type=GroupLink.LinkedType.issue).values_list('linked_id', flat=True)
    for external_issue_id in external_issue_ids:
        sync_status_outbound.apply_async(kwargs={'group_id': group_id, 'external_issue_id': external_issue_id})


@instrumented_task(name='sentry.tasks.integrations.migrate_repo', queue='integrations', default_retry_delay=300, max_retries=5)
@retry(exclude=(Integration.DoesNotExist, Repository.DoesNotExist, Organization.DoesNotExist))
def migrate_repo(repo_id, integration_id, organization_id):
    integration = Integration.objects.get(id=integration_id)
    installation = integration.get_installation(organization_id=organization_id)
    repo = Repository.objects.get(id=repo_id)
    if installation.has_repo_access(repo):
        if repo.integration_id is not None and repo.integration_id != integration_id:
            logger.info('repo.migration.integration-change', extra={'integration_id': integration_id, 
               'old_integration_id': repo.integration_id, 
               'organization_id': organization_id, 
               'repo_id': repo.id})
        repo.integration_id = integration_id
        repo.provider = 'integrations:%s' % (integration.provider,)
        original_status = repo.status
        if repo.status == ObjectStatus.DISABLED:
            repo.status = ObjectStatus.VISIBLE
        repo.save()
        logger.info('repo.migrated', extra={'integration_id': integration_id, 
           'organization_id': organization_id, 
           'repo_id': repo.id, 
           'original_status': original_status})
        from sentry.mediators.plugins import Migrator
        Migrator.run(integration=integration, organization=Organization.objects.get(id=organization_id))
    return


@instrumented_task(name='sentry.tasks.integrations.kickoff_vsts_subscription_check', queue='integrations', default_retry_delay=300, max_retries=5)
@retry()
def kickoff_vsts_subscription_check():
    organization_integrations = OrganizationIntegration.objects.filter(integration__provider='vsts', integration__status=ObjectStatus.VISIBLE, status=ObjectStatus.VISIBLE).select_related('integration')
    six_hours_ago = time() - timedelta(hours=6).seconds
    for org_integration in organization_integrations:
        organization_id = org_integration.organization_id
        integration = org_integration.integration
        try:
            if 'subscription' not in integration.metadata or integration.metadata['subscription']['check'] > six_hours_ago:
                continue
        except KeyError:
            pass

        vsts_subscription_check.apply_async(kwargs={'integration_id': integration.id, 'organization_id': organization_id})


@instrumented_task(name='sentry.tasks.integrations.vsts_subscription_check', queue='integrations', default_retry_delay=300, max_retries=5)
@retry(exclude=(ApiError, ApiUnauthorized, Integration.DoesNotExist))
def vsts_subscription_check(integration_id, organization_id, **kwargs):
    integration = Integration.objects.get(id=integration_id)
    installation = integration.get_installation(organization_id=organization_id)
    client = installation.get_client()
    try:
        subscription_id = integration.metadata['subscription']['id']
        subscription = client.get_subscription(instance=installation.instance, subscription_id=subscription_id)
    except (KeyError, ApiError) as e:
        logger.info('vsts_subscription_check.failed_to_get_subscription', extra={'integration_id': integration_id, 
           'organization_id': organization_id, 
           'error': six.text_type(e)})
        subscription = None

    if not subscription or subscription['status'] == 'disabledBySystem':
        if subscription:
            try:
                client.delete_subscription(instance=installation.instance, subscription_id=subscription_id)
            except ApiError as e:
                logger.info('vsts_subscription_check.failed_to_delete_subscription', extra={'integration_id': integration_id, 
                   'organization_id': organization_id, 
                   'subscription_id': subscription_id, 
                   'error': six.text_type(e)})

        try:
            secret = generate_token()
            subscription = client.create_subscription(instance=installation.instance, shared_secret=secret)
        except ApiError as e:
            logger.info('vsts_subscription_check.failed_to_create_subscription', extra={'integration_id': integration_id, 
               'organization_id': organization_id, 
               'error': six.text_type(e)})
        else:
            integration.metadata['subscription']['id'] = subscription['id']
            integration.metadata['subscription']['secret'] = secret
            logger.info('vsts_subscription_check.updated_diabled_subscription', extra={'integration_id': integration_id, 
               'organization_id': organization_id, 
               'subscription_id': subscription_id})

        integration.metadata['subscription']['check'] = time()
        integration.save()
    return