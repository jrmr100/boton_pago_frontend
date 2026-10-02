
def resultado_apimw(resultado_apimw):
    if resultado_apimw[0] == "except":
        return "error_page", resultado_apimw[1]
    elif resultado_apimw[1]["estado"] == "error":
        if "No existe el cliente" in resultado_apimw[1]["mensaje"]:
            return "flash", "No existe cliente con los datos suministrados"
        else:
            return "error_page", resultado_apimw[1]


