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

    def test_coowner_secret(self):
        secret = self.client.secret.get('26a2d53c-5260-47b5-8478-28900c24a714')
        self.assertEqual(secret['id'], '26a2d53c-5260-47b5-8478-28900c24a714')

    def test_coowner_secret_2(self):
        secret = self.client.secret.get('0031ff60-9873-4ffc-b0b1-6b9551867712')
        self.assertEqual(secret['id'], '0031ff60-9873-4ffc-b0b1-6b9551867712')

    def test_article(self):
        article = self.client.article.get('9791092c-1c13-4c46-8f23-c9a29d24513a')
        self.assertEqual(article['id'], '9791092c-1c13-4c46-8f23-c9a29d24513a')