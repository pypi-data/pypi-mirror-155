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

from pywaclient.models.category import Category
from pywaclient.models.user import User
from pywaclient.models.world import World
from pywaclient.api import AragornApiClient


class TestCategoryEntity(unittest.TestCase):

    def setUp(self):
        self.client = AragornApiClient(
            name='TEST APPLICATION',
            url='https://gitlab.com/SoulLink/world-anvil-api-client',
            application_key=os.environ.get('WA_APPLICATION_KEY'),
            authentication_token=os.environ.get('WA_AUTH_TOKEN'),
            version='0.1.0'
        )
        self.user = User(self.client)
        self.category = Category(self.client, self.client.category.get('38206bac-46b2-4093-96bd-d0ec393218d4'))

    def test_category_word(self):
        world = self.category.world
        self.assertIsInstance(world, World)


if __name__ == '__main__':
    unittest.main()
