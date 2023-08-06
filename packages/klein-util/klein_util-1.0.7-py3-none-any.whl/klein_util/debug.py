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
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="enable debug", action="store_true")
parser.add_argument("--info", help="enable debug", action="store_true")
args, unknown = parser.parse_known_args()

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

level = logging.ERROR

if args.info:
    level = logging.INFO
elif args.debug:
    level = logging.DEBUG

logging.basicConfig(level=level, format=LOG_FORMAT)
