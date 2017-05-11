import json
from uuid import uuid4

from flask import current_app, url_for, redirect, request
from rauth import OAuth2Service


class OAuthSignIn(object):
    """
    Abstract class used to gather a single provider object

    Every OAuthSignIn subclass should contain all the authorization logic
    used by the provider to be authenticated with.
    """
    providers = None

    def __init__(self, provider_name):
        """Loads config from instance/config.py"""
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']
        self.useragent = 'italygames:play:0.1'

    def authorize(self):
        """
        Authorize method to implement in subclasses

        The method should handle the initial call to the OAuth provider.
        Ideally set ups and redirects to the authorize endpoint
        """
        raise NotImplementedError("Authorize method not implemented")

    def callback(self):
        """
        Callback method to implement in subclasses

        The method should handle the incoming response from the OAuth provider.
        Receives authentication code and asks for 'me' object to gather id
        and username to be used in the user registration.

        Returns
        -------
        id : str
            Social ID to use for user registration
        username : str
            Username to use for user registration
        """
        raise NotImplementedError("Callback method not implemented")

    def get_callback_url(self):
        """Generates URL for the callback endpoint, to which we expect the
        provider will redirect back once authorized"""
        return url_for('auth.oauth_callback',
                       provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        """Method used to gather all the subclasses and returns the object
        of the provider_name corresponding class"""
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class RedditSignIn(OAuthSignIn):
    """Reddit OAuth provider"""

    def __init__(self):
        """Initializes an OAuth2Service used by rauth"""
        super(RedditSignIn, self).__init__('reddit')
        self.service = OAuth2Service(
            name='reddit',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            base_url='https://oauth.reddit.com/api/v1/',
            authorize_url='https://ssl.reddit.com/api/v1/authorize',
            access_token_url='https://ssl.reddit.com/api/v1/access_token'
        )

    # TODO: choose between temporary and permanent access
    def authorize(self):
        """
        Calls the reddit authorize endpoint.

        Sets up a custom user-agent because Reddit will only handle around 60 calls/mins for each user-agent. Using the default one will result
        in a lot of 429 errors.
        """
        state = str(uuid4())
        response = redirect(self.service.get_authorize_url(
            response_type='code',
            duration='permanent',
            scope='identity',
            state=state,
            redirect_uri=self.get_callback_url())
        )
        response.headers['User-Agent'] = self.useragent

        return response

    # TODO: check STATE parameter back
    def callback(self):
        """
        Handles the reddit callback

        If all went ok, it gets back the authorization code. It then calls
        the 'me' API to get the user identity.
        """
        if 'code' not in request.args:
            return None, None

        headers = {'user-agent': self.useragent}
        data = {
            'grant_type': 'authorization_code',
            'code': request.args['code'],
            'redirect_uri': self.get_callback_url()
        }
        oauth_session = self.service.get_auth_session(
            data=data,
            decoder=json.loads,
            headers=headers,
            auth=(self.consumer_id, self.consumer_secret)
        )
        me = oauth_session.get('me', headers=headers).json()

        return me['id'], me['name']
