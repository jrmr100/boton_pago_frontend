from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, FloatField
from wtforms.validators import InputRequired, Length, DataRequired
from src.utils.validaciones_form import only_numbers, banco_emisor, passport, monto_pm
from datetime import datetime


class FormFieldsTc(FlaskForm):

    tipo_id = SelectField('CI/RIF del pagador: ',
                          choices=[],
                          validators=[InputRequired()],
                          render_kw={'style': 'width: 80px; margin-right: 10px;'})

    payerID = StringField("", validators=[DataRequired(),
                                          Length(min=2, max=20), passport],
                          render_kw={'placeholder': '123456789',
                                     "title": "Ingrese la información del ID"})

    fecha_pago = DateField('Fecha del pago:',
                           default=datetime.now(),
                           validators=[DataRequired()])

    banco_emisor = SelectField('Banco Emisor: ',
                         choices=[],
                         validators=[InputRequired(),
                                     banco_emisor])
    referencia = StringField('Número de referencia (Últimos 6 dígitos):',
                        validators=[DataRequired(), only_numbers,
                                    Length(min=6, max=6)],
                        render_kw={"title": "Ultimos 6 digitos"})

    monto = FloatField('Monto del pago:',
                        validators=[DataRequired(), monto_pm],
                        render_kw={'disabled': False})

    submit_tc = SubmitField('Validar pago')
