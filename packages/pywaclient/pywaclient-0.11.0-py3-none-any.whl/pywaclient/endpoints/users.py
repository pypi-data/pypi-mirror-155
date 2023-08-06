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
from typing import Dict, Union, Any, List, Optional
from pywaclient.endpoints import Endpoint


class UserEndpoint(Endpoint):

    def __init__(self, client: 'AragornApiClient'):
        super().__init__(client)
        self.auth_user_path = 'user'
        self.path = 'user/{0}'
        self.path_manuscripts = 'user/{0}/manuscripts'
        self.path_worlds = 'user/{0}/worlds'
        self.authenticated_user_id = self.get()['id']

    def get(self, identifier: Union[str, None] = None) -> Dict[str, Any]:
        """Get a specific user with its identifier or the authenticated user of the access token if
        no identifier is given.

        :param identifier: Identifier of a specific user or None.
        :return: User metadata.
        """
        return self._request(self.auth_user_path if identifier is None else self.path.format(identifier))

    def manuscripts(self, identifier: Union[str, None] = None, **kwargs) -> Optional[List[Dict[str, Any]]]:
        """Get a list of all the manuscripts of the authorized user or the user by id.

        :param identifier: Identifier of a specific user or None.
        :return: List of minimalist manuscript metadata.
        """
        identifier = self.authenticated_user_id if identifier is None else identifier
        path = self.path_manuscripts.format(identifier)
        manuscripts = self._request(path, **kwargs)
        if manuscripts is not None and 'manuscripts' in manuscripts:
            return manuscripts['manuscripts']
        else:
            return None

    def worlds(self, identifier: Union[str, None] = None) -> Optional[List[Dict[str, Any]]]:
        """Get a list of all the worlds of the authorized user or the user by id.

        :param identifier: Identifier of a specific user or None.
        :return: List of minimalist worlds metadata.
        """
        identifier = self.authenticated_user_id if identifier is None else identifier
        path = self.path_worlds.format(identifier)
        worlds_collection = self._request(path)
        if 'worlds' in worlds_collection:
            return worlds_collection['worlds']
        else:
            return None
