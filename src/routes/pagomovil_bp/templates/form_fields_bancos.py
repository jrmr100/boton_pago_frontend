from flask_wtf import FlaskForm
from wtforms import SubmitField
from src.config import pm_banesco, pm_bancoplaza


class FormFieldsBancos(FlaskForm):
    submit_bancoplaza = SubmitField('REPORTAR PAGO', render_kw={'disabled': pm_bancoplaza[4]})
    submit_banesco = SubmitField('REPORTAR PAGO', render_kw={'disabled': pm_banesco[4]})

