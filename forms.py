from starlette_wtf import StarletteForm
from wtforms import StringField, IntegerField, TextField, PasswordField, validators
#from wtforms.validators import DataRequired, Email, EqualTo

class BankTransfer(StarletteForm):
    iban = StringField(id='iban', validators=[validators.InputRequired('zadejte svuj IBAN ucet')])
    currency = StringField(id='currency', validators=[validators.InputRequired()])
    amount = IntegerField(id='amount', validators=[validators.InputRequired(), validators.NumberRange(min=0, max=50000, message="maximalni suma je 50 000")])
    vs = IntegerField(id='vs')
    message = StringField(id='message', validators=[validators.Length(min=0, max=35, message="maximalni pocet znaku je 35")])

""" class BankTransfer(StarletteForm):
    iban = StringField(id='iban', validators=[validators.InputRequired()])
    currency = StringField(id='currency',validators=[validators.InputRequired()])
    amount = StringField(id='amount',validators=[validators.InputRequired(), validators.NumberRange(min=0, max=50000)])
    vs = StringField(id='vs',validators=[validators.InputRequired()])
    message = StringField(id='message',validators=[validators.Length(min=0, max=35)]) """    