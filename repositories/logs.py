import os
import datetime
import json
import logging

import dataset

_use_postgres = True


def save(brand, model=None, classic=False, convertible=False):
        postgres_save(brand, model, classic, convertible)

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
