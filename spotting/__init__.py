import os
import json
import logging

import requests
import flask

from flask_sslify import SSLify

import redis

import decorators
import redis_session

import authentication
import config
import forms
import data
from repositories import logs

ENV = os.environ.get("ENV", "PROD")

app = flask.Flask(__name__)
app.secret_key = os.urandom(24)

if not ENV == "DEV":
    sslify = SSLify(app)

if "REDIS_URL" in os.environ:
    redis_instance = redis.from_url(os.environ.get("REDIS_URL"))
    app.session_interface = redis_session.RedisSessionInterface(redis=redis_instance)

@app.route('/')
def index():
    if 'profile' in flask.session:
        return flask.redirect('/home')
    return flask.render_template("index.html", app_config=config.config, callback_url = config.callback_url[ENV])

@app.route('/home')
@decorators.requires_auth
def home():
    user = flask.session['profile']
    return flask.render_template("home.html", user=user, brands=data.brands)

@app.route('/callback')
def authorisation_callback():

    if 'profile' in flask.session:
        return flask.redirect('/home')
    
    code = flask.request.args.get('code')

    user_info = authentication.obtain_user_info(code)

    if user_info:
        flask.session['profile'] = user_info

    return flask.redirect('/home')

@app.route('/forms/log/submission', methods=['POST'])
def log_spot():
    form = forms.LogForm(flask.request.form)

    #logging.info(flask.request.form)

    if form.validate():
        brand = form.brand_free.data if form.brand_free.data else form.brand.data
        model = form.model.data
        logs.save(brand, model)
        flask.flash('Log recorded')
    else:
        logging.warning('Failed to validate form input')
        logging.info(form.errors)

    return flask.redirect(flask.url_for('home'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = int(os.environ.get('PORT', 3000)))
