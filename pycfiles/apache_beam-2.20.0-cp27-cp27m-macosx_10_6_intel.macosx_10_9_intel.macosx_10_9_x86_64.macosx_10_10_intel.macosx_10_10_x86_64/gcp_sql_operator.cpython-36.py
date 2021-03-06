# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_sql_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 34684 bytes
from googleapiclient.errors import HttpError
from airflow import AirflowException
from airflow.contrib.hooks.gcp_sql_hook import CloudSqlHook, CloudSqlDatabaseHook
from airflow.contrib.utils.gcp_field_validator import GcpBodyFieldValidator
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.base_hook import BaseHook
SETTINGS = 'settings'
SETTINGS_VERSION = 'settingsVersion'
CLOUD_SQL_CREATE_VALIDATION = [
 dict(name='name', allow_empty=False),
 dict(name='settings', type='dict', fields=[
  dict(name='tier', allow_empty=False),
  dict(name='backupConfiguration', type='dict', fields=[
   dict(name='binaryLogEnabled', optional=True),
   dict(name='enabled', optional=True),
   dict(name='replicationLogArchivingEnabled', optional=True),
   dict(name='startTime', allow_empty=False, optional=True)],
    optional=True),
  dict(name='activationPolicy', allow_empty=False, optional=True),
  dict(name='authorizedGaeApplications', type='list', optional=True),
  dict(name='crashSafeReplicationEnabled', optional=True),
  dict(name='dataDiskSizeGb', optional=True),
  dict(name='dataDiskType', allow_empty=False, optional=True),
  dict(name='databaseFlags', type='list', optional=True),
  dict(name='ipConfiguration', type='dict', fields=[
   dict(name='authorizedNetworks', type='list', fields=[
    dict(name='expirationTime', optional=True),
    dict(name='name', allow_empty=False, optional=True),
    dict(name='value', allow_empty=False, optional=True)],
     optional=True),
   dict(name='ipv4Enabled', optional=True),
   dict(name='privateNetwork', allow_empty=False, optional=True),
   dict(name='requireSsl', optional=True)],
    optional=True),
  dict(name='locationPreference', type='dict', fields=[
   dict(name='followGaeApplication', allow_empty=False, optional=True),
   dict(name='zone', allow_empty=False, optional=True)],
    optional=True),
  dict(name='maintenanceWindow', type='dict', fields=[
   dict(name='hour', optional=True),
   dict(name='day', optional=True),
   dict(name='updateTrack', allow_empty=False, optional=True)],
    optional=True),
  dict(name='pricingPlan', allow_empty=False, optional=True),
  dict(name='replicationType', allow_empty=False, optional=True),
  dict(name='storageAutoResize', optional=True),
  dict(name='storageAutoResizeLimit', optional=True),
  dict(name='userLabels', type='dict', optional=True)]),
 dict(name='databaseVersion', allow_empty=False, optional=True),
 dict(name='failoverReplica', type='dict', fields=[
  dict(name='name', allow_empty=False)],
   optional=True),
 dict(name='masterInstanceName', allow_empty=False, optional=True),
 dict(name='onPremisesConfiguration', type='dict', optional=True),
 dict(name='region', allow_empty=False, optional=True),
 dict(name='replicaConfiguration', type='dict', fields=[
  dict(name='failoverTarget', optional=True),
  dict(name='mysqlReplicaConfiguration', type='dict', fields=[
   dict(name='caCertificate', allow_empty=False, optional=True),
   dict(name='clientCertificate', allow_empty=False, optional=True),
   dict(name='clientKey', allow_empty=False, optional=True),
   dict(name='connectRetryInterval', optional=True),
   dict(name='dumpFilePath', allow_empty=False, optional=True),
   dict(name='masterHeartbeatPeriod', optional=True),
   dict(name='password', allow_empty=False, optional=True),
   dict(name='sslCipher', allow_empty=False, optional=True),
   dict(name='username', allow_empty=False, optional=True),
   dict(name='verifyServerCertificate', optional=True)],
    optional=True)],
   optional=True)]
CLOUD_SQL_EXPORT_VALIDATION = [
 dict(name='exportContext', type='dict', fields=[
  dict(name='fileType', allow_empty=False),
  dict(name='uri', allow_empty=False),
  dict(name='databases', optional=True, type='list'),
  dict(name='sqlExportOptions', type='dict', optional=True, fields=[
   dict(name='tables', optional=True, type='list'),
   dict(name='schemaOnly', optional=True)]),
  dict(name='csvExportOptions', type='dict', optional=True, fields=[
   dict(name='selectQuery')])])]
