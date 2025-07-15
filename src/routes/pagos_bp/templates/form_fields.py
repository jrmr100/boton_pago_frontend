from flask_wtf import FlaskForm
from wtforms import SubmitField
from src.config import metodos_pago_disabled



class FormFields(FlaskForm):
    submit_pagomovil = SubmitField('PAGO MOVIL', render_kw={'disabled': metodos_pago_disabled["pagomovil"]})
    submit_tarjetas_credito = SubmitField('TARJETAS DE CRÉDITO', render_kw={'disabled': metodos_pago_disabled["tarjetas_credito"]})
    submit_transferencias = SubmitField('TRANSFERENCIAS', render_kw={'disabled': metodos_pago_disabled["transferencias"]})