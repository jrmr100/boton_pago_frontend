from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import InputRequired, Length


class FormFields(FlaskForm):
    field1 = StringField('campo1',
                              validators=[InputRequired(),
                                          Length(min=1, max=50)])
    field2 = StringField('Campo2',
                             validators=[InputRequired(),
                                          Length(min=1, max=50)])

    field3 = SubmitField("Aceptar")
