import os
import datetime
import json
import logging

import fieldbook_py as fieldbook

import dataset

_use_fieldbook = False
_use_postgres = True

fieldbook_config = json.loads(os.environ['FIELDBOOK_CONFIG'])

fieldbook_api = fieldbook.FieldbookClient(fieldbook_config['API_KEY'], fieldbook_config['API_SECRET'], fieldbook_config['URL'])



def save(brand, model=None, classic=False, convertible=False):
    if(_use_fieldbook):
        fieldbook_save(brand, model, classic, convertible)

    if _use_postgres:
        postgres_save(brand, model, classic, convertible)

def fieldbook_save(brand, model=None, classic=False, convertible=False):
    iso_now = datetime.date.today().isoformat()

    log_data = {
        'date': iso_now,
        'brand': brand,
        'classic': classic,
        'convertible': convertible,
    }

    if model:
        log_data['model'] = model

    return fieldbook_api.add_row('logs', log_data)

def postgres_save(brand, model=None, classic=False, convertible=False):
    database_url = os.environ.get('DATABASE_URL', None)
    assert database_url, "No database url defined"
    db = dataset.connect(database_url)
    logs_table = db['logs']

    now = datetime.date.today()

    log_data = {
        'date': now,
        'brand': brand,
        'classic': classic,
        'convertible': convertible,
    }

    if model:
        log_data['model'] = model

    pk = logs_table.insert(log_data)

    return pk
