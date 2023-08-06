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


class ArticleEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.path = 'article/{0}'
        self.post_path = 'article'

    def get(self, identifier: str, **kwargs) -> Dict:
        """Get the metadata of a specific article.

        :param identifier: The identifier of the article.
        :keyword load_all_properties: Set to true to retrieve even empty fields. Use only for development.
        :return: article metadata
        """
        if 'load_all_properties' not in kwargs:
            kwargs['load_all_properties'] = False
        return self._request(self.path.format(identifier), **kwargs)

    def patch(self, identifier: str, content: Dict[str, Any]) -> str:
        return self._patch_request(self.path.format(identifier), content)

    def post(self, content: Dict[str, Any]) -> str:
        return self._post_request(self.post_path, content)

    def delete(self, identifier: str):
        self._delete_request(self.path.format(identifier))
