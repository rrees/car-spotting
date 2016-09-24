import os
import json
import logging

import requests
import flask

from flask_sslify import SSLify

import decorators

import authentication
import config

ENV = os.environ.get("ENV", "PROD")

app = flask.Flask(__name__)
app.secret_key = os.urandom(24)


if not ENV == "DEV":
	sslify = SSLify(app)

@app.route('/')
def index():
    return flask.render_template("index.html", config=config.config, callback_url = config.callback_url[ENV])

@app.route('/home')
@decorators.requires_auth
def home():
	user = flask.session['profile']
	return flask.render_template("home.html", user=user)

@app.route('/callback')
def authorisation_callback():
	code = flask.request.args.get('code')

	user_info = authentication.obtain_user_info(code)

	if user_info:
		flask.session['profile'] = user_info

	return flask.redirect('/home')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = int(os.environ.get('PORT', 3000)))
