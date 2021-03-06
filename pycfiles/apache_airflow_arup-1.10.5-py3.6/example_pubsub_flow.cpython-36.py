# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_pubsub_flow.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3199 bytes
"""
This example DAG demonstrates how the PubSub*Operators and PubSubPullSensor
can be used to trigger dependant tasks upon receipt of a Pub/Sub message.

NOTE: project_id must be updated to a GCP project ID accessible with the
      Google Default Credentials on the machine running the workflow
"""
from __future__ import unicode_literals
from base64 import b64encode
import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.pubsub_operator import PubSubTopicCreateOperator, PubSubSubscriptionCreateOperator, PubSubPublishOperator, PubSubTopicDeleteOperator, PubSubSubscriptionDeleteOperator
from airflow.contrib.sensors.pubsub_sensor import PubSubPullSensor
from airflow.utils import dates
project = 'your-project-id'
topic = 'example-topic'
subscription = 'subscription-to-example-topic'
messages = [
 {'data': b64encode(b'Hello World')},
 {'data': b64encode(b'Another message')},
 {'data': b64encode(b'A final message')}]
default_args = {'owner':'airflow', 
 'depends_on_past':False, 
 'start_date':dates.days_ago(2), 
 'email':[
  'airflow@example.com'], 
 'email_on_failure':False, 
 'email_on_retry':False, 
 'project':project, 
 'topic':topic, 
 'subscription':subscription}
echo_template = '\n{% for m in task_instance.xcom_pull(task_ids=\'pull-messages\') %}\n    echo "AckID: {{ m.get(\'ackId\') }}, Base64-Encoded: {{ m.get(\'message\') }}"\n{% endfor %}\n'
with DAG('pubsub-end-to-end', default_args=default_args, schedule_interval=datetime.timedelta(days=1)) as (dag):
    t1 = PubSubTopicCreateOperator(task_id='create-topic')
    t2 = PubSubSubscriptionCreateOperator(task_id='create-subscription',
      topic_project=project,
      subscription=subscription)
    t3 = PubSubPublishOperator(task_id='publish-messages',
      messages=messages)
    t4 = PubSubPullSensor(task_id='pull-messages', ack_messages=True)
    t5 = BashOperator(task_id='echo-pulled-messages', bash_command=echo_template)
    t6 = PubSubSubscriptionDeleteOperator(task_id='delete-subscription')
    t7 = PubSubTopicDeleteOperator(task_id='delete-topic')
    t1 >> t2 >> t3
    t2 >> t4 >> t5 >> t6 >> t7