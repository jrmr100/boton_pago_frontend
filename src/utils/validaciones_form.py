from wtforms import ValidationError
from flask import session



# VALIDACIONES PERSONALIZADAS
def only_numbers(form, field):
    if not field.data.isnumeric():
        raise ValidationError('El campo solo puede contener números')

def banco_emisor(form, field):
    if "Seleccione un banco" in field.data:
        raise ValidationError('Debe seleccionar un banco emisor')

def passport(form, field):
    if form["tipo_id"].data != "P":
        only_numbers(form, field)

def monto_pm(form, field):
    if field.data < session["monto_bs"]:
        raise ValidationError(f'El monto debe ser igual o mayor a la deuda: Bs.{session["monto_bs"]}')
