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
from typing import Dict, Any, Iterable
from pywaclient.endpoints import Endpoint


class ImageEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.path = 'image/{0}'

    def get(self, identifier: str) -> Dict[str, Any]:
        """Get the metadata for a specific image.

        :param identifier: Identifier of the image.
        :return: Image metadata.
        """
        return self._request(self.path.format(identifier))

    def get_binary(self, identifier: str) -> Iterable[bytes]:
        """Get the image binary by identifier

        :param identifier: Identifier of the image.
        :return: Iterable of image binary chunks.
        """
        metadata = self._request(self.path.format(identifier))
        return Endpoint._download_binary(metadata['url'])
