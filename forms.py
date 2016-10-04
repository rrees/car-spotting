import wtforms

class LogForm(wtforms.Form):
    brand = wtforms.StringField('Brand', [wtforms.validators.DataRequired()])
    model = wtforms.StringField('Model', [])