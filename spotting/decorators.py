import os
import logging
from functools import wraps

import flask

USER_EMAIL = os.environ.get('USER_EMAIL', None)

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in flask.session:
      # Redirect to Login page here
      return flask.redirect('/')

    user_email = flask.session.get('profile', {}).get('user_email', None)
    #logging.info(user_email)
    
    if not user_email == USER_EMAIL:
        return flask.redirect('/')

    return f(*args, **kwargs)

  return decorated