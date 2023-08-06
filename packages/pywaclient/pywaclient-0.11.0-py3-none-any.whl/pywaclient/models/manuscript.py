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
from typing import Dict, Any, Iterable, Union

from pywaclient.models.entity import Entity


class ManuscriptPart(Entity):

    def __init__(self, client: 'AragornApiClient', metadata: Dict[str, Any]):
        """

        :param client:
        :param metadata:
        """
        super().__init__(client, metadata)

    @property
    def type(self) -> str:
        """The type of this part. It is one value of folder, text and image."""
        return self._metadata['type']

    @property
    def title(self) -> str:
        """The title of the part."""
        return self._metadata['title'] if self._metadata['title'] is not None else ''


    @property
    def content(self) -> str:
        """The content of this part.

        - Folder: None
        - Text: Text
        - Image: Caption Text
        """
        return self._metadata['content'] if self._metadata['content'] is not None else ''

    @property
    def has_image(self) -> bool:
        """Checks if an image is present or not."""
        return self.type == 'image' and 'image' in self._metadata

    @property
    def image_url(self) -> Union[str, None]:
        """The url of the image if this is an image part."""
        if self.has_image:
            return self._metadata['image']['url']
        else:
            return None

    @property
    def image_id(self) -> Union[int, None]:
        """The id of the image if this is an image part."""
        if self.has_image:
            return self._metadata['image']['id']
        else:
            return None

    def children(self) -> Iterable['ManuscriptPart']:
        if 'children' in self._metadata:
            for key in self._metadata['children']:
                yield ManuscriptPart(self._client, self._metadata['children'][key])

    def to_html(self) -> str:
        if self.type == 'image':
            if self.has_image:
                return f'<img src="{self.image_url}" alt="{self.content}">\n'
            else:
                return ''
        elif self.type == 'text':
            return self.content
        else:
            return f'<h1>{self.title}</h1>\n'


class ManuscriptExport(Entity):

    def __init__(self, client: 'AragornApiClient', metadata: Dict[str, Any], manuscript: 'Manuscript' = None):
        """

        :param client:
        :param metadata:
        """
        super().__init__(client, metadata)
        self._manuscript = manuscript

    @property
    def manuscript(self) -> 'Manuscript':
        if self._manuscript is None:
            return Manuscript.from_id(self._client, self._metadata['manuscript']['id'])
        else:
            return self._manuscript

    @property
    def version(self) -> 'ManuscriptVersion':
        return ManuscriptVersion(self._client, self._metadata['version'])

    @property
    def parts(self) -> Iterable['ManuscriptPart']:
        if 'parts' in self._metadata:
            for key in self._metadata['parts']:
                yield ManuscriptPart(self._client, self._metadata['parts'][key])


class ManuscriptVersion(Entity):

    def __init__(self, client: 'AragornApiClient', metadata: Dict[str, Any]):
        super().__init__(client, metadata)

    @property
    def title(self) -> str:
        return self._metadata['title']

    @property
    def state(self) -> str:
        """"""
        return self._metadata['state']


class Manuscript(Entity):

    @classmethod
    def from_id(cls, client: 'AragornApiClient', identifier: str):
        return Manuscript(client, client.manuscript.get(identifier))

    def __init__(self, client: 'AragornApiClient', metadata: Dict[str, Any]):
        """

        :param client:
        :param metadata:
        .:param author:
        """
        super().__init__(client, metadata)

    @property
    def title(self) -> str:
        """Title of the manuscript.

        :return: manuscript title
        """
        return self._metadata['title']

    @property
    def status(self) -> str:
        """The status of this manuscript (completed / ongoing).

        :return: status
        """
        return self._metadata['status']

    @property
    def author(self) -> 'User':
        """The author of this manuscript.

        :return: User
        """
        # this import is here because of circular imports.
        from pywaclient.models.user import User
        return User(self._client, self._metadata['author']['id'])

    @property
    def active_version(self) -> ManuscriptVersion:
        """Fetches the active version of this manuscript.

        :return: ManuscriptVersion
        """
        return ManuscriptVersion(self._client, self._metadata['active_version'][0])

    @property
    def active_export(self) -> ManuscriptExport:
        """Fetches the export of the active version of this manuscript.

        :return: ManuscriptExport
        """
        return ManuscriptExport(self._client, self._client.manuscript.export_version(self.active_version.id), self)
