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
from typing import Dict, Any


class Entity:

    def __init__(self, client: 'AragornApiClient', metadata: Dict[str, Any]):
        self._client = client
        self._metadata = metadata

    @property
    def id(self) -> str:
        return self._metadata['id']

    def to_json(self, indent='    ', ensure_ascii: bool = False) -> str:
        return json.dumps(self._metadata, ensure_ascii=ensure_ascii, indent=indent)

    def __getitem__(self, key):
        return self._metadata[key]

    def __repr__(self):
        return repr(self._metadata)
