from flask_wtf import FlaskForm
from wtforms import SubmitField


class FormFields(FlaskForm):
    submit1 = SubmitField('ACEPTAR')
    submit2 = SubmitField('CANCELAR')