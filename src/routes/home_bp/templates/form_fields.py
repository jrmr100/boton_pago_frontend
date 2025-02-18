from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, Email, Length
from src.utils.validaciones_form import only_numbers


class FormFields(FlaskForm):
    email = EmailField('Correo electrónico',
                              validators=[InputRequired(), Email(),
                                          Length(min=1, max=50)])
    tipo_id = SelectField('CI/RIF:',
                          render_kw={'style': 'width: 80px; margin-right: 10px;'})
    ci = StringField('Cédula de identidad',
                             validators=[InputRequired(), Length(min=3, max=40), only_numbers])

    submit = SubmitField('Aceptar')
