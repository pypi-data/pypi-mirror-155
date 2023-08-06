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
from pywaclient.endpoints import Endpoint


class BlockEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.path = 'block/{0}'

    def get(self, identifier: str, **kwargs) -> Dict[str, Any]:
        """Get a specific block by id.

        :param identifier: Identifier of the block.
        :return: Block metadata.
        """
        return self._request(self.path.format(identifier), **kwargs)
