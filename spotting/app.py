import os
import json
import logging
import datetime
import re

import requests
import flask

from spotting import decorators

from .auth_password import decorators as auth_decorators
from .auth_password.routes import auth_routes

from spotting import forms

from spotting import data

from repositories import logs

from spotting import handlers

ENV = os.environ.get("ENV", "PROD")

app = flask.Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

app.config.update(
    {
        "PERMANENT_SESSION_LIFETIME": datetime.timedelta(days=30),
        "SESSION_COOKIE_SECURE": True if not ENV == "DEV" else False,
    }
)

routes = auth_routes

for path, endpoint, handler, methods in routes:
    app.add_url_rule(path, endpoint, handler, methods=methods)


@app.route("/")
def index():
    if "email" in flask.session:
        return flask.redirect("/home")
    return flask.render_template("index.html")


@app.route("/home")
@auth_decorators.login_required
def home():
    return flask.render_template("home.html", brands=data.brands)


@app.route("/forms/log/submission", methods=["POST"])
@auth_decorators.login_required
def log_spot():
    form = forms.LogForm(flask.request.form)

    # logging.info(flask.request.form)
    if form.validate():
        brand = form.brand_free.data if form.brand_free.data else form.brand.data
        model = form.model.data
        classic = form.classic.data
        convertible = form.convertible.data
        logs.save(brand, model, classic, convertible)
        flask.flash("Log recorded", "success")
    else:
        logging.warning("Failed to validate form input")
        logging.info(form.errors)

    return flask.redirect(flask.url_for("home"))


@app.route("/api/brand/<brand_name>/models/suggestions")
def models_lookup(brand_name):
    models = [] if not brand_name else data.models.get(brand_name.lower(), [])

    return flask.jsonify({"models": models})


@app.route("/api/brand/<brand_name>/models/sub-types/suggestions")
def model_sub_types_lookup(brand_name):
    models = [] if not brand_name else data.model_sub_types.get(brand_name.lower(), [])

    return flask.jsonify({"models": models})


@app.route("/api/brands/<brand_prefix>/suggestions")
def infrequent_brands_lookup(brand_prefix):
    brands = (
        []
        if not brand_prefix
        else [
            brand
            for brand in data.infrequent_brands
            if re.match(brand_prefix, brand, flags=re.IGNORECASE)
        ]
    )

    return flask.jsonify({"brands": brands})


@app.route("/manifest.json")
def web_manifest():
    manifest = {
        "short_name": "Spotting",
        "name": "Car Spotter",
        "start_url": "/",
        "orientation": "portrait",
        "background_color": "white",
        "icons": [
            {
                "src": "/static/images/icon.png",
                "sizes": "1024x1024",
                "type": "image/png",
            },
            {
                "src": "/static/images/icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
            },
        ],
    }

    return flask.jsonify(manifest)


@app.route("/recent")
def recent_logs():
    recent_logs = logs.recent()
    return handlers.recent_logs(recent_logs=recent_logs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
