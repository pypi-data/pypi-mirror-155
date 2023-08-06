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
from typing import Dict, Any, List

from pywaclient.models.entity import Entity


class Secret(Entity):

    def __init__(self, client: 'AragornApiClient', metadata: Dict[str, Any]):
        super().__init__(client, metadata)

    @property
    def title(self) -> str:
        return self._metadata['title']

    @property
    def content(self) -> str:
        return self._metadata['content']

    @property
    def content_parsed(self) -> str:
        return self._metadata['content_parsed']

    @property
    def state(self) -> str:
        return self._metadata['state']

    @property
    def tags(self) -> List[str]:
        return self._metadata['tags'].split(',')

    @property
    def author_id(self) -> str:
        return self._metadata['author']['id']

    @property
    def author(self) -> 'User':
        from pywaclient.models.user import User
        return User(self._client, self.author_id)

    @property
    def subscriber_groups(self) -> List[Dict[str, str]]:
        return self._metadata['subscriber_groups']
