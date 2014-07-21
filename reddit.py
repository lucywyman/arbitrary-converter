import urllib2
import json
from types import *
from random import choice

# Get cute picture from reddit for error pages
def getpic(subreddit):
    try:
        url = "http://www.reddit.com/r/" + subreddit + \
            "/top/.json?sort=top&t=week&limit=5"
        r = urllib2.urlopen(url).read()
        data = json.loads(r)

        posts = []

        for post in data[u'data'][u'children']:
            if (post[u'kind'] == u't3' and
                    post[u'data'][u'domain'] == u'i.imgur.com'):
                posts.append(post[u'data'][u'url'])

        if(len(posts) > 0):
            return choice(posts)

    except urllib2.HTTPError, e:
        # print e.code
        return "https://i.imgur.com/uhBWeIE.jpg"
        # in the interest of time, we'll return a safe bet
        # if you want, uncomment these lines to get a different image
        # sleep(1)
        # return getpic(subreddit)
    # None from that sub, just pick /aww
    return getpic("aww")

