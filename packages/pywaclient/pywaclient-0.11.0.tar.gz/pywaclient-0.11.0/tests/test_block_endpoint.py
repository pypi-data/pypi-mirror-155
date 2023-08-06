#    Copyright 2020 Jonas Waeber
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import logging
import os
import sys
import unittest

from pywaclient.exceptions import InternalServerException
from pywaclient.models.world import World
from pywaclient.api import AragornApiClient
from pywaclient.models.user import User

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class TestEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = AragornApiClient(
            name='TEST APPLICATION',
            url='https://gitlab.com/SoulLink/world-anvil-api-client',
            application_key=os.environ.get('WA_APPLICATION_KEY'),
            authentication_token=os.environ.get('WA_AUTH_TOKEN'),
            version='0.1.0'
        )
        self.maxDiff = None
        self.user = User(self.client)
        self.world = World(self.client, self.client.world.get('daae0a12-f3c3-4978-b571-b5313e3c1741'))

    def testGetBlockById(self):
        with self.assertRaises(InternalServerException):
            self.client.block.get('678589')
