from wtforms import ValidationError



# VALIDACIONES PERSONALIZADAS
def only_numbers(form, field):
    if not field.data.isnumeric():
        raise ValidationError('El campo solo puede contener números')