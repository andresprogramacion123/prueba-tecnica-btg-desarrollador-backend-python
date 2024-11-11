# Prueba técnica desarrollador backend python BTG

**Julian Andres Montoya Carvajal C.C 1214727927**

## Parte 1: Necesidad del negocio

### 1. Tecnologías utilizadas para garantizar la solución

Para garantizar el funcionamiento del sistema que permite a los clientes de BTG realizar acciones como suscribirse a un fondo, retirarse de un fondo, ver el historial de transacciones recientes y recibir notificaciones por email o SMS, propongo las siguientes tecnologías:

* Backend: Utilizaría el lenguaje de programación Python, conocido por su simplicidad y su capacidad para soportar operaciones asincrónicas. Esto facilita la escritura de código eficiente y adaptable. En particular, escogería el framework FastAPI por mi experiencia previa y rapidez de desarrollo con él.

* FastAPI es un framework ideal para construir APIs RESTful con soporte nativo para operaciones asincrónicas, lo que significa que no bloquea la entrada y salida (I/O) en procesos prolongados. Además, se integra fácilmente con bibliotecas de bases de datos tanto ORM como ODM, y utiliza Pydantic para la validación y serialización de datos, lo que es muy útil para manejar datos de manera eficiente.
Dado que el sistema debe enviar notificaciones por email o SMS, FastAPI es una excelente opción. Su capacidad para manejar operaciones asincrónicas permite gestionar estas tareas sin afectar el rendimiento general. Además, su flexibilidad facilita la integración de diversos componentes y el diseño de arquitecturas escalables y adaptables.

* Base de Datos: Utilizaría MongoDB como base de datos NoSQL debido a la necesidad de un esquema de datos flexible y la capacidad de escalabilidad de la API. MongoDB es adecuado para manejar datos no estructurados y permite realizar cambios rápidos en el diseño del esquema. Si más adelante la lógica del negocio requiere un modelo de datos con relaciones complejas, consideraríamos migrar a una base de datos relacional como PostgreSQL. Sin embargo, para este caso, MongoDB es la opción más apropiada por su simplicidad y flexibilidad.

* Servicios de Notificaciones:

**Amazon SNS**: Utilizaría Amazon SNS para enviar mensajes de texto en masa, ya que es una solución confiable para manejar la mensajería a gran escala.

**Amazon SES:** Para el envío de emails, usaría Amazon SES, que es ideal para envíos críticos y de gran volumen. Ofrece alta confiabilidad y garantiza la entrega eficiente de notificaciones importantes, como las relacionadas con la suscripción a un fondo. Si bien podría considerar un servidor SMTP como el de Gmail para pruebas o proyectos pequeños, sus limitaciones en el volumen de envío lo hacen inadecuado para este proyecto.

* Contenedores y replicabilidad: Implementaría Docker y Docker Compose para asegurar que la aplicación se pueda replicar y ejecutar de manera consistente en diferentes entornos de desarrollo y producción. Esto facilita la gestión y despliegue de la solución.

* Despliegue: Utilizaría Amazon EC2 para desplegar la API REST. Amazon EC2 proporciona un entorno controlado y escalable para gestionar servidores según las necesidades específicas de la aplicación. Permite el escalado vertical aumentando recursos como almacenamiento, memoria RAM y núcleos de procesamiento cuando sea necesario

### 2. Diseñar un modelo de datos NOSQL que permita la solucion del problema:

Se plantea para la solucion dos colecciones.

La primera coleccion es la de fondos que permite registrar los 5 fondos definidos por el negocio. Su esquema es el siguiente:

```bash
fondo: {
  "_id": int,
  "nombre": str,
  "monto_minimo": float,
  "categoria": str (categorico puede ser "FPV" o "FIC")
}
```

Un ejemplo de un fondo en base de datos:

```bash
{
  "_id": "1",
  "nombre": "FPV_BTG_PACTUAL_RECAUDADORA",
  "monto_minimo": 75000,
  "categoria": "FPV"
}
```

