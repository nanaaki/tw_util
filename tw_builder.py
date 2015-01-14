from twython import Twython, TwythonError
from settings import *

class TwBuilder(object):
    def __init__(self):
        self.APP_KEY = APP_KEY
        self.APP_SECRET = APP_SECRET
        self.OAUTH_TOKEN = OAUTH_TOKEN
        self.OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRET
        self._tw = Twython(self.APP_KEY, \
                           self.APP_SECRET, \
                           self.OAUTH_TOKEN, \
                           self.OAUTH_TOKEN_SECRET)

    def tw(self):
        return self._tw