CLOUD_SQL_IMPORT_VALIDATION = [
 dict(name='importContext', type='dict', fields=[
  dict(name='fileType', allow_empty=False),
  dict(name='uri', allow_empty=False),
  dict(name='database', optional=True, allow_empty=False),
  dict(name='importUser', optional=True),
  dict(name='csvImportOptions', type='dict', optional=True, fields=[
   dict(name='table'),
   dict(name='columns', type='list', optional=True)])])]
CLOUD_SQL_DATABASE_CREATE_VALIDATION = [
 dict(name='instance', allow_empty=False),
 dict(name='name', allow_empty=False),
 dict(name='project', allow_empty=False)]
CLOUD_SQL_DATABASE_PATCH_VALIDATION = [
 dict(name='instance', optional=True),
 dict(name='name', optional=True),
 dict(name='project', optional=True),
 dict(name='etag', optional=True),
 dict(name='charset', optional=True),
 dict(name='collation', optional=True)]

class CloudSqlBaseOperator(BaseOperator):
    """CloudSqlBaseOperator"""

    @apply_defaults
    def __init__(self, instance, project_id=None, gcp_conn_id='google_cloud_default', api_version='v1beta4', *args, **kwargs):
        self.project_id = project_id
        self.instance = instance
        self.gcp_conn_id = gcp_conn_id
        self.api_version = api_version
        self._validate_inputs()
        self._hook = CloudSqlHook(gcp_conn_id=(self.gcp_conn_id), api_version=(self.api_version))
        (super(CloudSqlBaseOperator, self).__init__)(*args, **kwargs)

    def _validate_inputs(self):
        if self.project_id == '':
            raise AirflowException("The required parameter 'project_id' is empty")
        if not self.instance:
            raise AirflowException("The required parameter 'instance' is empty or None")

    def _check_if_instance_exists(self, instance):
        try:
            return self._hook.get_instance(project_id=(self.project_id), instance=instance)
        except HttpError as e:
            status = e.resp.status
            if status == 404:
                return False
            raise e

    def _check_if_db_exists(self, db_name):
        try:
            return self._hook.get_database(project_id=(self.project_id),
              instance=(self.instance),
              database=db_name)
        except HttpError as e:
            status = e.resp.status
            if status == 404:
                return False
            raise e

    def execute(self, context):
        pass

    @staticmethod
    def _get_settings_version(instance):
        return instance.get(SETTINGS).get(SETTINGS_VERSION)


class CloudSqlInstanceCreateOperator(CloudSqlBaseOperator):
    """CloudSqlInstanceCreateOperator"""
    template_fields = ('project_id', 'instance', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, body, instance, project_id=None, gcp_conn_id='google_cloud_default', api_version='v1beta4', validate_body=True, *args, **kwargs):
        self.body = body
        self.validate_body = validate_body
        (super(CloudSqlInstanceCreateOperator, self).__init__)(args, project_id=project_id, instance=instance, gcp_conn_id=gcp_conn_id, api_version=api_version, **kwargs)

    def _validate_inputs(self):
        super(CloudSqlInstanceCreateOperator, self)._validate_inputs()
        if not self.body:
            raise AirflowException("The required parameter 'body' is empty")

    def _validate_body_fields(self):
        if self.validate_body:
            GcpBodyFieldValidator(CLOUD_SQL_CREATE_VALIDATION, api_version=(self.api_version)).validate(self.body)

    def execute(self, context):
        self._validate_body_fields()
        if not self._check_if_instance_exists(self.instance):
            self._hook.create_instance(project_id=(self.project_id),
              body=(self.body))
        else:
            self.log.info('Cloud SQL instance with ID {} already exists. Aborting create.'.format(self.instance))
        instance_resource = self._hook.get_instance(project_id=(self.project_id), instance=(self.instance))
        service_account_email = instance_resource['serviceAccountEmailAddress']
        task_instance = context['task_instance']
        task_instance.xcom_push(key='service_account_email', value=service_account_email)


class CloudSqlInstancePatchOperator(CloudSqlBaseOperator):
    """CloudSqlInstancePatchOperator"""
    template_fields = ('project_id', 'instance', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, body, instance, project_id=None, gcp_conn_id='google_cloud_default', api_version='v1beta4', *args, **kwargs):
        self.body = body
        (super(CloudSqlInstancePatchOperator, self).__init__)(args, project_id=project_id, instance=instance, gcp_conn_id=gcp_conn_id, api_version=api_version, **kwargs)

    def _validate_inputs(self):
        super(CloudSqlInstancePatchOperator, self)._validate_inputs()
        if not self.body:
            raise AirflowException("The required parameter 'body' is empty")

    def execute(self, context):
        if not self._check_if_instance_exists(self.instance):
            raise AirflowException('Cloud SQL instance with ID {} does not exist. Please specify another instance to patch.'.format(self.instance))
        else:
            return self._hook.patch_instance(project_id=(self.project_id),
              body=(self.body),
              instance=(self.instance))


