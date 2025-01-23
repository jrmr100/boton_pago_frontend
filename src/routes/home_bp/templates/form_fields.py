from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from src.utils.validaciones_form import only_numbers


class FormFields(FlaskForm):
    field1 = EmailField('Correo electrónico',
                              validators=[InputRequired(), Email(),
                                          Length(min=1, max=50)])
    field2 = StringField('Cédula de identidad',
                             validators=[InputRequired(), Length(min=3, max=40), only_numbers])

    field3 = SubmitField("Aceptar")
