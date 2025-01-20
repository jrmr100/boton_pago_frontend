from flask_wtf import FlaskForm
from wtforms import EmailField, IntegerField
from wtforms.validators import InputRequired, Email, NumberRange, Length


class home_form(FlaskForm):
    client_email = EmailField('Correo electrónico',
                              validators=[InputRequired(), Email(),
                                          Length(min=1, max=50)])
    client_ci = IntegerField('Cedula de identidad',
                             validators=[InputRequired(), NumberRange(min=0)])