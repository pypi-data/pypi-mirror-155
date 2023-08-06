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

from pywaclient.api import AragornApiClient


class TestWorldEndpoint(unittest.TestCase):

    def setUp(self):
        self.client = AragornApiClient(
            name='TEST APPLICATION',
            url='https://gitlab.com/SoulLink/world-anvil-api-client',
            application_key=os.environ.get('WA_APPLICATION_KEY'),
            authentication_token=os.environ.get('WA_AUTH_TOKEN'),
            version='0.1.0'
        )

    def testCategoriesGenerator(self):
        categories = self.client.world.categories('daae0a12-f3c3-4978-b571-b5313e3c1741')
        for category in categories:
            self.assertIn('title', category)

    def test_articles_list(self):
        for article in self.client.world.articles('daae0a12-f3c3-4978-b571-b5313e3c1741'):
            if article['id'] == '48d301ff-9547-4593-8647-bea70070dc6c':
                self.assertTrue(False)

    def test_patch_world(self):
        content = {
            'name': 'API Client Test World',
            'state': 'public',
            'subtitle': 'Subtitle',
            'description': 'This is a description of the world. This world is used to test the API.',
            'copyright': 'No copyright. Its all random stuff anyway...',
            'global_announcement':
                '[h4]Global Announcement[/h4]\nThis text appears in every article at the top of the sidebar.',
            'global_header': '[center]Global Header[/h4]',
            'global_sidebar_footer': '[h4]See Also[/h4]',
            'global_article_introduction': 'This World is for test purposes only. Nothing to see here!',
            'world_sidebar_content': 'What is this?',
            'display_css': '/* A comment for CSS */',
            'display_panel_css': '/* A comment for CSS */',
            'tags': '#TEST,#DONOTCLICK'
        }
        response = self.client.world.patch('daae0a12-f3c3-4978-b571-b5313e3c1741', content)
        self.assertEqual(response, 'daae0a12-f3c3-4978-b571-b5313e3c1741')

    def test_illegal_state(self):
        content = {
            'state': 'illegal'
        }
        response = self.client.world.patch('daae0a12-f3c3-4978-b571-b5313e3c1741', content)
        self.assertEqual(response, 'daae0a12-f3c3-4978-b571-b5313e3c1741')

    def test_secrets(self):
        response = self.client.world.secrets('daae0a12-f3c3-4978-b571-b5313e3c1741')
        for secret in response:
            self.assertIn('title', secret)


if __name__ == '__main__':
    unittest.main()
