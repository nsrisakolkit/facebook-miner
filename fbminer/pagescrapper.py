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

    def get_posts(self, pages, limit=100):
        if type(pages) is not list:
            pages = [pages]
        fields = 'id,message,created_time,shares,likes.limit(0).summary(true),comments.limit(0).summary(true)'
        all_pages = pd.DataFrame(columns=['page_id', 'page_name', 'post_id', 'message', 'post_time', 'likes_count',
                                          'shares_count', 'comments_count'])
        for page in pages:
            posts = self.facebook_api.get_connections(id=page, connection_name='posts', fields=fields, limit=limit)
            post_id = []
            message = []
            created_time = []
            likes_count = []
            shares_count = []
            comments_count = []
            for post in posts['data']:
                post_id.append(post['id'])
                if post.get('message') is None:
                    message.append('')
                else:
                    message.append(post['message'].replace('\n', ' '))
                created_time.append(post['created_time'][:10] + ' ' + post['created_time'][11:19])
                likes_count.append(post['likes']['summary']['total_count'])
                if post.get('shares') is None:
                    shares_count.append(0)
                else:
                    shares_count.append(post['shares']['count'])
                comments_count.append(post['comments']['summary']['total_count'])
            page_name_id = self.facebook_api.get_object(id=page, fields='name')
            page_id = [page_name_id['id']]*len(posts['data'])
            page_name = [page_name_id['name']]*len(posts['data'])
            df_posts = pd.DataFrame(np.column_stack([page_id, page_name, post_id, message, created_time, likes_count,
                                                     shares_count, comments_count]),
                                    columns=['page_id', 'page_name', 'post_id', 'message', 'post_time', 'likes_count',
                                             'shares_count', 'comments_count'])
            df_posts['post_time'] = pd.to_datetime(df_posts['post_time'], format='%Y-%m-%d %H:%M:%S')
            all_pages = all_pages.append(df_posts, ignore_index=True)
        return all_pages

    def get_post_comments(self, post_ids, limit=None):
        if type(post_ids) is not list:
            post_ids = [post_ids]
        fields = 'id,from,message,created_time,likes.limit(0).summary(true),comments.limit(0).summary(true)'
        all_posts = pd.DataFrame(columns=['page_id', 'post_id', 'comment_id', 'user_id', 'message', 'post_time',
                                          'likes_count', 'reply_count'])
        for post_id in post_ids:
            post = self.facebook_api.get_object(id=post_id, fields='from,comments.limit(0).summary(true)')
            page_id = post['from']['id']
            if limit is None:
                limit = post['comments']['summary']['total_count']
            comments = self.facebook_api.get_connections(id=post_id, connection_name='comments', fields=fields,
                                                         limit=limit)
            comment_id = []
            from_user_id = []
            message = []
            created_time = []
            likes_count = []
            replies_count = []
            for comment in comments['data']:
                comment_id.append(comment['id'])
                from_user_id.append(comment['from']['id'])
                if comment.get('message') is None:
                    message.append('')
                else:
                    message.append(comment['message'].replace('/n', ' '))
                created_time.append(comment['created_time'][:10] + ' ' + comment['created_time'][11:19])
                likes_count.append(comment['likes']['summary']['total_count'])
                replies_count.append(comment['comments']['summary']['total_count'])
            list_post_id = [post_id]*len(comments['data'])
            list_page_id = [page_id]*len(comments['data'])
            df_posts = pd.DataFrame(np.column_stack([list_page_id, list_post_id, comment_id, from_user_id, message,
                                                     created_time, likes_count, replies_count]),
                                    columns=['page_id', 'post_id', 'comment_id', 'user_id', 'message', 'post_time',
                                             'likes_count', 'reply_count'])
            all_posts = all_posts.append(df_posts, ignore_index=True)
        return all_posts
