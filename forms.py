import wtforms

class LogForm(wtforms.Form):
    brand = wtforms.StringField('Brand', [wtforms.validators.Optional()])
    brand_free = wtforms.StringField('Brand', [wtforms.validators.Optional()])
    model = wtforms.StringField('Model', [])