La segunda coleccion es la coleccion de usuarios que permite registrar el usario con sus datos basicos pero ademas esta coleccion permite almacenar las transacciones realizados por cada usuario. Su esquema es el siguiente:

```bash
usuario: {
  "_id": int,
  "nombre": str,
  "correo": str,
  "telefono": int,
  "saldo_disponible": float,
  "saldo_fondos": [
    float (Saldo en fondo 1),
    float (Saldo en fondo 2),
    float (Saldo en fondo 3),
    float (Saldo en fondo 4),
    float (Saldo en fondo 5)
  ],
  "transacciones": [Transaccion]
}
```

donde el objeto Transaccion es:

```bash
transaccion: {
  "id": uuid,
  "id_fondo": int,
  "nombre_fondo": str,
  "valor": float,
  "tipo_transaccion": str (categorico puede ser "Apertura" o "Cancelacion"),
  "fecha": datetime
}
```

Un ejemplo de un usuario en base de datos recien inscrito

```bash
{
  "_id": "2",
  "nombre": "pepito",
  "correo": "pepito@gmail.com",
  "telefono": 12345,
  "saldo_disponible": 500000,
  "saldo_fondos": [
    0,
    0,
    0,
    0,
    0
  ],
  "transacciones": []
}
```

Un ejemplo de un usuario en base de datos despues de realizar suscripciones y cancelaciones (transacciones)

```bash
{
  "_id": "1",
  "nombre": "julian",
  "correo": "julian@gmail.com",
  "telefono": 3005444343,
  "saldo_disponible": 300000,
  "saldo_fondos": [
    0,
    200000,
    0,
    0,
    0
  ],
  "transacciones": [
    {
      "id": "75712a57-bba1-45e1-9d22-7908df0b5e7e",
      "id_fondo": "1",
      "nombre_fondo": "FPV_BTG_PACTUAL_RECAUDADORA",
      "valor": 200000,
      "tipo_transaccion": "apertura",
      "fecha": "2024-11-11T03:12:34.164180"
    },
    {
      "id": "74e2d003-4fd1-4789-b660-ad8157acbcd0",
      "id_fondo": "2",
      "nombre_fondo": "FPV_BTG_PACTUAL_ECOPETROL",
      "valor": 200000,
      "tipo_transaccion": "apertura",
      "fecha": "2024-11-11T03:18:25.254006"
    },
    {
      "id": "56cd9ab4-4fb1-4630-8a19-d715e57f29ea",
      "id_fondo": "1",
      "nombre_fondo": "FPV_BTG_PACTUAL_RECAUDADORA",
      "valor": 200000,
      "tipo_transaccion": "cancelacion",
      "fecha": "2024-11-11T03:18:36.453024"
    }
  ]
}
```

Con este enfoque se tiene la posibilidad de que un usuario se puede suscribir a varios fondos en la medida que cumpla las respectivas condiciones, ademas puede invertir dinero en un mismo fondo varias veces y en caso de retirarse se le devuelve todo el dinero correspondiente a las diferentes suscripciones al mismo fondo. Ademas el usuario puede invertir en un fondo con un valor mayor al monto minimo del fondo siempre y cuando posee saldo disponible.

Este diseño de modelo de datos permite mantener la escalabilidad parcial pues no se esta considerando el caso de que hayan mas de 5 fondos. Ademas el modelo permite mantener la seguridad pues permite evaluar la logica del negocio y observar que un usuario no reciba ni mas ni menos dinero de lo que corresponde.

### 3.Construccion de la API REST con FastAPI y MongoDB y como ejecutar el proyecto a nivel local

[Descargar video de ejecucion de proyecto](VideoEjecucion2min.mp4)

La API Rest diseñada se puede ejecutar de dos maneras a nivel local:

1. Ejecucion por medio docker y docker compose

Veamos la ejecucion por medio de docker y docker compose:

* Preferiblemente tener instalado Ubuntu 22.04.3 LTS (Jammy) (Windows tambien se puede pero debe poder instalar docker y docker compose).

