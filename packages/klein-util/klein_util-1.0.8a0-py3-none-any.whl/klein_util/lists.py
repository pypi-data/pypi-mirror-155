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

def uniqify(seq, idfun=None):
    # pylint: disable=function-redefined
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen:
            continue
        seen[marker] = 1
        result.append(item)
    return result


def add_string(input_list, value):
    """
    Adds a value to a list; checks thing type, and handles cases of the thing being a list or string.
    Currently doesn't handle dict data types.
    :param input_list: the input list to which we're adding the thing
    :param value: the value to be added
    :return list
    """
    if not isinstance(input_list, list):
        raise TypeError(f"Target list is is not a list: type detected = {type(input_list)}")

    if isinstance(value, int):
        value = str(value)

    if isinstance(value, str):
        value = [value]

    if isinstance(value, dict):
        value = list(value.keys())

    if not isinstance(value, list):
            raise TypeError(f"Item to be added to the target list is of unhandled type {type(value)}")

    return uniqify(input_list + value)
