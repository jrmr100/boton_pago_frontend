from flask_wtf import FlaskForm
from wtforms import SubmitField
from src.config import metodos_pago_disabled



class FormFields(FlaskForm):
    submit_pagomovil = SubmitField('PAGO MOVIL', render_kw={'disabled': metodos_pago_disabled["pagomovil_total"]})
    submit_tarjeta_credito = SubmitField('TARJETA DE CRÉDITO', render_kw={'disabled': metodos_pago_disabled["tarjeta_credito_total"]})