from flask_wtf import FlaskForm
from wtforms import EmailField, IntegerField, SubmitField
from wtforms.validators import InputRequired, Email, NumberRange, Length


class FormTemplate(FlaskForm):
    email = EmailField('Correo electrónico',
                              validators=[InputRequired(), Email(),
                                          Length(min=1, max=50)])
    ci = IntegerField('Cédula de identidad',
                             validators=[InputRequired(), NumberRange(min=0)])

    submit = SubmitField("Aceptar")
