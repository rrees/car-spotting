import os
import datetime
import json
import logging

import fieldbook_py as fieldbook

import dataset

fieldbook_config = json.loads(os.environ['FIELDBOOK_CONFIG'])

fieldbook_api = fieldbook.FieldbookClient(fieldbook_config['API_KEY'], fieldbook_config['API_SECRET'], fieldbook_config['URL'])

def save(brand, model=None, classic=False, convertible=False):

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
