from wtforms import ValidationError



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
