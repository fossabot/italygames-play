import json
from uuid import uuid4

from flask import current_app, url_for, redirect, request
from rauth import OAuth2Service


# TODO: comments
class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        raise NotImplementedError("Authorize method not implemented")

    def callback(self):
        raise NotImplementedError("Callback method not implemented")

    def get_callback_url(self):
        return url_for('auth.oauth_callback',
                       provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class RedditSignIn(OAuthSignIn):
    def __init__(self):
        super(RedditSignIn, self).__init__('reddit')
        self.service = OAuth2Service(
            name='reddit',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            base_url='https://www.reddit.com/api/v1/',
            authorize_url='https://www.reddit.com/api/v1/authorize',
            access_token_url='https://www.reddit.com/api/v1/access_token'
        )

    # TODO: choose between temporary and permanent access
    def authorize(self):
        state = str(uuid4())
        return redirect(self.service.get_authorize_url(
            response_type='code',
            duration='permanent',
            scope='identity',
            state=state,
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None

        data = {
            'grant_type': 'authorization_code',
            'code': request.args['code'],
            'redirect_uri': self.get_callback_url()
        }
        oauth_session = self.service.get_auth_session(data=data, decoder=decode_json)
        me = oauth_session.get('me')

        return (me.get('id'), me.get('name'))
