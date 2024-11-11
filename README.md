# Prueba técnica desarrollador backend python BTG

**Julian Andres Montoya Carvajal C.C 1214727927**

## Parte 1: Necesidad del negocio

### 1. Tecnologias utilizadas para garantizar la solucion:

Para garantizar la solucion del sistema que permite a los clientes BTG realizar las acciones de suscribirse a un fondo, Salirse de un fondo, ver el historial de sus ultimas transacciones y envio de notificaciones via email o sms. Utilizaria en el backend el lenguaje de programacion Python debido a su simplicidad a la hora de escribir codigo y ademas a su posibilidad para soportar operaciones asincronas. Ahora para utilizar un framework de python debido a mi experiencia y rapidez a la hora de desarrollar escogeria el framework FastAPI. 

FastAPI es es un framework especializado para escribir API Rest, posee soporte para operaciones asincronas, es decir no bloquear I/O en casos de operaciones muy demoradas. Tambien se puede integrar facilmente con otras librerias de bases de datos como ORM o ODM. FasTAPI utiliza pydantic como libreria para la validacion de datos, de manera que es muy util para validar los datos que entran y serializar a json. Como se desea enviar notificaciones via email o sms. FastAPI es ideal debido a que su soporte asincrono permitiria manejar las operaciones para este caso de envio de notificaciones. Ademas debido a la flexibilidad que posee el framework utilizar diversos componentes, establecer diversas arquitecturas es posible de manera que es un framework que se puede adapatar a muchos casos de uso.

MongoDB como base de datos. Debido a que la solucion de la logica del negocio involucra considerar varios casos y se desea de momento una API escalable y flexible en el esquema de datos. Utilizaria una base de datos no relacional (NoSQL) como MongoDB. En la medida que el esquema de datos este bien definido y que la solucion requiera realizar muchas relaciones se podria considerar una base de datos relacional como Postgresql. Pero de momento la mejor opcion es MongoDB debido a su simplicidad y flexibilidad a la hora de establecer esquemas de datos.

Amazon SNS y SBS

Docker y Docker compose

Amazon EC2

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

La API Rest diseñada se puede ejecutar de dos maneras a nivel local:

1. Ejecucion por medio docker y docker compose

Veamos la ejecicion por medio de docker y docker compose:

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

## Parte 2: Consultas SQL

```bash
SELECT c.nombre
FROM Cliente c
JOIN Inscripcion i ON c.id = i.idCliente
JOIN Disponibilidad d ON i.idProducto = d.idProducto
JOIN Visitan v ON c.id = v.idCliente AND d.idSucursal = v.idSucursal;
```