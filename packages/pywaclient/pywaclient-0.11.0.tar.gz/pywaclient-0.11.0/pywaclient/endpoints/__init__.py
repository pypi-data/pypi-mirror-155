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
import json
from typing import Dict, Any, Iterable, Optional

import requests
from requests import RequestException

from pywaclient.exceptions import AccessForbidden, ResourceNotFound, InternalServerException, \
    UnexpectedStatusException, ConnectionException


def _parse_response(path, response) -> str:
    if response.ok:
        data = response.json()
        if 'id' in data:
            return data['id']
    elif response.status_code == 403:
        raise AccessForbidden(path)
    elif response.status_code == 404:
        raise ResourceNotFound(path)
    elif response.status_code == 500:
        raise InternalServerException(path)
    else:
        raise UnexpectedStatusException(response.status_code, response.reason, path)


class Endpoint:

    def __init__(self, client: 'AragornApiClient'):
        self.client = client

    def _request(self, path: str, **kwargs) -> Optional[Dict[str, Any]]:
        try:
            response = requests.get(self.client.base_url + path, params=kwargs, headers=self.client.headers)
            if response.ok:
                return json.loads(response.text)
            elif response.status_code == 403:
                raise AccessForbidden(path)
            elif response.status_code == 404:
                raise ResourceNotFound(path)
            elif response.status_code == 500:
                raise InternalServerException(path)
            else:
                raise UnexpectedStatusException(response.status_code, response.reason, path)
        except RequestException as err:
            raise ConnectionException(str(err))

    def _patch_request(self, path: str, content: Dict[str, Any]) -> str:
        try:
            response = requests.patch(self.client.base_url + path, json=content,
                                      headers=self.client.headers)
            return _parse_response(path, response)
        except RequestException as err:
            raise ConnectionException(str(err))

    def _post_request(self, path: str, content: Dict[str, Any]) -> str:
        try:
            response = requests.post(self.client.base_url + path, json=content,
                                     headers=self.client.headers)
            return _parse_response(path, response)

        except RequestException as err:
            raise ConnectionException(str(err))

    def _delete_request(self, path: str):
        try:
            response = requests.delete(self.client.base_url + path,
                                       headers=self.client.headers)
            return _parse_response(path, response)

        except RequestException as err:
            raise ConnectionException(str(err))

    def _scroll_collection(self, path: str, collection_tag: str, **kwargs) -> Iterable[Dict[str, Any]]:
        limit = 50
        offset = 0
        result = self._request(path, **kwargs)
        if collection_tag in result:
            items = result[collection_tag]
            while len(items) > 0:
                for item in items:
                    yield item
                offset += 1
                kwargs['offset'] = offset * limit

                result = self._request(path, **kwargs)
                if collection_tag not in result:
                    return
                items = result[collection_tag]

    @staticmethod
    def _download_binary(url: str, **kwargs) -> Iterable[bytes]:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=kwargs['chunk_size'] if 'chunk_size' in kwargs else 8192):
                yield chunk
