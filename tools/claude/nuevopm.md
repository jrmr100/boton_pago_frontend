# nuevopm.md
Este archivo provee todos los parametros base para agregar un nuevo banco a la seccion de pagomovil, actualmente esta banesco y banco plaza y el objetivo es agregar banco mercantil

## Resumen del archivo
Agregar banco mercantil como una nueva opcion de pagomovil

## Variables a considerar


## Acciones a realizar:
- Manten el diseño original del proyecto
- usa el logo /home/jmonroy/Python/IFX/boton_pago_frontend/src/routes/pagomovil_bp/static/img/logo_mercantil.png para identificar al banco mercantil en la ruta /pagomovil_bancos y en la nueva ruta de reporte de pago a crear /pagomovil_mercantil
- el codigo del banco para mercantil es 0105 agregalo al .env en la seccion INSTAPAGO con la variable RECEIPTBANK_MERCANTIL_IP="0105" y en donde sea necesario
- en la ruta /pagomovil_bancos agrega los 3 bancos en la misma fila de la tarjeta bootstrap, valida q se cumpla la visualizacion responsiva correctamente y todo se vea simetrico, usa este orden mercantil, banesco y banco plaza
- crea el archivo route_mercantil.py con los mismos datos q los otros formularios de pagomovil
- en la funcion de api_instapago de /utils, modifica la validacion de pago para reciba el receiptbank desde banesco y ahora mercantil, solo estos dos bancos pertenecen a instapago, banco plaza es del proveedor vippo, realiza los ajusten en todo el proyecto donde se use api_instapago
- Modifica la informacion del medio de pago que se reporta al momento de pagar las facturas, ahora existiran dos medio_pago = "pm_instapago_banesco" y medio_pago = "pm_instapago_mercantil"
- valida en todo el proyecto para q se integre correctamente banco mercantil como una opcion mas de pagomovil
- El telefono para banco mercantil sera 04166206963, agregalo como variable editable
- Esta tarjeta no llevara QR
- no realices commit a git, eso se hara manual
  
  