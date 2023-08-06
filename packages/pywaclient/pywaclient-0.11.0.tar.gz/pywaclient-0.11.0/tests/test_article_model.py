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

from models.user import User
from pywaclient.api import AragornApiClient
from pywaclient.models.article import Article


class TestArticleModel(unittest.TestCase):

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

    def testHasParentArticle(self):
        article = Article(self.client, self.client.article.get('7c6b1e91-210f-4519-929e-bb6c79c92899'))
        self.assertTrue(article.has_parent_article)

    def testGetParentArticle(self):
        article = Article(self.client, self.client.article.get('7c6b1e91-210f-4519-929e-bb6c79c92899'))
        parent = article.get_parent_article()
        self.assertEqual(parent.title, 'Test Parent Article')

    def test_get_category(self):
        article = Article(self.client, self.client.article.get('7583923f-ef7d-4813-8265-b109ce3c45cb'))
        self.assertEqual(article.category_title, 'Parent Category')
        self.assertEqual(article.category_id, '99e5083f-1217-47b4-80f1-b21da6a656d5')
        self.assertEqual(article.category.title, 'Parent Category')

    def test_last_update(self):
        article = Article(self.client, self.client.article.get('7c6b1e91-210f-4519-929e-bb6c79c92899'))
        self.assertEqual(article.last_update, '2021-02-07 11:25:51.000000')

        article = Article(self.client, self.client.article.get('e1da4cf0-601e-4920-85dd-33e024de98a4'))
        self.assertEqual(article.last_update, '2020-02-25 01:18:20.000000')

    def test_creation_date(self):
        article = Article(self.client, self.client.article.get('7c6b1e91-210f-4519-929e-bb6c79c92899'))
        self.assertEqual(article.creation_date, '2021-02-07 11:22:33.000000')

    def test_notification_date(self):
        article = Article(self.client, self.client.article.get('7c6b1e91-210f-4519-929e-bb6c79c92899'))
        self.assertEqual(article.notification_date, '')

    def test_excerpt(self):
        article = Article(self.client, self.client.article.get('7c6b1e91-210f-4519-929e-bb6c79c92899'))
        self.assertEqual(article.excerpt, 'This articles for tests with a child article.')


if __name__ == '__main__':
    unittest.main()
