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
import os
import unittest

from pywaclient.models.user import User
from pywaclient.api import AragornApiClient


class TestSecretEndpoint(unittest.TestCase):

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

    def test_get_secret(self):
        secret = self.client.secret.get('d68ad140-ef7f-4733-8cb5-b9addfdf85d3')
        self.assertEqual(secret['id'], 'd68ad140-ef7f-4733-8cb5-b9addfdf85d3')
        self.assertEqual(secret['title'], 'Title')
        self.assertEqual(secret['content'], 'Content')
        self.assertEqual(secret['state'], 'private')


if __name__ == '__main__':
    unittest.main()
