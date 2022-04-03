# DevOps AD 4 - Capacidades de Despliegue
Repositorio para la actividad 4 de DevOps sobre Capacidades de Despliegue

## Enunciado
El siguiente paso sería añadir capacidades de despliegue a nuestro servicio, idealmente lanzado automáticamente desde su pipeline de CICD:

* Desplegar los contenedores en algún servicio que lo provea, como AWS Fargate, un Hashicorp Nomad en self-hosting, o máquinas propias con Docker o Docker Swarm instalado.
* Aplicar un Deployment en Kubernetes, ya sea propio o la versión de los Cloud providers.
* Enviar los ejecutables a una o más instancias que los pueden servir, usando servidores web como Tomcat/Catalina (Java) o Unicorn/WSGI (Python).

Pero incluso antes de pensar en desplegar, tenemos que pensar en cómo garantizar que nuestro servicio esté funcionando perfectamente una vez eso ocurra: para eso existen los endpoints de disponibilidad (readiness) y estado (liveness).

Además, es vital poder emitir métricas desde nuestra aplicación, métricas que podrían ser enviadas por un agente a un servicio como Elasticsearch, o recolectadas en modo pull por un servidor de Prometheus.

Por último, se necesita empezar a centralizar el sistema de logs para su futuro envío a un almacén distribuido de trazas. Para esto, es requisito que las trazas (logs) de la aplicación acaben en la carpeta logs , con el siguiente formato de nombre:

- Trazas de aplicación: server-YYYYMMDD.log
- Errores: error-YYYYMMDD.log

## Objetivo

Se pide al alumno la codificación de tres nuevos endpoints, no protegidos por autenticación:

- /ready
  - HTTP 200 - Si el servicio está preparado para funcionar (base de datos accesible, servicios de terceros conectados, logging y métricas configuradas…)
  - HTTP 503 - Si existe alguna condición que evite dar servicio.
  - **NOTA:** En caso de no existir ningún recurso que comprobar (ej. no se ha implementado ningún backend de almacenamiento, ni siquiera un fichero) deberá implementarse alguno para la práctica. Sino, no será correcta.

- /health
  - HTTP 200 - Si el servicio está funcionando OK.
  - HTTP 503- Si el servicio no puede funcionar.

- /metrics
  - Un diccionario JSON con los valores de las siguientes métricas:
    - número de peticiones a cada endpoint.
    - tiempo medio en dar una respuesta (milisegundos) por endpoint.
    - Número de entradas en base de datos de palabras.

    **Estos valores empiezan a contar desde que arranca el servicio.**

  Ejemplo (el formato es libre mientras se respete el contenido):
  
    ```yalm
    {
        "metrics": [
            {
                "name": "consulta_avg_response_time",
                "value" "15.05"
            },
            {
                "name": "consulta_hits",
                "value": "120"
            },
            {
                "name": "db_entries",
                "value": "140000"
            }
        ]
    }
    ```

  **Adicionalmente**, se puede añadir también los datos históricos (incluyendo de todas las ejecuciones pasadas), lo que subirá la nota final.


## Implementación
Se ha optado por realizar una implementación del servicio usando Python y Flask mediante peticiones POST y GET al servidor.\
Se ha considerado que cuando se usa el endpoint "almacena" se está modificando el estado del servidor y por tanto el verbo HTTP correcto es POST.\
Sin embargo, cuando se hace uso del endpoint "consulta", se envían datos al servidor pero no se modifica su estado, así que se ha optado por emplear GET.\
Del mismo modo cuando se da de alta un Usuario se ha de emplear el método POST. Para hacer login o logout se empleará GET.\
Para probar el funcionamiento se recomienda emplear un programa como Curl o Postman.
Se ha eliminado el fichero de almacenamiento de cadenas de las versiones anteriores y se ha sustituido por una tabla dentro de la base de datos del programa.\
Se pretendía implementar el frontend de la aplicación mediante plantillas html, para facilitar el testing y la presentación, pero ha sido posible. 


### Dependencias
Las dependencias están declaradas en el fichero _requeriments.txt_


### Ejecución
Para iniciar la aplicación ejecute el comando:

_python server.py [-h] [-p \<puerto\>]_

Si no se indica ningún parámetro se levantará el servicio con las opciones por defecto que es empleando el puerto 12345.\
Para terminar la aplicación pulsar Ctrl+C

Para Windows, se ha creado el fichero _start.bat_ que inicia el servicio con sus valores por defecto si no se incluyen parámetros y además permite elegir un puerto mediante la sintaxis:
_start.bat -p puerto_

