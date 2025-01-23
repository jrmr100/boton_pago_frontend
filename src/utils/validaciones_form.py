from wtforms import ValidationError
from datetime import datetime



# VALIDACIONES PERSONALIZADAS
def only_numbers(form, field):
    if not field.data.isnumeric():
        raise ValidationError('El campo solo puede contener números')

def passport(form, field):
    if form["tipo_id"].data != "P":
        only_numbers(form, field)

def banco_emisor(form, field):

    if  "Seleccione un banco" in field.data:
        raise ValidationError('Debe seleccionar un banco emisor')

def fecha_futura(form, field):
    fecha_actual = datetime.now()
    fecha_actual_solo_fecha = fecha_actual.date()
    if  field.data > fecha_actual_solo_fecha:
        raise ValidationError('Fecha incorrecta')

def monto(form, field):
    if  "," in field.data:
        raise ValidationError('Formato incorrecto, use "." como separador decimal')
    try:
        float(field.data)
    except ValueError:
        raise ValidationError('El campo solo puede contener números')


