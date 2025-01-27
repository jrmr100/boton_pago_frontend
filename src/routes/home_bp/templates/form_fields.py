from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, Email, Length
from src.utils.validaciones_form import only_numbers


class FormFields(FlaskForm):
    field1 = EmailField('Correo electrónico',
                              validators=[InputRequired(), Email(),
                                          Length(min=1, max=50)])
    field2 = SelectField('CI/RIF:',
                          choices=[],
                          validators=[InputRequired()],
                          render_kw={'style': 'width: 80px; margin-right: 10px;'})
    field3 = StringField('Cédula de identidad',
                             validators=[InputRequired(), Length(min=3, max=40), only_numbers])

    field4 = SubmitField('Aceptar')
