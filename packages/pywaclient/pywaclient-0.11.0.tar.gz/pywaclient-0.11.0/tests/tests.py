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
from collections import Iterable

import requests

from pywaclient.api import AragornApiClient
from pywaclient.models.article import Article
from pywaclient.models.genre import Genre
from pywaclient.models.user import User
from pywaclient.models.world import World

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

    def testAuthenticatedUser(self):
        self.assertEqual('42eb1d6a-021b-49b4-bbbb-f7ddf6b135a4', self.client.user.authenticated_user_id)

    def testUserEndpointWorlds(self):
        self.assertEqual('a86b6da9-6ba2-413a-87d9-ee98cbc6d9b9', self.client.user.worlds()[0]['id'])

    def testWorldEndpointArticles(self):
        articles = self.client.world.articles(self.client.user.worlds()[0]['id'])
        self.assertTrue(isinstance(articles, Iterable))

    def testImageEndpointGetBinary(self):
        images = self.client.world.images(self.client.user.worlds()[0]['id'])
        byte_stream = self.client.image.get_binary(next(images)['id'])
        self.assertTrue(isinstance(byte_stream, Iterable))

    def testArticleEndpointGet(self):
        article = self.client.article.get('4d8c93bc-bdb4-418c-b3d0-8c14fa1bf59c', load_all_properties="true")
        article2 = self.client.article.get('4d8c93bc-bdb4-418c-b3d0-8c14fa1bf59c')
        self.assertEqual(article, article2)

    def testArticle(self):
        article = Article(self.client, self.client.article.get('4d8c93bc-bdb4-418c-b3d0-8c14fa1bf59c'))
        self.assertTrue(article.full_render != '')

        world = article.world
        self.assertTrue(isinstance(world, World))

        author = article.author
        self.assertTrue(isinstance(author, User))

    def testGenres(self):
        world = World(self.client, self.client.world.get('8f312eff-fdcc-49d1-9626-a98af28ada54'))
        for item in world.genres:
            self.assertTrue(isinstance(item, Genre))


if __name__ == '__main__':
    unittest.main()
