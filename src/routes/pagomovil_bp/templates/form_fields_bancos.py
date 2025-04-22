from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import InputRequired, Length, DataRequired
from src.utils.validaciones_form import only_numbers, banco_emisor, passport


class pagoMovilBancos(FlaskForm):
    bancos = RadioField(
        'Selecciona el banco destino:',
        choices=[('banco1', 'Banco Plaza'), ('banco2', 'Banesco')],
        validators=[DataRequired(message='Por favor, selecciona un banco.')]
    )
    submit = SubmitField('Siguiente')