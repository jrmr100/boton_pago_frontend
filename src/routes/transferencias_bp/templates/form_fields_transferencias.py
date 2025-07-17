from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, FloatField
from wtforms.validators import InputRequired, Length, DataRequired
from src.utils.validaciones_form import only_numbers, banco_emisor, passport, monto_deuda
from datetime import datetime


class FormFieldsTransferencias(FlaskForm):

    tipo_id = SelectField('CI/RIF del pagador: ',
                          choices=[],
                          validators=[InputRequired()],
                          render_kw={'style': 'width: 80px; margin-right: 10px;'})

    ci = StringField("", validators=[DataRequired(),
                                          Length(min=2, max=20), passport],
                          render_kw={'placeholder': '123456789',
                                     "title": "Ingrese la información del ID"})

    fecha_pago = DateField('Fecha de la transferencia:',
                           default=datetime.now(),
                           validators=[DataRequired()])

    banco_emisor = SelectField('Banco Emisor: ',
                         choices=[],
                         validators=[InputRequired(),
                                     banco_emisor])
    referencia = StringField('Número de referencia:',
                        validators=[DataRequired(), only_numbers,
                                    Length(min=4)],
                        render_kw={"title": "Mínimo 4 caracteres"})

    monto = FloatField('Monto de la transferencia:',
                       validators=[DataRequired(), monto_deuda],
                       render_kw={'disabled': False})

    submit_transferencias = SubmitField('Validar pago')
