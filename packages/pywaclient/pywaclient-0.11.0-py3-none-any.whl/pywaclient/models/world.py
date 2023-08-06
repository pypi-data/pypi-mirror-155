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
from typing import Optional, Dict, Iterable, List

from pywaclient.exceptions import AccessForbidden, InternalServerException
from pywaclient.models.entity import Entity
from pywaclient.models.genre import Genre
from pywaclient.models.article import Article
from pywaclient.models.category import Category
from pywaclient.models.block import Block
from pywaclient.models.secret import Secret


class World(Entity):

    def __init__(self, client: 'AragornApiClient', metadata: Dict[str, str]):
        super().__init__(client, metadata)

    @property
    def name(self) -> str:
        """Get the name of the world"""
        return self._metadata['name']

    @name.setter
    def name(self, name: str, update: bool = True):
        self._metadata['name'] = name
        if update:
            self._client.world.patch(self.id, {'name': name})

    @property
    def url(self) -> str:
        """Absolute url to the worlds homepage."""
        return self._metadata['url']

    @property
    def display_css(self) -> Optional[str]:
        """Property to get the world CSS if present.

        :return: Returns the CSS or None
        """
        if 'display_css' in self._metadata and self._metadata['display_css']:
            return self._metadata['display_css']
        else:
            return None

    @display_css.setter
    def display_css(self, css: str, update: bool = True):
        self._metadata['display_css'] = css
        if update:
            self._client.world.patch(self.id, {'display_css': css})

    @property
    def locale(self) -> str:
        """The language setting of this world as code (e.g. en, de, es etc)."""
        return self._metadata['locale']

    @property
    def genres(self) -> List[Genre]:
        """The genres of this world."""
        if 'genres' in self._metadata:
            for genre in self._metadata['genres']:
                yield Genre(genre)
        else:
            return []

    def categories(self) -> Iterable['Category']:
        for category in self._client.world.categories(self.id):
            if category is not None:
                yield Category(self._client, category)

    def articles(self) -> Iterable[Article]:
        for article in self._client.world.articles(self.id):
            try:
                article = self._client.article.get(article['id'], return_error=False)
                if article is not None:
                    yield Article(self._client, article)
            except AccessForbidden as err:
                logging.error(f"Access Forbidden: {err}.")
                yield None

    def blocks(self) -> Iterable[Block]:
        for block in self._client.world.blocks(self.id):
            try:
                block = self._client.block.get(block['id'], return_error=False)
                if block is not None:
                    yield Block(self._client, block)
            except InternalServerException as err:
                logging.error(f"Internal Server Error: {err}")

    def secrets(self) -> Iterable[Secret]:
        for secret in self._client.world.secrets(self.id):
            try:
                secret = self._client.secret.get(secret['id'], return_error=False)
                if secret is not None:
                    yield Secret(self._client, secret)
            except InternalServerException as err:
                logging.error(f"Internal Server Error: {err}")