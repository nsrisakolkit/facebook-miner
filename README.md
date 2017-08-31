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

Use function .get_posts to get posts of specific pages. Enter the page name (name in URL) or page ID. This input can be list of pages or just one page. The limit is the number of maximum recent posts for each page. The result is in data frame format.
```python
posts = facebook_api.get_posts(pages=['DramaAdd', 'ejeab'], limit=100)
# or
posts = facebook_api.get_posts(pages='DramaAdd', limit=100)
```

Use function .get_post_comments to get comments in specific posts. Set the argument 'posts' equals to post ID or list of post ID The limit is maximum recent comments (default or None mean get all comments). This function doesn't return the sub-comments. The result is also in data  frame format.
```python
comments = facebook_api.get_post_comments(post_ids=['141108613290_10155828741308291', '1544278182503962_1930411163890660'], limit=None)
```

