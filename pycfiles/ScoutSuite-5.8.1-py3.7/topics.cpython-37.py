# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/sns/topics.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1573 bytes
import json
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources
from .subscriptions import Subscriptions

class Topics(AWSCompositeResources):
    _children = [
     (
      Subscriptions, 'subscriptions')]

    def __init__(self, facade, region):
        super(Topics, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_topics = await self.facade.sns.get_topics(self.region)
        for raw_topic in raw_topics:
            topic_name, topic = self._parse_topic(raw_topic)
            self[topic_name] = topic

        await self._fetch_children_of_all_resources(resources=self,
          scopes={topic_id:{'region':self.region,  'topic_name':topic['name']} for topic_id, topic in self.items()})
        for topic in self.values():
            topic['subscriptions_count'] = topic['subscriptions'].pop('subscriptions_count')

    def _parse_topic(self, raw_topic):
        raw_topic['arn'] = raw_topic.pop('TopicArn')
        raw_topic['name'] = raw_topic['arn'].split(':')[(-1)]
        attributes = raw_topic.pop('attributes')
        for k in ('Owner', 'DisplayName'):
            raw_topic[k] = attributes[k] if k in attributes else None

        for k in ('Policy', 'DeliveryPolicy', 'EffectiveDeliveryPolicy'):
            raw_topic[k] = json.loads(attributes[k]) if k in attributes else None

        return (raw_topic['name'], raw_topic)