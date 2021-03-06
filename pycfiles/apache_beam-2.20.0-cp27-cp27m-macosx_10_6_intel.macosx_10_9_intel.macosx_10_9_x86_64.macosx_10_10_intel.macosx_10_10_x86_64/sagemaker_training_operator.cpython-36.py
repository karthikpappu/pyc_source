# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/sagemaker_training_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4033 bytes
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.contrib.operators.sagemaker_base_operator import SageMakerBaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException

class SageMakerTrainingOperator(SageMakerBaseOperator):
    """SageMakerTrainingOperator"""
    integer_fields = [
     [
      'ResourceConfig', 'InstanceCount'],
     [
      'ResourceConfig', 'VolumeSizeInGB'],
     [
      'StoppingCondition', 'MaxRuntimeInSeconds']]

    @apply_defaults
    def __init__(self, config, wait_for_completion=True, print_log=True, check_interval=30, max_ingestion_time=None, *args, **kwargs):
        (super(SageMakerTrainingOperator, self).__init__)(args, config=config, **kwargs)
        self.wait_for_completion = wait_for_completion
        self.print_log = print_log
        self.check_interval = check_interval
        self.max_ingestion_time = max_ingestion_time

    def expand_role(self):
        if 'RoleArn' in self.config:
            hook = AwsHook(self.aws_conn_id)
            self.config['RoleArn'] = hook.expand_role(self.config['RoleArn'])

    def execute(self, context):
        self.preprocess_config()
        self.log.info('Creating SageMaker Training Job %s.', self.config['TrainingJobName'])
        response = self.hook.create_training_job((self.config),
          wait_for_completion=(self.wait_for_completion),
          print_log=(self.print_log),
          check_interval=(self.check_interval),
          max_ingestion_time=(self.max_ingestion_time))
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise AirflowException('Sagemaker Training Job creation failed: %s' % response)
        else:
            return {'Training': self.hook.describe_training_job(self.config['TrainingJobName'])}