# Copyright 2017, Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import collections
import sys

import psutil

from google.cloud.proto.pubsub.v1 import pubsub_pb2
from google.gax.utils.messages import get_messages


# Define the default values for batching.
#
# This class is used when creating a publisher or subscriber client, and
# these settings can be altered to tweak Pub/Sub behavior.
# The defaults should be fine for most use cases.
Batching = collections.namedtuple('Batching',
    ['max_bytes', 'max_latency', 'max_messages'],
)
Batching.__new__.__defaults__ = (
    1024 * 1024 * 5,  # max_bytes: 5 MB
    0.25,             # max_latency: 0.25 seconds
    1000,             # max_messages: 1,000
)

# Define the type class and default values for flow control settings.
#
# This class is used when creating a publisher or subscriber client, and
# these settings can be altered to tweak Pub/Sub behavior.
# The defaults should be fine for most use cases.
FlowControl = collections.namedtuple('FlowControl',
    ['max_bytes', 'max_messages'],
)
FlowControl.__new__.__defaults__ = (
    psutil.virtual_memory().total * 0.2,  # max_bytes: 20% of total RAM
    float('inf'),                         # max_messages: no limit
)


names = ['Batching', 'FlowControl']
for name, message in get_messages(pubsub_pb2).items():
    setattr(sys.modules[__name__], name, message)
    names.append(name)


__all__ = tuple(sorted(names))