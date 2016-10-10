import os
import json
import logging

import requests
import flask

from flask_sslify import SSLify
from flask.ext.session import Session

import decorators

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

    session = Session()
    app.config['SESSION_TYPE'] = 'redis'
    session.init_app(app)

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

    if form.validate():
        logs.save(form.brand.data, form.model.data)
        flask.flash('Log recorded')

    return flask.redirect(flask.url_for('home'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = int(os.environ.get('PORT', 3000)))
