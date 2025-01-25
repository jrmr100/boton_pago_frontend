# nombre_proyecto
    Plantilla para proyectos Flask

# Objetivo:
    Tener acceso rapido a los codigos iniciales de proyectos web usando flask

# Premisas
    - Reutilizable en cualquier proyecto
    - Actualizado con las mejores prácticas
    - Funcional

# INSTALACIÓN:
- Sistema base: Debian 12
- Actualizar los repositorios del sistema

      apt install git virtualenv
      apt install nginx (si usa nginx)
      apt install apache2 libapache2-mod-wsgi-py3 apachetop (si usa apache)

- Clonar el repositorio de github
- Crear entorno virtual de python dentro de la carpeta root del proyecto

      sudo virtualenv venv -p /usr/bin/python3
      source venv/bin/activate

- Instala los requerimientos del sistema

      sudo venv/bin/pip3 install -r requirements.txt
      sudo venv/bin/pip3 install gunicorn (si usa nginx)

- Cambiar el propietario de toda la carpeta en caso de producción

      sudo chown -R www-data:www-data nombre_proyecto/

- Configurar .env y mi_config.py con los datos y rutas del sistema


INSTALACIÓN CON APACHE2 CON MOD_WSGI:

- habiltar wsgi

      sudo a2enmod wsgi

- Configurar los puertos que apache usara para escuchar peticiones

      sudo nano /etc/apache2/ports.conf
      Listen 8000

- Crear certificados autofirmados (Solo para ambientes donde no hace falta validar los certificados validos)

      openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 3650

      El nombre del FQDN debe coincidir con SERVERNAME de apache

- Configurar apache2
- Agregar archivo de configuración de apache
 
      sudo nano /etc/apache2/sites-available/nombre_proyecto.conf

      <VirtualHost 181.225.41.12:80>
          ServerName 181.225.41.12
          ServerAdmin jmonrroy@ifx.com.ve
          DocumentRoot /var/www/nombre_proyecto
          # DirectoryIndex home.html

          WSGIDaemonProcess nombre_proyecto user=www-data group=www-data threads=10 python-home=/var/www/nombre_proyecto/venv/ processes=2 graceful-timeout=30 maximum-requests=1000 restart-interval=30
          WSGIProcessGroup nombre_proyecto
          WSGIApplicationGroup %{GLOBAL}
          WSGIScriptAlias / /var/www/nombre_proyecto/nombre_proyecto.wsgi
          Alias /static/ /var/www/nombre_proyecto/static/
          <Directory /var/www/nombre_proyecto/>
              Options Indexes FollowSymLinks
              AllowOverride all
              Require all granted
          </Directory>

          ErrorLog ${APACHE_LOG_DIR}/error.log
          CustomLog ${APACHE_LOG_DIR}/access.log combined
          RewriteEngine on
          RewriteCond %{SERVER_NAME} =181.225.41.12
          RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
      </VirtualHost>


- Agregar archivo de configuración de apache con HTTPS

      sudo nano /etc/apache2/sites-available/nombre_proyecto-ssl.conf

      <VirtualHost 181.225.41.12:443>
              ServerName 181.225.41.12
              ServerAdmin jmonroy@ifx.com.ve
              DocumentRoot /var/www/nombre_proyecto
              # DirectoryIndex index.html
              ErrorLog ${APACHE_LOG_DIR}/error.log
              CustomLog ${APACHE_LOG_DIR}/access.log combined

              SSLEngine on
              SSLCertificateFile /var/www/nombre_proyecto/cert.pem
              SSLCertificateKeyFile /var/www/nombre_proyecto/key.pem

              WSGIDaemonProcess nombre_proyecto-ssl user=www-data group=www-data threads=10 python-home=/var/www/nombre_proyecto/venv/ processes=2 graceful-timeout=30 maximum-requests=1000 restart-interval=30
              WSGIProcessGroup nombre_proyecto
              WSGIApplicationGroup %{GLOBAL}
              WSGIScriptAlias / /var/www/nombre_proyecto/nombre_proyecto.wsgi
              Alias /static/ /var/www/nombre_proyecto/static/
              <Directory /var/www/nombre_proyecto/>
                      Options FollowSymLinks
                      AllowOverride None
                      Require all granted
              </Directory>
      </VirtualHost>

- Activar el virtualhost en apache

      sudo a2ensite nombre_proyecto.conf
      sudo a2ensite nombre_proyecto-ssl.conf
 

- Crear archivo wsgi con las variables adecuadas
      
      sudo nano nombre_proyecto.wsgi

      import sys
      sys.path.insert(0, '/var/www/nombre_proyecto/')
      sys.path.append('/var/www/nombre_proyecto/venv/lib/python3.7/site-packages/')
      from app import app as application

- Restart apache

      sudo service apache2 restart

- Agregar regla al UFW

      sudo ufw allow 8000

# TROUBLESOOTING

- LOG
 
        sudo tail -f /var/log/syslog
        sudo tail -f /var/log/apache2/error.log
        sudo tail -f /var/log/apache2/access.log

- Revisar y matar proceso en ejecucion

      ps -aux |grep python
      sudo kill -9 29918

