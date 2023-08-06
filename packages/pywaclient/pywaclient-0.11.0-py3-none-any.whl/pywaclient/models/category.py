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
from typing import Dict, Any

from pywaclient.models.entity import Entity
from pywaclient.exceptions import NoParentCategoryException


class Category(Entity):

    def __init__(self, client: 'AragornApiClient', metadata: Dict[str, Any]):
        super().__init__(client, metadata)
        self._world = None

    @property
    def title(self) -> str:
        """Title of the category."""
        return self._metadata['title']

    @property
    def url(self) -> str:
        """url of the category."""
        return self._metadata['url']

    @property
    def state(self) -> str:
        """State of the category: public | private."""
        return self._metadata['state']

    @property
    def views(self) -> int:
        """Number of views on the category."""
        views = self._metadata['views']
        return views if views else 0

    @property
    def position(self) -> int:
        """Number of views on the category."""
        position = self._metadata['position']
        return position if position else 0

    @property
    def description(self) -> str:
        """The main description field of the category."""
        description = self._metadata['description']
        return description if description else ""

    @property
    def excerpt(self) -> str:
        """The main excerpt field of the category."""
        excerpt = self._metadata['excerpt']
        return excerpt if excerpt else ""

    @property
    def icon(self) -> str:
        """The main icon field of the category."""
        icon = self._metadata['icon']
        return icon if icon else ""

    @property
    def has_parent_category(self) -> bool:
        """Has this category a parent category?"""
        return 'parent_category' in self._metadata

    @property
    def parent_category(self) -> 'Category':
        """Get the parent category of this category.

        :returns: Parent category
        :raises NoParentCategoryException: No parent category present.
        """
        if self.has_parent_category:
            return Category(self._client, self._client.category.get(self._metadata['parent_category']['id']))
        else:
            raise NoParentCategoryException(f"The category {self.title} has no parent category.")

    @property
    def book_cover(self) -> str:
        """Returns the book cover url or an empty string."""
        if 'book_cover' in self._metadata:
            return self._metadata['book_cover']['url']
        else:
            return ""

    @property
    def page_cover(self) -> str:
        """Returns the page cover url or an empty string."""
        if 'page_cover' in self._metadata:
            return self._metadata['page_cover']['url']
        else:
            return ""

    @property
    def world(self) -> 'World':
        """The world this category is a part of."""
        if self._world is None:
            from pywaclient.models.world import World
            self._world = World(self._client, self._client.world.get(self._metadata['world']['id']))
        return self._world
