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
from pywaclient.endpoints.secrets import SecretEndpoint
from pywaclient.endpoints.categories import CategoryEndpoint
from pywaclient.endpoints.articles import ArticleEndpoint
from pywaclient.endpoints.blocks import BlockEndpoint
from pywaclient.endpoints.images import ImageEndpoint
from pywaclient.endpoints.manuscripts import ManuscriptEndpoint
from pywaclient.endpoints.users import UserEndpoint
from pywaclient.endpoints.worlds import WorldEndpoint


class AragornApiClient:

    def __init__(self,
                 name: str,
                 url: str,
                 version: str,
                 application_key: str,
                 authentication_token: str,
                 ):
        self.headers = {
            'x-auth-token': authentication_token,
            'x-application-key': application_key,
            'Accept': 'application/json',
            'User-Agent': f'{name} ({url}, {version})'
        }
        self.base_url = 'https://www.worldanvil.com/api/aragorn/'
        self.block = BlockEndpoint(self)
        self.article = ArticleEndpoint(self)
        self.image = ImageEndpoint(self)
        self.manuscript = ManuscriptEndpoint(self)
        self.user = UserEndpoint(self)
        self.secret = SecretEndpoint(self)
        self.world = WorldEndpoint(self)
        self.category = CategoryEndpoint(self)
