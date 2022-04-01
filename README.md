# DevOps AD 3 - Seguridad
Repositorio para la actividad 3 de DevOps sobre Seguridad

## Enunciado
Para proteger el acceso y los datos de nuestro nuevo servicio web, se establecen los siguientes requisitos:
Se limitará el acceso a usuarios registrados y se crearán nuevos endpoints:
* 1. Creación de usuario, donde como mínimo se dará de alta a un usuario identificado por un ID y una contraseña. Por motivos de seguridad, la contraseña nunca se almacena en claro.
Eliminación de usuario, servicio complementario al anterior, elimina un usuario del sistema e invalida todos sus tokens. 
Evidentemente, es un endpoint al que solo puede acceder el propio usuario.
Login, servicio que responderá a un par ID/contraseña válidos con un token de servicio, válido durante una hora como máximo.
Logout, servicio que invalida automáticamente los tokens de un usuario.
* 2. Se protegerá el acceso a los endpoints existentes, empleando un token que se enviará mediante cabeceras HTTP.
Se debe validar el token para ver que no sea demasiado antiguo y que no corresponda a un usuario inválido.
* 3. Para proteger los datos en tránsito, se requiere que el acceso al servicio aproveche las capacidades de cifrado de datos protocolo TLS. 

## Implementación
Se ha optado por realizar una implementación del servicio usando Python y Flask mediante peticiones POST y GET al servidor.\
Se ha considerado que cuando se usa el endpoint "almacena" se está modificando el estado del servidor y por tanto el verbo HTTP correcto es POST.\
Sin embargo, cuando se hace uso del endpoint "consulta", se envían datos al servidor pero no se modifica su estado, así que se ha optado por emplear GET.\
Para probar el funcionamiento se recomienda emplear un programa como Curl.

### Dependencias
* Python 3.7+
* Flask
* Flask-Sqlalchemy
* pyjwt

  
### Ejecución
Para iniciar la palicación ejecutar el comando: _python server.py [-h] [-f \<filename\>] [-p \<puerto\>]_\
Si no se indica ningún parámetro se levantará el servicio con las opciones por defecto que son usando el fichero "cadenas.txt" en el puerto 12345.\
Para terminar la aplicación pulsar Ctrl+C 

Para Windows, se ha creado el fichero _start.bat_ que inicia el servicio con sus valores por defecto si no se incluyen parámetros y además permite elegir un fichero y un puerto mediante la sintaxis:
_start.bat -f fichero -p puerto_

## Funcionamiento
Los dos endpoints son 
* /almacena
* /consulta
* /signup
* /login
* /users
Hay que destacar que se usa SSL, por los que los endpoints ahora emplean el protocolo HTTPS (si se intenta acceder a ellos mediante HTTP dará un error).

### Signup
Permite el registro de un nuevo usuario en la base de datos.
Se debe indicar en el cuerpo del mensaje un JSON con un nombre (name) y una contraseña (password):
{"name":"Fulanito", "password":"contraseña"}
El servidor devuelve un mensaje JSON en la respuesta indicando el resultado de la operación
El nuevo usuario y la contraseña se almacenan en la base de datos (no se almacena la contraseña en claro, si no un hash)

### Login
Permite autenticarse al usuario indicando su nombre y su contraseña en el cuerpo del mensaje en forma de JSON (análogo al endpoint signup)
Si el usuario existe y la contraseña es correcta (se hace el hash y se comprueba con la que se tiene guardada en la base de datos) el servidor devuelve un token que será válido durante 60 minutos.
Este token habrá que incluirlo en la cabecera de las peticiones a los endpoints /almacena y /consulta en un campo llamado _x-access-tokens_ para que nos permita usarlos.

### Logout
Se pretendía conseguir un endpoint que invalidara el token de forma inmediata, pero no hemos conseguido implementarlo a tiempo.

### Almacena
Se necesita un token válido para poder llevar a cabo el almacenamiento
Para llevar a cabo el almacenamiento de una cadena en el fichero se debe realizar un POST e incluir el parámetro string con la cadena que queremos almacenar en el fichero:
* ej: _POST 127.0.0.1/almacena?string=Cadena+a+almacenar_

Si se emplea un verbo distinto de POST devolverá un error 405 Method Not Allowed.\
Si no se incluye el parámetro "string" devolverá una respuesta 400 BAD REQUEST con un json en el cuerpo con información sobre el error (debe incluir el parámetro string).
### Consulta
Se necesita un token válido para llevar a cabo la consulta
Para llevar a cabo la consulta de una palabra en el fichero se debe realizar un GET e incluir el parámetro string con la palabra que queremos almacenar en el fichero:
* ej: _POST 127.0.0.1/consulta?string=Cadena_

Si se emplea un verbo distinto de GET devolverá un error 405 Method Not Allowed.\
Si no se incluye el parámetro "string" devolverá una respuesta 400 BAD REQUEST con un json en el cuerpo con información sobre el error (debe incluir el parámetro string).\
Si se envía más de una palabra devolvera una respuesta 400 BAD REQUEST con un json en el cuerpo con información sobre el error (debe enviar una única palabra).

## Tests
NOTA: No nos ha dado tiempo a realizar los test para verificar el funcionamiento correcto de los tokens
En la carpeta tests se han incluído los test unitarios para probar el funcionamiento del servicio intentando tener una cobertura del 100%
* _test_almacena.py_ -- prueba el funcionamiento del endpoint "almacena"
* _test_consulta.py_ -- prueba el funcionamiento del endpoint "consulta"
* _test_others.py_   -- prueba el funcionamiento del resto de funciones de server.py 

Para poder ejecutar los test y ver su cobertura es necesario instalar _pytest_ y _coverage_

Para evaluar la covertura:\
_coverage run -m pytest_\
Para visualizar el resultado:\
_coverage report_\
Para generar un reporte detallado en HTML:\
_coverage html_\
El resultado de éste último cuando se ejecutó en nuestra máquina se ha incluido en el repositorio.

## Autores ✒️

Los componentes del grupo:

* **Antonio De Gea Velasco**
* **Adrian Rodriguez Montesinos**
* **Jorge Sánchez-Alor Expósito**
