from flask import Flask, render_template, request
import os

import urllib2
import json
from time import sleep
from random import choice


##Disclaimer: I know this is one big, kind of messy file, but this is really just a weekend hack to get introduced to flask.  Feel free to play around with the code and send me pull requests, questions, or suggestions.

#Create the application
app = Flask(__name__)

#Alphabet dictionary for bases greater than 10
alphabet = {
'a' : 11,
'b' : 12,
'c' : 13,
'd' : 14,
'e' : 15,
'f' : 16,
'g' : 17,
'h' : 18,
'i' : 19,
'j' : 20,
'k' : 21,
'l' : 22,
'm' : 23,
'n' : 24,
'o' : 25,
'p' : 26,
'q' : 27,
'r' : 28,
's' : 29,
't' : 30,
'u' : 31,
'v' : 32,
'w' : 33,
'x' : 34,
'y' : 35,
'z' : 36
}

#Bring up index page
@app.route('/')
def index():
    return render_template('index.html')

#About page
@app.route('/about')
def about():
    return render_template('about.html')

#Generate convert page with results
@app.route('/convert', methods=['POST', 'GET'])
def getinfo():
    newnumber = 0
    """Get information from html form (protip: this is
what request.form does!)"""
    try:
        base1 = int(request.form['base1'])
        base2 = int(request.form['base2'])
    except ValueError:
        return render_template('index.html', error=1)
    if ((base1<-36 or (base1>-1 and base1<1) or base1>36) or (base2<-36 or (base2>-1 and base2<1) or base2>36)):
        return render_template('index.html', error=1)
    """Number can't be forced to be int since it may have
base greater than 10.  Python automatically types all
input as string, so then all we have to do is make sure
it's lower case so that the dictionary will work."""
    number = request.form['number'].lower()
    """If the first base is greater than 10, convert number to decimal
and change base1 to base 10.  Kind of a cheat, but it works."""
    if (base1 > 10):
        newnumber = int(number, base1)
        base1 = 10
    else:
        newnumber = number
    result = convert(base1, base2, newnumber)
    return render_template('/convert.html', number=number, base2=base2, result=result)

    """I got this algorithm from a great stackoverflow post here
(it's not just copy paste)
http://cs.stackexchange.com/questions/10318/the-math-behind-converting-from-any-base-to-any-base-without-going-through-base"""
def toDigits(number, base2):
    result = []
    rem = 0
    while number!=0:
        rem = number%base2
        number = number//base2
        #Uncomment at your own risk
        #number, rem = divmod(number, base2)
        if (rem < 0):
            number = number+1
            rem = rem+(-1*base2)
        result.insert(0, rem)
    count = 0
    for digit in result:
        count += 1
        if (digit > 10):
            result[count-1] = str(unichr(int(digit)+86))
    """Since the number is now an array, we convert it to a string,
concatenate the string, then change it back to an int"""
    result = str(''.join(map(str, result)))
    return result

def fromDigits(number, base1):
    s = str(number)
    digits = []
    n = 0
    for digit in s:
        digits.append(int(digit))
    for d in digits:
        n = base1*n+d
    return n

#Now, using these two functions, we can actually convert stuff!
def convert(base1, base2, number):
    result = toDigits(fromDigits(number, base1), base2)
    return result

#Get cute picture from reddit for error pages
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

#Fancy error handlers, for fancy error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', image=getpic("aww"), message="404 Error: Page not found")

@app.errorhandler(403)
def forbidden_page(e):
    return render_template('error.html', image=getpic("aww"), message="403 Error: Page forbidden")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', image=getpic("aww"), message="500 Error: Internal Server Error")

#Now, run the app!  Yay!
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
