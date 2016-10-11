import wtforms

class LogForm(wtforms.Form):
    brand = wtforms.StringField('Brand', [wtforms.validators.Optional()])
    brand_free = wtforms.StringField('Brand', [wtforms.validators.Optional()])
    model = wtforms.StringField('Model', [])

    def validate(self):
        if not wtforms.Form.validate(self):
            return False

        if not self.brand.data and not self.brand_free.data:
            return False

        return True