* Asegurate de instalar Docker version 24.0.7 y ademas Docker Compose version 2.21.0. El siguiente link te puede ayudar a obtener los dos https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04

* Clone el repositorio con los siguientes comandos (debe tener instalado git)

```bash
git clone https://github.com/andresprogramacion123/prueba-tecnica-btg-desarrollador-backend-python.git
```

* Ingresa a la carpeta donde esta el proyecto

```bash
cd prueba-tecnica-btg-desarrollador-backend-python
```

* Posteriomente ejecute el archivo docker compose para ejecutar el proyecto

```bash
sudo docker compose up --build
```

* Visita http://localhost:5000/ en tu navegador para acceder a la aplicacion

* Visita http://localhost:5000/docs en tu navegador para acceder a la documentación interactiva de la API generada automáticamente por FastAPI.

**Nota:** En caso de tener problemas con puertos ya utilizados, ejecutar comando siguiente para conocer el ID del contenedor

```bash
sudo docker ps
```

Luego detener el contenedor con el siguiente comando

```bash
sudo docker stop ID_CONTENEDOR
```

2. Ejecucion sin utilizar docker y docker compose pero cumpliendo con los requistos de desarrollo.

**Requisitos de desarrollo:**

A continuacion se van a describir los requisitos de desarrollo

* Preferiblemente ejecutar y/o desarollar en sistema operativo Ubuntu 22.04 LTS (Jammy) https://releases.ubuntu.com/jammy/
* Tener instalado Python 3.10.12 o superior
* Tener instalado virtualenv para gestionar ambientes virtuales con python y no tener problemas con las dependencias (Aislar entornos de desarrollo)
* Instalar MongoDB 8.0.3 https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/#std-label-install-mdb-community-ubuntu

Despues de tener los anteriores requisitos es posible comenzar a clonar el repositorio

* Clone el repositorio con los siguientes comandos (debe tener instalado git)

```bash
git clone https://github.com/andresprogramacion123/prueba-tecnica-btg-desarrollador-backend-python.git
```

* Ingresa a la carpeta donde esta el proyecto

```bash
cd prueba-tecnica-btg-desarrollador-backend-python
```

* Establece el entorno virtual

```bash
virtualenv env --python=python3
```

* Activa el entorno virtual en linux

```bash
source env/bin/activate
```

* Instala las dependencias

```bash
pip install -r requirements.txt
```

* Ejecutar el proyecto

```bash
export PYTHONDONTWRITEBYTECODE=1 && ./app/prestart.sh && fastapi dev app/main.py
```

* En caso de tener que dar permisos al archivo prestart.sh ejecutar el siguiente comando y volver a ejecutar el comando anterior de ejecucion de proyecto.

```bash
chmod +x app/prestart.sh
```

* Visita `http://localhost:8000/` en tu navegador para acceder a la aplicacion

* Visita `http://localhost:8000/docs` en tu navegador para acceder a la documentación interactiva de la API generada automáticamente por FastAPI

* Para ejecutar pruebas unitarias

```bash
pytest
```

**Despliegue con CloudFormation**

* Subimos la llave SSH a AWS:

* Subimos el archivo YAML a CloudFormation:

* Iniciamos el stack

* Verificamos en la consola de EC2 que la instancia esta en ejecucion.

* Podemos conectarnos a la instancia usando SSH para verificar que Docker y la aplicación estén ejecutándose correctamente.

* Visitamos la IP publica de la instancia para asegurarnos de que la API esta disponible.

## Parte 2: Consultas SQL

```bash
SELECT Cliente.nombre
FROM Cliente 
JOIN Inscripcion ON Cliente.id = Inscripcion.idCliente
JOIN Disponibilidad ON Inscripcion.idProducto = Disponibilidad.idProducto
JOIN Visitan ON Cliente.id = Visitan.idCliente AND Disponibilidad.idSucursal = Visitan.idSucursal;
```