class CloudSqlInstanceDeleteOperator(CloudSqlBaseOperator):
    """CloudSqlInstanceDeleteOperator"""
    template_fields = ('project_id', 'instance', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, instance, project_id=None, gcp_conn_id='google_cloud_default', api_version='v1beta4', *args, **kwargs):
        (super(CloudSqlInstanceDeleteOperator, self).__init__)(args, project_id=project_id, instance=instance, gcp_conn_id=gcp_conn_id, api_version=api_version, **kwargs)

    def execute(self, context):
        if not self._check_if_instance_exists(self.instance):
            print('Cloud SQL instance with ID {} does not exist. Aborting delete.'.format(self.instance))
            return True
        else:
            return self._hook.delete_instance(project_id=(self.project_id),
              instance=(self.instance))


class CloudSqlInstanceDatabaseCreateOperator(CloudSqlBaseOperator):
    """CloudSqlInstanceDatabaseCreateOperator"""
    template_fields = ('project_id', 'instance', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, instance, body, project_id=None, gcp_conn_id='google_cloud_default', api_version='v1beta4', validate_body=True, *args, **kwargs):
        self.body = body
        self.validate_body = validate_body
        (super(CloudSqlInstanceDatabaseCreateOperator, self).__init__)(args, project_id=project_id, instance=instance, gcp_conn_id=gcp_conn_id, api_version=api_version, **kwargs)

    def _validate_inputs(self):
        super(CloudSqlInstanceDatabaseCreateOperator, self)._validate_inputs()
        if not self.body:
            raise AirflowException("The required parameter 'body' is empty")

    def _validate_body_fields(self):
        if self.validate_body:
            GcpBodyFieldValidator(CLOUD_SQL_DATABASE_CREATE_VALIDATION, api_version=(self.api_version)).validate(self.body)

    def execute(self, context):
        self._validate_body_fields()
        database = self.body.get('name')
        if not database:
            self.log.error("Body doesn't contain 'name'. Cannot check if the database already exists in the instance {}.".format(self.instance))
            return False
        else:
            if self._check_if_db_exists(database):
                self.log.info("Cloud SQL instance with ID {} already contains database '{}'. Aborting database insert.".format(self.instance, database))
                return True
            return self._hook.create_database(project_id=(self.project_id), instance=(self.instance),
              body=(self.body))


class CloudSqlInstanceDatabasePatchOperator(CloudSqlBaseOperator):
    """CloudSqlInstanceDatabasePatchOperator"""
    template_fields = ('project_id', 'instance', 'database', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, instance, database, body, project_id=None, gcp_conn_id='google_cloud_default', api_version='v1beta4', validate_body=True, *args, **kwargs):
        self.database = database
        self.body = body
        self.validate_body = validate_body
        (super(CloudSqlInstanceDatabasePatchOperator, self).__init__)(args, project_id=project_id, instance=instance, gcp_conn_id=gcp_conn_id, api_version=api_version, **kwargs)

    def _validate_inputs(self):
        super(CloudSqlInstanceDatabasePatchOperator, self)._validate_inputs()
        if not self.body:
            raise AirflowException("The required parameter 'body' is empty")
        if not self.database:
            raise AirflowException("The required parameter 'database' is empty")

    def _validate_body_fields(self):
        if self.validate_body:
            GcpBodyFieldValidator(CLOUD_SQL_DATABASE_PATCH_VALIDATION, api_version=(self.api_version)).validate(self.body)

    def execute(self, context):
        self._validate_body_fields()
        if not self._check_if_db_exists(self.database):
            raise AirflowException("Cloud SQL instance with ID {} does not contain database '{}'. Please specify another database to patch.".format(self.instance, self.database))
        else:
            return self._hook.patch_database(project_id=(self.project_id),
              instance=(self.instance),
              database=(self.database),
              body=(self.body))


class CloudSqlInstanceDatabaseDeleteOperator(CloudSqlBaseOperator):
    """CloudSqlInstanceDatabaseDeleteOperator"""
    template_fields = ('project_id', 'instance', 'database', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, instance, database, project_id=None, gcp_conn_id='google_cloud_default', api_version='v1beta4', *args, **kwargs):
        self.database = database
        (super(CloudSqlInstanceDatabaseDeleteOperator, self).__init__)(args, project_id=project_id, instance=instance, gcp_conn_id=gcp_conn_id, api_version=api_version, **kwargs)

    def _validate_inputs(self):
        super(CloudSqlInstanceDatabaseDeleteOperator, self)._validate_inputs()
        if not self.database:
            raise AirflowException("The required parameter 'database' is empty")

    def execute(self, context):
        if not self._check_if_db_exists(self.database):
            print("Cloud SQL instance with ID {} does not contain database '{}'. Aborting database delete.".format(self.instance, self.database))
            return True
        else:
            return self._hook.delete_database(project_id=(self.project_id),
              instance=(self.instance),
              database=(self.database))


