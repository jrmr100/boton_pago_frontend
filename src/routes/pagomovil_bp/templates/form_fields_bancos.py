from flask_wtf import FlaskForm
from wtforms import SubmitField


class FormFieldsBancos(FlaskForm):
    submit_bancoplaza = SubmitField('REPORTAR PAGO')
    submit_banesco = SubmitField('REPORTAR PAGO')

