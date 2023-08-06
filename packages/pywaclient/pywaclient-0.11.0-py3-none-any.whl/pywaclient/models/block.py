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


class Block(Entity):

    def __init__(self, client: 'AragornApiClient', metadata: Dict[str, Any]):
        super().__init__(client, metadata)

    @property
    def name(self) -> str:
        return self._metadata['name']
