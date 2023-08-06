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


class Genre:

    def __init__(self, metadata: Dict[str, Any]):
        self._metadata = metadata

    @property
    def id(self) -> str:
        """Id of the genre."""
        return self._metadata['id']

    @property
    def name(self) -> str:
        """Name of the genre."""
        return self._metadata['name']
