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
from time import sleep

from models.user import User
from pywaclient.api import AragornApiClient


class TestArticleEndpoint(unittest.TestCase):

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

    def test_get_private_article_by_co_owner(self):
        article = self.client.article.get('0de4a4a5-de6e-4e6d-b4e6-82f73257633a')
        self.assertEqual(article['id'], '0de4a4a5-de6e-4e6d-b4e6-82f73257633a')

    def test_article(self):
        article = self.client.article.get('48d301ff-9547-4593-8647-bea70070dc6c')
        self.assertEqual(article['id'], '48d301ff-9547-4593-8647-bea70070dc6c')

    def test_post_article(self):
        identifier = self.client.article.post(
            {'title': 'Test Article Creation', 'template': 'article', 'world': 'daae0a12-f3c3-4978-b571-b5313e3c1741'}
        )
        self.client.article.patch(identifier, {'content': 'Some Content'})
        sleep(1)
        self.client.article.delete(identifier)


if __name__ == '__main__':
    unittest.main()
