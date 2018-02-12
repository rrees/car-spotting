import os
import json
import logging
import datetime
import re

import requests
import flask

from flask_sslify import SSLify

import redis

import decorators
import redis_session

import spotting.authentication as authentication
import spotting.config as config
import forms

import data

from repositories import logs

ENV = os.environ.get("ENV", "PROD")

app = flask.Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

app.config.update({
    'PERMANENT_SESSION_LIFETIME': datetime.timedelta(days=30),
    'SESSION_COOKIE_SECURE': True if not ENV == "DEV" else False
    })


if not ENV == "DEV":
    sslify = SSLify(app)

if "REDIS_URL" in os.environ:
    redis_instance = redis.from_url(os.environ.get("REDIS_URL"))

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
    #logging.info(user_info)

    if user_info:
        flask.session.permanent = True
        flask.session['profile'] = {
            "user_email": user_info['email']
        }
        return flask.redirect('/home')

    return flask.redirect('/login')

@app.route('/forms/log/submission', methods=['POST'])
def log_spot():
    form = forms.LogForm(flask.request.form)

    #logging.info(flask.request.form)
    if form.validate():
        brand = form.brand_free.data if form.brand_free.data else form.brand.data
        model = form.model.data
        classic = form.classic.data
        convertible = form.convertible.data
        logs.save(brand, model, classic, convertible)
        flask.flash('Log recorded', 'success')
    else:
        logging.warning('Failed to validate form input')
        logging.info(form.errors)

    return flask.redirect(flask.url_for('home'))

@app.route('/api/brand/<brand_name>/models/suggestions')
def models_lookup(brand_name):

    models = [] if not brand_name else data.models.get(brand_name.lower(), [])

    return flask.jsonify({"models" : models})

@app.route('/api/brand/<brand_name>/models/sub-types/suggestions')
def model_sub_types_lookup(brand_name):

    models = [] if not brand_name else data.model_sub_types.get(brand_name.lower(), [])

    return flask.jsonify({"models" : models})

@app.route('/api/brands/<brand_prefix>/suggestions')
def infrequent_brands_lookup(brand_prefix):
    brands = [] if not brand_prefix else [brand for brand in data.infrequent_brands if re.match(brand_prefix, brand, flags=re.IGNORECASE)]

    return flask.jsonify({"brands" : brands})

@app.route('/manifest.json')
def web_manifest():
    manifest = {
        "short_name": "Car Spotter",
        "name": "Car Spotter",
        "start_url": "/",
        "orientation": "portrait",
    }

    return flask.jsonify(manifest)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = int(os.environ.get('PORT', 3000)))