class CloudSqlInstanceExportOperator(CloudSqlBaseOperator):
    """CloudSqlInstanceExportOperator"""
    template_fields = ('project_id', 'instance', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, instance, body, project_id=None, gcp_conn_id='google_cloud_default', api_version='v1beta4', validate_body=True, *args, **kwargs):
        self.body = body
        self.validate_body = validate_body
        (super(CloudSqlInstanceExportOperator, self).__init__)(args, project_id=project_id, instance=instance, gcp_conn_id=gcp_conn_id, api_version=api_version, **kwargs)

    def _validate_inputs(self):
        super(CloudSqlInstanceExportOperator, self)._validate_inputs()
        if not self.body:
            raise AirflowException("The required parameter 'body' is empty")

    def _validate_body_fields(self):
        if self.validate_body:
            GcpBodyFieldValidator(CLOUD_SQL_EXPORT_VALIDATION, api_version=(self.api_version)).validate(self.body)

    def execute(self, context):
        self._validate_body_fields()
        return self._hook.export_instance(project_id=(self.project_id),
          instance=(self.instance),
          body=(self.body))


class CloudSqlInstanceImportOperator(CloudSqlBaseOperator):
    """CloudSqlInstanceImportOperator"""
    template_fields = ('project_id', 'instance', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, instance, body, project_id=None, gcp_conn_id='google_cloud_default', api_version='v1beta4', validate_body=True, *args, **kwargs):
        self.body = body
        self.validate_body = validate_body
        (super(CloudSqlInstanceImportOperator, self).__init__)(args, project_id=project_id, instance=instance, gcp_conn_id=gcp_conn_id, api_version=api_version, **kwargs)

    def _validate_inputs(self):
        super(CloudSqlInstanceImportOperator, self)._validate_inputs()
        if not self.body:
            raise AirflowException("The required parameter 'body' is empty")

    def _validate_body_fields(self):
        if self.validate_body:
            GcpBodyFieldValidator(CLOUD_SQL_IMPORT_VALIDATION, api_version=(self.api_version)).validate(self.body)

    def execute(self, context):
        self._validate_body_fields()
        return self._hook.import_instance(project_id=(self.project_id),
          instance=(self.instance),
          body=(self.body))


class CloudSqlQueryOperator(BaseOperator):
    """CloudSqlQueryOperator"""
    template_fields = ('sql', 'gcp_cloudsql_conn_id', 'gcp_conn_id')
    template_ext = ('.sql', )

    @apply_defaults
    def __init__(self, sql, autocommit=False, parameters=None, gcp_conn_id='google_cloud_default', gcp_cloudsql_conn_id='google_cloud_sql_default', *args, **kwargs):
        (super(CloudSqlQueryOperator, self).__init__)(*args, **kwargs)
        self.sql = sql
        self.gcp_conn_id = gcp_conn_id
        self.gcp_cloudsql_conn_id = gcp_cloudsql_conn_id
        self.autocommit = autocommit
        self.parameters = parameters
        self.gcp_connection = BaseHook.get_connection(self.gcp_conn_id)
        self.cloudsql_db_hook = CloudSqlDatabaseHook(gcp_cloudsql_conn_id=gcp_cloudsql_conn_id,
          gcp_conn_id=gcp_conn_id,
          default_gcp_project_id=(self.gcp_connection.extra_dejson.get('extra__google_cloud_platform__project')))
        self.cloud_sql_proxy_runner = None
        self.database_hook = None

    def execute(self, context):
        self.cloudsql_db_hook.validate_ssl_certs()
        self.cloudsql_db_hook.create_connection()
        try:
            self.cloudsql_db_hook.validate_socket_path_length()
            self.database_hook = self.cloudsql_db_hook.get_database_hook()
            try:
                try:
                    if self.cloudsql_db_hook.use_proxy:
                        self.cloud_sql_proxy_runner = self.cloudsql_db_hook.get_sqlproxy_runner()
                        self.cloudsql_db_hook.free_reserved_port()
                        self.cloud_sql_proxy_runner.start_proxy()
                    self.log.info('Executing: "%s"', self.sql)
                    self.database_hook.run((self.sql), (self.autocommit), parameters=(self.parameters))
                finally:
                    if self.cloud_sql_proxy_runner:
                        self.cloud_sql_proxy_runner.stop_proxy()
                        self.cloud_sql_proxy_runner = None

            finally:
                self.cloudsql_db_hook.cleanup_database_hook()

        finally:
            self.cloudsql_db_hook.delete_connection()
            self.cloudsql_db_hook = None