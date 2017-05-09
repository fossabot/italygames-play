from .. import oauth


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

    def get_callback(self):
        return url_for('oauth_callback',
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
        self.service = oauth.remote_app('reddit',
            consumer_key=self.consumer_id,
            consumer_secret=self.consumer_secret,
            base_url='https://www.reddit.com/api/v1/',
            request_token_url=None,
            authorize_url='https://www.reddit.com/api/v1/authorize',
            access_token_url='https://www.reddit.com/api/v1/access_token'
        )

    def authorize(self):
        pass

    def callback(self):
        pass
