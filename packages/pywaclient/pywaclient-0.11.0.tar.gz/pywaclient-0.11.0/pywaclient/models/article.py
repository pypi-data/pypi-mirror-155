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
from typing import Dict, Any, List, Union

from pywaclient.models.entity import Entity


class Article(Entity):

    def __init__(self, client: 'AragornApiClient', metadata: Dict[str, Any]):
        super().__init__(client, metadata)
        if 'fullRender' in self._metadata:
            self._full_render = self._metadata['fullRender']
            del self._metadata['fullRender']
        else:
            self._full_render = ""

    @property
    def title(self) -> str:
        return self._metadata['title']

    @property
    def template(self) -> str:
        return self._metadata['template']

    @property
    def is_draft(self) -> bool:
        return self._metadata['isDraft']

    @property
    def is_wip(self) -> bool:
        return self._metadata['isWip']

    @property
    def state(self) -> str:
        """State of the article: 'private' or 'public'."""
        return self._metadata['state']

    @property
    def wordcount(self) -> int:
        """Wordcount within the article."""
        return self._metadata['wordcount']

    @property
    def url(self) -> str:
        """Absolute url of the article."""
        if 'url' in self._metadata:
            return self._metadata['url']
        else:
            return ''

    @property
    def tags(self) -> List[str]:
        """A list of all the tags on this article."""
        tags = self._metadata['tags']
        if tags is None:
            return list()
        else:
            return tags.split(',')

    @property
    def last_update(self) -> str:
        """The date when the article was update the last time."""
        if 'lastUpdate' in self._metadata and 'date' in self._metadata['lastUpdate']:
            return self._metadata['lastUpdate']['date']
        elif 'updateDate' in self._metadata and 'date' in self._metadata['updateDate']:
            return self._metadata['updateDate']['date']
        else:
            return ''

    @property
    def creation_date(self) -> str:
        """The date when this article was created."""
        if 'creationDate' in self._metadata:
            value = self._metadata['creationDate']
            if value is None:
                return ''
            else:
                return self._metadata['creationDate']['date']
        else:
            return ''

    @property
    def notification_date(self) -> str:
        """The date when the last notification was sent out."""
        if 'notificationDate' in self._metadata:
            value = self._metadata['notificationDate']
            if value is None:
                return ''
            else:
                return self._metadata['notificationDate']['date']
        else:
            return ''

    @property
    def publication_date(self) -> str:
        """The date when the last notification was sent out."""
        if 'publicationDate' in self._metadata:
            value = self._metadata['publicationDate']
            if value is None:
                return ''
            else:
                return self._metadata['publicationDate']['date']
        else:
            return ''

    @property
    def has_category(self) -> bool:
        return 'category' in self._metadata

    @property
    def category_title(self) -> str:
        if 'category' in self._metadata:
            return self._metadata['category']['title']
        else:
            return ''

    @property
    def category_id(self) -> str:
        if 'category' in self._metadata:
            return self._metadata['category']['id']
        else:
            return ''

    @property
    def category(self) -> Union['Category', None]:
        if self.has_category:
            from pywaclient.models.category import Category
            return Category(self._client, self._client.category.get(self.category_id))
        else:
            return None

    @property
    def has_parent_article(self) -> bool:
        if 'relations' in self._metadata:
            return 'articleParent' in self._metadata['relations']
        else:
            return False

    @property
    def parent_article_id(self) -> str:
        """Returns the parent article id or an empty string if it is not defined."""
        if self.has_parent_article:
            try:
                return self._metadata['relations']['articleParent']['items']['id']
            except KeyError:
                return self._metadata['relations']['articleParent']['id']
        else:
            ''

    @property
    def parent_article_title(self) -> str:
        """Returns the parent article title or an empty string if it is not defined."""
        if self.has_parent_article:
            try:
                return self._metadata['relations']['articleParent']['items']['title']
            except KeyError:
                return self._metadata['relations']['articleParent']['title']
        else:
            ''

    def get_parent_article(self) -> Union['Article', None]:
        """Get the model of the parent article in full. This makes a  GET request to WorldAnvil."""
        if self.has_parent_article:
            identifier = self.parent_article_id
            if identifier == '':
                return None
            return Article(self._client, self._client.article.get(identifier))
        else:
            return None

    @property
    def author_id(self) -> str:
        return self._metadata['author']['id']

    @property
    def author(self) -> 'User':
        from pywaclient.models.user import User
        return User(self._client, self.author_id)

    @property
    def world_id(self) -> str:
        return self._metadata['world']['id']

    @property
    def world(self) -> 'World':
        from pywaclient.models.world import World
        return World(self._client, self._client.world.get(self.world_id))

    @property
    def full_render(self) -> str:
        return self._full_render

    @property
    def excerpt(self) -> str:
        if 'excerpt' in self._metadata:
            return self._metadata['excerpt']
        else:
            return ''

    def to_json(self, indent='    ', ensure_ascii: bool = False, include_full_render: bool = False) -> str:
        if include_full_render:
            self._metadata['fullRender'] = self._full_render
        return super().to_json(indent, ensure_ascii)
