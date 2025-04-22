from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, DataRequired
from src.utils.validaciones_form import only_numbers, banco_emisor, passport


class FormFields(FlaskForm):
    entity = SelectField('Banco Emisor: ',
                         choices=[],
                         validators=[InputRequired(),
                                     banco_emisor])

    tipo_id = SelectField('CI/RIF del pagador: ',
                          choices=[],
                          validators=[InputRequired()],
                          render_kw={'style': 'width: 80px; margin-right: 10px;'})

    payerID = StringField("", validators=[DataRequired(),
                                          Length(min=2, max=20), passport],
                          render_kw={'placeholder': '123456789',
                                     "title": "Ingrese la información del ID"})

    tipo_phone = SelectField('Teléfono del pagador: ',
                             choices=[],
                             validators=[InputRequired()],
                             render_kw={'style': 'width: 80px; margin-right: 10px;'})

    payerPhone = StringField('',
                             validators=[DataRequired(),
                                         Length(min=5, max=7), only_numbers],
                             render_kw={'placeholder': '1234567', "title": "Solo números, ejem: 1234567"})

    order = StringField('Número de referencia (Últimos 6 dígitos):',
                        validators=[DataRequired(),
                                    Length(min=6, max=6)],
                        render_kw={"title": "Ultimos 6 digitos"})