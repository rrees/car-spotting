import os
import json
import logging

import requests
import flask

import auth0

app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template("index.html")

@app.route('/home')
def home():
	return "Home page"

@app.route('/callback')
def authorisation_callback():
	code = flask.request.args.get('code')

	user_info = auth0.obtain_user_info(code)

	if user_info:
		flask.session['profile'] = user_info

	return flask.redirect('/home')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = int(os.environ.get('PORT', 3000)))
