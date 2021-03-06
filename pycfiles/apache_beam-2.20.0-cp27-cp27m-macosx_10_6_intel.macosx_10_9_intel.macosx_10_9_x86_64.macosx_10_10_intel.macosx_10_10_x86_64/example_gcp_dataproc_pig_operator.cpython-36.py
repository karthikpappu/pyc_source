# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_gcp_dataproc_pig_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2049 bytes
__doc__ = '\nExample Airflow DAG for Google Dataproc PigOperator\n'
import os, airflow
from airflow import models
from airflow.contrib.operators.dataproc_operator import DataProcPigOperator, DataprocClusterCreateOperator, DataprocClusterDeleteOperator
default_args = {'start_date': airflow.utils.dates.days_ago(1)}
CLUSTER_NAME = os.environ.get('GCP_DATAPROC_CLUSTER_NAME', 'example-project')
PROJECT_ID = os.environ.get('GCP_PROJECT_ID', 'an-id')
REGION = os.environ.get('GCP_LOCATION', 'europe-west1')
with models.DAG('example_gcp_dataproc_pig_operator',
  default_args=default_args,
  schedule_interval=None) as (dag):
    create_task = DataprocClusterCreateOperator(task_id='create_task',
      cluster_name=CLUSTER_NAME,
      project_id=PROJECT_ID,
      region=REGION,
      num_workers=2)
    pig_task = DataProcPigOperator(task_id='pig_task',
      query="define sin HiveUDF('sin');",
      region=REGION,
      cluster_name=CLUSTER_NAME)
    delete_task = DataprocClusterDeleteOperator(task_id='delete_task',
      project_id=PROJECT_ID,
      cluster_name=CLUSTER_NAME,
      region=REGION)
    create_task >> pig_task >> delete_task