## Funcionamiento
Los endpoints son:
* /
* /signup
* /login
* /logout
* /users
* /almacena
* /consulta
* /ready
* /health
* /metrics

Hay que destacar que se usa SSL, por los que los endpoints ahora emplean el protocolo HTTPS (si se intenta acceder a ellos mediante HTTP dará un error).

### Home
Si se accede al endpoint / se muestra el mensaje HTML "Servicio Web para Cadenas"

### Signup
Permite el registro de un nuevo usuario en la base de datos.\
Se debe indicar en el cuerpo del mensaje un JSON con un nombre (name) y una contraseña (password):
```yalm
{ 
    "name":"Fulanito",
    "password":"contraseña" 
}
```
El servidor devuelve un mensaje JSON en la respuesta indicando el resultado de la operación.\
El nuevo usuario y la contraseña se almacenan en la base de datos (no se almacena la contraseña en claro, si no un hash)

### Login
Permite al usuario autenticarse  indicando su nombre y su contraseña mediante la cabecera de Autorización de HTML.

Si el usuario existe y la contraseña es correcta (se hace el hash y se comprueba con la que se tiene guardada en la base de datos) el servidor devuelve un token que será válido durante 60 minutos.
Este token deberá ser incluido en la cabecera de las peticiones a los endpoints protegidos en un campo llamado _x-access-tokens_ para que nos permita usarlos.

### Logout
Si se accede al endpoint con un token válido, se incluye dicho token en una tabla de tokens expirados. A partir de ese momento no podrá acceder a ningún endpoint protegido hasta que consiga un nuevo token válido mediante el endpoint /login 

### Almacena
Se necesita un token válido para poder llevar a cabo el almacenamiento.\
Para llevar a cabo el almacenamiento de una cadena en el fichero se debe realizar un POST e incluir el parámetro string con la cadena que queremos almacenar en el fichero:
* ej: _POST 127.0.0.1/almacena?string=Cadena+a+almacenar_

Si se emplea un verbo distinto de POST devolverá un error 405 Method Not Allowed.\
Si no se incluye el parámetro "string" devolverá una respuesta 400 BAD REQUEST con un json en el cuerpo con información sobre el error (debe incluir el parámetro string).

### Consulta
Se necesita un token válido para llevar a cabo la consulta.\
Para llevar a cabo la consulta de una palabra en el fichero se debe realizar un GET e incluir el parámetro string con la palabra que queremos almacenar en el fichero:
* ej: _POST 127.0.0.1/consulta?string=Cadena_

Si se emplea un verbo distinto de GET devolverá un error 405 Method Not Allowed.\
Si no se incluye el parámetro "string" devolverá una respuesta 400 BAD REQUEST con un json en el cuerpo con información sobre el error (debe incluir el parámetro string).\
Si se envía más de una palabra devolvera una respuesta 400 BAD REQUEST con un json en el cuerpo con información sobre el error (debe enviar una única palabra).
### Ready
Endpoint que comprueba la conexión con la base de datos y el correcto funcionamiento de los logs
Si todo funciona correctamente devuelve un 200 OK. Si alguno de los dos falla devuelve un 503 NO DISPONIBLE.

### Health
Endpoint que devuelve 200 OK si el funciona correctamente, 503 si no está disponible.

### Metrics
Este endpoint devuelve un JSON con las métricas de los endpoints CONSULTA y ALMACENA y del numero de cadenas almacenadas actualmente en la base de datos.\
En concreto devuelve el número de peticiones en cada endpoint y el tiempo medio de respuesta de cada endpoint.\
El formato de salida es el siguiente:

```yalm
{
  "metrics": [
    {
      "Endpoint_CONSULTA": [
        {
          "name": "consulta_avg_response_time",
          "value": averageConsulta
        },
        {
          "name": "consulta_hits",
          "value": consultaHits
        }
      ]
    },
    {
      "Endpoint_ALMACENA": [
        {
          "name": "almacena_avg_response_time",
          "value": averageAlmacena
        },
        {
          "name": "almacena_hits",
          "value": almacenaHits
        }
      ]
    },
    {
      "Resource_DB": [
        {
          "name": "db_entries",
          "value": resultsEntries
        }
      ]
    }
  ]
}
```
Si no estuviera disponible enviará un mensaje 503.

## Tests
NOTA: No se han implementado los test para verificar el funcionamiento correcto de los tokens.\
En la carpeta tests se han incluído los test unitarios para probar el funcionamiento del servicio. Se han tenido que rebajar las expectativas de cobertura para poder llegar a implementar todos los endpoints requeridos.
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
