from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from wtforms.validators import DataRequired


class FormFieldsBancos(FlaskForm):
    submit_bancoplaza = SubmitField('REPORTAR PAGO')
    submit_banesco = SubmitField('REPORTAR PAGO')
