import datetime, time
from tw_builder import TwBuilder

class TwUtil(object):
    def __init__(self):
        self.tw = TwBuilder().tw()
        self.NO_LIMIT_MODE = False

    def get_limits(self, resources=""):
        return self.tw.get_application_rate_limit_status(resources=resources)

    def get_all_tweet(self, **params):
        limits = self.get_limits(resources='statuses')
        limits = limits['resources']['statuses']['/statuses/user_timeline']

        tweets = []
        while limits['remaining'] != 0:
            tmp_tweets = self.tw.get_user_timeline(**params)
            tweets.extend(tmp_tweets)
            params['max_id'] = tmp_tweets[params['count']-1 if 'count' in params else 20-1]['id']

            limits['remaining'] = int(self.tw.get_lastfunction_header('x-rate-limit-remaining'))

            if self.NO_LIMIT_MODE and limits['remaining'] == 0:
                reset = int(self.tw.get_lastfunction_header('x-rate-limit-reset'))
                print("{0}:wait api reset {0}sec", datetime.datetime.now() ,reset-int(time.time()))
                time.sleep(reset-int(time.time()))
            print("{0}tweets, {1}remaining".format(len(tweets), limits['remaining']))

        return tweets

    def get_all_follows(self, **params):
        cursor = -1
        limits = self.get_limits('friends')
        limits = limits['resources']['friends']['/friends/list']

        follows_users = []
        while cursor != 0 and limits['remaining']!= 0:
            follows = self.tw.get_friends_list(**params)
            follows_users.extend(follows['users'])
            params['cursor'] = int(follows['next_cursor'])

            limits['remaining'] = int(self.tw.get_lastfunction_header('x-rate-limit-remaining'))

            if self.NO_LIMIT_MODE and limits['remaining'] == 0:
                reset = int(self.tw.get_lastfunction_header('x-rate-limit-reset'))
                print("{0}:wait api reset {0}sec", datetime.datetime.now() ,reset-int(time.time()))
                time.sleep(reset-int(time.time()))
            print("{0}tweets, {1}remaining".format(len(follows), limits['remaining']))

        return follows_users

if __name__ == '__main__':
    tw_util = TwUtil()
    tw_util.NO_LIMIT_MODE = True
    print(tw_util.get_all_tweet(screen_name='nanaaki_77th', count=200))
    print(tw_util.get_all_follows(screen_name='nanaaki_77th', count=200))
