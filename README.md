# Facebook Miner
Mining Facebook data using Facebook Graph API with Python

## How to use
First, sign up for [Facebook for Developer](https://developers.facebook.com/) to get your application ID and application secret. Then, in python, import this module.
```python
from fbminer import FacebookAPI
```

Enter the Facebook application ID, secret, and version of Facebook Graph API as follows.
```python
facebook_app_id = ''
facebook_app_secret = ''
graph_api_version = 2.10
facebook_api = FacebookAPI(facebook_app_id, facebook_app_secret, graph_api_version)
```

Enter the page name (name in URL) or page ID; and the number of post you want. The result is in data frame format.
```python
drama_posts = facebook_api.get_posts('DramaAdd', 100)
```
