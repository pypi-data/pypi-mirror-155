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
from typing import Dict, List, Any, Union
from pywaclient.endpoints import Endpoint


class ManuscriptEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.path = 'manuscript/{0}'
        self.path_version = 'manuscript/version/{0}'
        self.path_version_export = 'manuscript/version/{0}/export'

    def get(self, identifier: str) -> Dict[str, Any]:
        """Get a manuscript by id.

        :param identifier: Identifier of the manuscript.
        :return: Manuscript metadata.
        """
        return self._request(self.path.format(identifier))

    def get_active_version(self, identifier: str) -> Dict[str, str]:
        """Get the current active version of the manuscript.

        :param identifier: Identifier of the manuscript.
        :return: Manuscript version metadata.
        """
        return self.get(identifier)['active_version'][0]

    def get_versions(self, identifier: str) -> List[Dict[str, str]]:
        """Get the versions of a specific manuscript.

        :param identifier: Identifier of the manuscript.
        :return: List of manuscript version metadata.
        """
        return self.get(identifier)['versions']

    def get_version(self, identifier: str) -> Dict[str, str]:
        """Get the specific manuscript version metadata.

        :param identifier: Identifier of the manuscript version.
        :return: Manuscript version metadata.
        """
        return self._request(self.path_version.format(identifier))

    def export(self, identifier: str) -> Dict[str, Any]:
        """Export the content of the active manuscript version.

        - Exports at most four levels of folders and scenes (e.g. Act -> Chapter -> Section -> Scene).
        - Ignores any folders and scenes not under the manuscript root folder.

        :param identifier: Identifier of the manuscript.
        :return: Parts of the active manuscript version with content.
        """
        return self.export_version(self.get_active_version(identifier)['id'])

    def export_version(self, identifier: str) -> Union[Dict[str, Any], None]:
        """Export the content of a specific manuscript version.

        - Exports at most four levels of folders and scenes.
        - Ignores any folders and scenes not under the manuscript root folder.

        :param identifier: Identifier of the manuscript version.
        :return: Parts of the manuscript version with content or none if there are no parts.
        """
        return self._request(self.path_version_export.format(identifier))
