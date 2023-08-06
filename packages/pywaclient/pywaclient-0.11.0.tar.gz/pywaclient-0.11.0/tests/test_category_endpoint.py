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
import json
import os
import unittest

from models.user import User
from pywaclient.api import AragornApiClient


class TestCategoryEndpoint(unittest.TestCase):

    def setUp(self):
        self.client = AragornApiClient(
            name='TEST APPLICATION',
            url='https://gitlab.com/SoulLink/world-anvil-api-client',
            application_key=os.environ.get('WA_APPLICATION_KEY'),
            authentication_token=os.environ.get('WA_AUTH_TOKEN'),
            version='0.1.0'
        )
        self.user = User(self.client)

    def testEmptyCategory(self):
        category = self.client.category.get('93acb705-2500-4f0d-92cc-e46e5db52589')
        with open('data/empty_catgeory.json', 'r') as fp:
            data = json.load(fp)
        self.assertEqual(category, data)

    def testFullCategory(self):
        category = self.client.category.get('38206bac-46b2-4093-96bd-d0ec393218d4')
        with open('data/full_category.json', 'r') as fp:
            data = json.load(fp)
        self.assertEqual(category, data)

    def testCategoryWithParent(self):
        category = self.client.category.get('9fa4bd6c-a2c2-4159-8015-fc44b35d06a8')
        with open('data/category_with_parent.json', 'r') as fp:
            data = json.load(fp)
        self.assertEqual(category, data)


if __name__ == '__main__':
    unittest.main()
