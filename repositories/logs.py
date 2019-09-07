import os
import datetime
import json
import logging

import dataset

_use_postgres = True


def _connect():
    database_url = os.environ.get('DATABASE_URL', None)
    assert database_url, "No database url defined"
    return dataset.connect(database_url)

def _map_log(log_dataset):
    return log_dataset

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

def recent():
    db = _connect()
    logs_table = db['logs']

    def results_generator(log_query):
        for log in log_query:
            yield _map_log(log)

    return results_generator(logs_table.find(order_by=['-id'], _limit=10))