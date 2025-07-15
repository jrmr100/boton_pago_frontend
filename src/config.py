# Lista de opciones CI/RIF para el home
lista_id = ("V", "J", "G", "E", "P")

# Lista de operadoras telefonicas
lista_phone = ("0412", "0414", "0424", "0416", "0426")

# Lista de correos para enviar errores de tasa BCV y lista de bancos
correos_tasa_bcv = ["jmonrroy@ifx.com.ve", "gjaramillo@ifx.com.ve", "zarelda.herbert@gmail.com",
                    "mariaespana2netvzla@gmail.com", "reinaldo.b@ifxnw.com.ve", "gerencia@sisca.co"]

# Deshabilitar metodos de pago
metodos_pago_disabled = {
    "pagomovil": False,
    "tarjetas_credito": False,
    "transferencias": False,
    "zelle": False
}

# Config Banco Plaza
pm_bancoplaza = {
    "telefono": "04241686275",
    "nombre_banco": "BANCO PLAZA",
    "rif": "J303390684",
    "logo": "img/logo_bancoplaza.png",
    "disabled": False
}

# Config Banesco
pm_banesco = {
    "telefono": "04143025855",
    "nombre_banco": "BANESCO",
    "rif": "J303390684",
    "logo": "img/logo_banesco.png",
    "qr_disabled": False,
    "disabled": False
}

# Config Banesco
tarjetas_credito = {
    "telefono": "04143025855",
    "nombre_banco": "BANESCO",
    "rif": "J303390684",
    "logo": "img/tarjetas_credito.png",
    "qr_disabled": False,
    "disabled": False
}

transferencias = {
    "telefono": "04143025855",
    "nombre_banco": "BANESCO",
    "rif": "J303390684",
    "logo": "img/transferencias.png",
    "qr_disabled": False,
    "disabled": False
}

contacto_WhatsApp = "04241686275"