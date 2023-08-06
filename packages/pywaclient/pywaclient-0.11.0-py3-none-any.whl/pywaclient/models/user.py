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
from typing import Optional, Iterable

from pywaclient.models.entity import Entity
from pywaclient.models.manuscript import Manuscript
from pywaclient.models.world import World


class User(Entity):

    def __init__(self, client: 'AragornApiClient', identifier: Optional[str] = None):
        metadata = client.user.get(identifier)
        super().__init__(client, metadata)

    @property
    def username(self) -> str:
        return self._metadata['username']

    def world(self, identifier: str) -> World:
        return World(self._client, self._client.world.get(identifier))

    def worlds(self) -> Iterable[World]:
        result = self._client.user.worlds(self.id)
        if result:
            for world in result:
                world = self._client.world.get(world['id'])
                if world is not None:
                    yield World(self._client, world)
                else:
                    logging.error("Could not retrieve a world because of an error in the API.")

    def manuscripts(self) -> Iterable[Manuscript]:
        result = self._client.user.manuscripts(self.id)
        if result:
            for manuscript in result:
                manuscript = self._client.manuscript.get(manuscript['id'])
                if manuscript is not None:
                    yield Manuscript(self._client, manuscript)
                else:
                    logging.error("Could not retrieve a manuscript because of an error in the API.")


