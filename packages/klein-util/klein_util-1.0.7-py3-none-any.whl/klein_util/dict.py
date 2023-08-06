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


def traverse_dict(data, parts):
    remaining = len(parts)
    key = parts.pop(0)
    if key not in data:
        raise LookupError(f"Key '{key}' does not exist in {json.dumps(list(data.keys()))}")
    return traverse_dict(data[key], parts) if remaining > 1 else data[key]
