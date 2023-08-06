# World Anvil API Python Client

The World Anvil API provides endpoints to interact with the World Anvil data base.

[API Documentation](https://www.worldanvil.com/api/aragorn/documentation)

## Installation
The package is published on PYPI and can be installed with pip.

`pip --install pywaclient`

## Usage

This library can be used either by accessing the json data returned by the 
api client or use the class wrapper with properties and access points.

Instantiate the client:

```python
from pywaclient.api import AragornApiClient

client = AragornApiClient(
    '<YourScriptName>',
    '<link-to-your-website-or-bot-repository>', '<version>', os.environ['WA_APPLICATION_KEY'], os.environ['WA_AUTH_TOKEN']
)
```

Load an article:
```python

article_metadata = client.article.get('<article-id>')
```

Create article model:
```python
from pywaclient.models.article import Article

article = Article(client, client.article.get('<article-id>'))
```

The model is a wrapper with some convience properties for the JSON file. Not all fields can be extracted like that, but any fields without an element can be extracted
with the property name as a dictionary accessor:

```python

identifier = article.id
author: User = article.author
world: World = article.world
passcode = article['passcode']
```

