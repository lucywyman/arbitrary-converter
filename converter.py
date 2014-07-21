from flask import Flask, render_template, request
import os
import string
import math
from functions import *
from reddit import *

# Disclaimer: I know this is one big, kind of messy file, but this is
# really just a weekend hack to get introduced to flask.  Feel free to
# play around with the code and send me pull requests, questions, or
# suggestions.

# Create the application
app = Flask(__name__)

# Bring up index page


@app.route('/')
def index():
    return render_template('index.html')


# About page
@app.route('/about')
def about():
    return render_template('about.html')


# Generate convert page with results
@app.route('/convert', methods=['POST', 'GET'])
def convertpage():
    info = getinfo()
    data = process(info[0], info[1], info[2])
    return render_template('/convert.html', number = data[0],
                           base2=data[1], result=data[2])
 

# Fancy error handlers, for fancy error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', image=getpic("aww"),
                           message="404 Error: Page not found")


@app.errorhandler(403)
def forbidden_page(e):
    return render_template('error.html', image=getpic("aww"),
                           message="403 Error: Page forbidden")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', image=getpic("aww"),
                           message="500 Error: Internal Server Error")


# Now, run the app!  Yay!
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
