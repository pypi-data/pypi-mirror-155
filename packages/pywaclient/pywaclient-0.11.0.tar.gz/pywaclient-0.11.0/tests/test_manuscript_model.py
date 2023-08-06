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
import logging
import os
import sys
import unittest

from pywaclient.api import AragornApiClient
from pywaclient.models.manuscript import Manuscript, ManuscriptPart
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
        self.manuscript = self.client.manuscript.get('4acb220b-0e08-42dc-8753-8ee57d44f0e5')

    def testManuscriptTitle(self):
        manuscript = Manuscript(self.client, self.manuscript)
        self.assertEqual('Test Manuscript', manuscript.title)

    def testManuscriptStatus(self):
        manuscript = Manuscript(self.client, self.manuscript)
        self.assertEqual('ongoing', manuscript.status)

    def testManuscriptAuthor(self):
        manuscript = Manuscript(self.client, self.manuscript)
        self.assertEqual('SoulLink', manuscript.author.username)

    def testManuscriptActiveVersion(self):
        manuscript = Manuscript(self.client, self.manuscript)
        self.assertEqual('{"id": "100fadbf-1ee8-4fc5-8a1a-2ed9dbe7b103", "title": "Draft 1", "state": "private"}',
                         manuscript.active_version.to_json(indent=None))

    def testManuscriptActiveVersionExport(self):
        manuscript = Manuscript(self.client, self.manuscript)
        with open('data/test_manuscript_export.json', 'r') as fp:
            self.assertEqual(fp.read(),
                             manuscript.active_export.to_json(indent=None))

    def testManuscriptExportParts(self):
        manuscript = Manuscript(self.client, self.manuscript)
        export = manuscript.active_export
        self.assertEqual(5, len(list(export.parts)))

    def testManuscriptExportPartTitle(self):
        manuscript = Manuscript(self.client, self.manuscript)
        export = manuscript.active_export
        part = list(export.parts)[0]
        self.assertEqual('Chapter 1', part.title)

    def testManuscriptExportPartType(self):
        manuscript = Manuscript(self.client, self.manuscript)
        export = manuscript.active_export
        part = list(export.parts)[0]
        self.assertEqual('folder', part.type)

    def testManuscriptExportPartContent(self):
        manuscript = Manuscript(self.client, self.manuscript)
        export = manuscript.active_export
        part = list(export.parts)[0]
        self.assertEqual('', part.content)

    def testManuscriptExportPartChildren(self):
        manuscript = Manuscript(self.client, self.manuscript)
        export = manuscript.active_export
        part = list(export.parts)[0]
        self.assertIsInstance(list(part.children())[0], ManuscriptPart)

    def testManuscriptExportPartToHTML(self):
        manuscript = Manuscript(self.client, self.manuscript)
        export = manuscript.active_export
        part = list(export.parts)[0].to_html()
        self.assertEqual('<h1>Chapter 1</h1>\n', part)
