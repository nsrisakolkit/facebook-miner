import facebook
import requests
import pandas as pd
import numpy as np


class FacebookAPI:
    def __init__(self, facebook_app_id, facebook_app_secret, version=None):
        self.facebook_app_id = facebook_app_id
        self.facebook_app_secret = facebook_app_secret
        payload = {'grant_type': 'client_credentials', 'client_id': self.facebook_app_id,
                   'client_secret': self.facebook_app_secret}
        request_token = requests.post('https://graph.facebook.com/oauth/access_token?', params=payload)
        self.access_token = request_token.json()['access_token']
        self.version = version
        if self.version is not None:
            self.facebook_api = facebook.GraphAPI(access_token=self.access_token, version=self.version)
        else:
            self.facebook_api = facebook.GraphAPI(access_token=self.access_token)

    def get_posts(self, page, limit=100):
        fields = 'id,message,created_time,shares,likes.limit(0).summary(true),comments.limit(0).summary(true)'
        posts = self.facebook_api.get_connections(id=page, connection_name='posts', fields=fields, limit=limit)
        post_id = []
        message = []
        created_time = []
        likes_count = []
        shares_count = []
        comments_count = []
        for post in range(limit):
            post_id.append(posts['data'][post]['id'])
            message.append(posts['data'][post]['message'].replace('\n', ' '))
            created_time.append(posts['data'][post]['created_time'][:10] + ' '
                                + posts['data'][post]['created_time'][11:19])
            likes_count.append(posts['data'][post]['likes']['summary']['total_count'])
            if posts['data'][post].get('shares') is None:
                shares_count.append(0)
            else:
                shares_count.append(posts['data'][post]['shares']['count'])
            comments_count.append(posts['data'][post]['comments']['summary']['total_count'])
        page_name_id = self.facebook_api.get_object(id=page, fields='name')
        page_id = [page_name_id['id']]*limit
        page_name = [page_name_id['name']]*limit
        df_posts = pd.DataFrame(np.column_stack([page_id, page_name, post_id, message, created_time, likes_count,
                                                 shares_count, comments_count]),
                                columns=['page_id', 'page_name', 'post_id', 'message', 'post_time', 'likes_count',
                                         'shares_count', 'comments_count'])
        df_posts['post_time'] = pd.to_datetime(df_posts['post_time'], format='%Y-%m-%d %H:%M:%S')
        return df_posts
