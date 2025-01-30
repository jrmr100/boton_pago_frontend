def resultado_api(resultado_apimw):
    if resultado_apimw[0] == "except":
        return "except"
    elif resultado_apimw[1]["estado"] == "exito":
        return "exito"
    else:
        return "error"

def validar_email(client_email, email_mw):
    if client_email == email_mw:
        return True
