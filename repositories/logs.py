import os
import datetime
import json
import logging

from collections import namedtuple
from dataclasses import dataclass

import dataset

_use_postgres = True

#Log = namedtuple('Log', ['date', 'brand', 'model', 'classic'])

@dataclass(frozen=True)
class Log:
    log_date: datetime.date
    brand: str
    model: str
    classic: bool

def _connect():
    database_url = os.environ.get('DB_URL', None)

    if not database_url:
        database_url = os.environ.get('DATABASE_URL', None)

    if database_url.startswith('postgres:'):
        database_url = database_url.replace('postgres:', 'postgresql:')
    assert database_url, "No database url defined"
    assert database_url.startswith('postgresql://'), 'Database protocol is incorrect'
    return dataset.connect(database_url)

def _map_log(log_dataset):
    return Log(
        log_date=log_dataset['date'],
        brand=log_dataset.get('brand', None),
        model=log_dataset.get('model', None),
        classic=log_dataset.get('classic', False),
        )

def save(brand, model=None, classic=False, convertible=False):
        postgres_save(brand, model, classic, convertible)

def postgres_save(brand, model=None, classic=False, convertible=False):
    db = _connect()
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