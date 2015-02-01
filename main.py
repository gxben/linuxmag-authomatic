#!/usr/bin/env python2.7

import sys, os
import functools
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import tornado.autoreload
from flask import Flask, render_template, request, url_for, redirect, session, make_response
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
import json

from config import CONFIG
from config import SECRET

AUTHOMATIC_STATE = 'authomatic:fb:state'

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = SECRET
oauth_sessions= {}

# Instantiate Authomatic.
authomatic = Authomatic(CONFIG, SECRET, report_errors=False)

##################
# Authentication #
##################
def oauth_valid_session(session):
    state = None
    if AUTHOMATIC_STATE in session: state = session[AUTHOMATIC_STATE]
    if state in oauth_sessions: return True
    return False

def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not oauth_valid_session(session):
            return redirect('/login')
        state = session[AUTHOMATIC_STATE]
        kwargs['oauth'] = oauth_sessions[state]
        return func(*args, **kwargs)
    return wrapper

@app.route('/logout', methods=['GET'])
def logout():
    state = session[AUTHOMATIC_STATE]
    if state in oauth_sessions:
        del oauth_sessions[state]
    return redirect('/')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login_provider(provider_name):
    # We need response object for the WerkzeugAdapter.
    response = make_response()

    result = authomatic.login(WerkzeugAdapter(request, response),
                              provider_name,
                              session=session,
                              session_saver=lambda: app.save_session(session, response))

    # If there is no LoginResult object, the login procedure is still pending.
    if result:
        if result.user:
            result.user.update()
            state = session[AUTHOMATIC_STATE]
            oauth_sessions[state] = result
        return redirect('/')

    # Don't forget to return the response.
    return response

########
# Main #
########
@app.route('/')
@login_required
def index(oauth):
    email = oauth.user.email
    if email is None:
        email = ""
    return render_template('index.html', result=oauth, name=oauth.user.name, email=email)

# use UTF-8 encoding instead of unicode to support more characters
reload(sys)
sys.setdefaultencoding("utf-8")

# Run the app.
if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.bind(80)
    http_server.start()

    ioloop = IOLoop().instance()
    tornado.autoreload.start(ioloop)
    ioloop.start()
