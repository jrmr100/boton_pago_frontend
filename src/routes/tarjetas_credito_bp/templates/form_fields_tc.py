from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, FloatField
from wtforms.validators import InputRequired, Length, DataRequired
from src.utils.validaciones_form import only_numbers, banco_emisor, passport, monto_deuda
from datetime import datetime


class FormFieldsTc(FlaskForm):
    monto = FloatField('Monto del pago:',
                       validators=[DataRequired(), monto_deuda],
                       render_kw={'disabled': False, "title": "Use punto(.) para decimales."})
    descripcion = StringField("Descripción", validators=[DataRequired(),
                                          Length(min=3, max=20), passport],
                          render_kw={"title": "Descripción de la operación"})
    nombre = StringField("Nombre del tarjeta habiente", validators=[DataRequired(),
                                                         Length(min=3, max=25), passport],
                              render_kw={"title": "Nombre como aparece en la tarjeta"})

    tipo_id = SelectField('CI/RIF del tarjeta habiente: ',
                          choices=[],
                          validators=[InputRequired()],
                          render_kw={'style': 'width: 80px; margin-right: 10px;'})

    ci = StringField("", validators=[DataRequired(),
                                          Length(min=2, max=20), passport],
                     render_kw={"title": "Ingrese la información del ID"})

    numero_tc = StringField('Número de tarjeta:',
                            validators=[DataRequired(), only_numbers,
                                        Length(min=16, max=16)],
                            render_kw={"title": "No use espacios, ni separadores"})
    codigo_seguridad = StringField("Codigo de seguridad", validators=[DataRequired(),
                                                                    Length(min=3, max=25), passport],
                         render_kw={"title": "Código secreto de la tarjeta de crédito"})

    fecha_vencimiento = DateField('Fecha de vencimiento:',
                           default=datetime.now(),
                           validators=[DataRequired()])

    submit_tc = SubmitField('Validar pago')
