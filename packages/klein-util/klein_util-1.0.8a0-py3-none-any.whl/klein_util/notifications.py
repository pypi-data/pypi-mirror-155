# copyright 2022 Medicines Discovery Catapult
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
import json
from klein_config import get_config
import boto3


def notify(msg, **kwargs):
    config = get_config()
    if config.has("notifications.topic") and config.has("aws"):
        msg_string = json.dumps(msg)
        client = boto3.client('sns', region_name=config.get("aws.region"))
        client.publish(
            TopicArn=config.get("notifications.topic"),
            Message=msg_string,
            Subject=kwargs["subject"] if "subject" in kwargs else "Consumer Notification",
        )
