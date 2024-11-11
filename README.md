# Prueba técnica desarrollador backend python BTG

**Julian Andres Montoya Carvajal C.C 1214727927**

**Parte 1: Necesidad del negocio**

1. Tecnologias utilizadas para garantizar la solucion:

Para garantizar la solucion del sistema que permite a los clientes BTG realizar las acciones de suscribirse a un fondo, Salirse de un fondo, ver el historial de sus ultimas transacciones y envio de notificaciones via email o sms. Utilizaria en el backend el lenguaje de programacion Python debido a su simplicidad a la hora de escribir codigo y ademas a su posibilidad para soportar operaciones asincronas. Ahora para utilizar un framework de python debido a mi experiencia y rapidez a la hora de desarrollar escogeria el framework FastAPI. 

FastAPI es es un framework especializado para escribir API Rest, posee soporte para operaciones asincronas, es decir no bloquear I/O en casos de operaciones muy demoradas. Tambien se puede integrar facilmente con otras librerias de bases de datos como ORM o ODM. FasTAPI utiliza pydantic como libreria para la validacion de datos, de manera que es muy util para validar los datos que entran y serializar a json. Como se desea enviar notificaciones via email o sms. FastAPI es ideal debido a que su soporte asincrono permitiria manejar las operaciones para este caso de envio de notificaciones. Ademas debido a la flexibilidad que posee el framework utilizar diversos componentes, establecer diversas arquitecturas es posible de manera que es un framework que se puede adapatar a muchos casos de uso.

MongoDB como base de datos. Debido a que la solucion de la logica del negocio involucra considerar varios casos y se desea de momento una API escalable y flexible en el esquema de datos. Utilizaria una base de datos no relacional (NoSQL) como MongoDB. En la medida que el esquema de datos este bien definido y que la solucion requiera realizar muchas relaciones se podria considerar una base de datos relacional como Postgresql. Pero de momento la mejor opcion es MongoDB debido a su simplicidad y flexibilidad a la hora de establecer esquemas de datos.

2. Diseñar un modelo de datos NOSQL que permita la solucion del problema:

3.Construccion de la API REST con FastAPI y MongoDB y como ejecutar el proyecto a nivel local

**Requisitos de desarrollo:**

A continuacion se van a describir los requisitos de desarrollo

* Preferiblemente ejecutar y/o desarollar en sistema operativo Ubuntu 22.04 LTS (Jammy) https://releases.ubuntu.com/jammy/
* Tener instalado Python 3.10.12 o superior
* Tener instalado virtualenv para gestionar ambientes virtuales con python y no tener problemas con las dependencias (Aislar entornos de desarrollo)
* Instalar MongoDB 8.0.3 https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/#std-label-install-mdb-community-ubuntu

Nota: Por motivos de tiempo, no se ha utilizado Docker para empaquetar toda la aplicación. Usar Docker permitiría contenerizar tanto el sistema operativo Ubuntu como la versión de Python, eliminando la necesidad de crear ambientes virtuales.

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

* para ejecutar pruebas unitarias

```bash
pytest
```

**Parte 2: Consultas SQL**

```bash
SELECT c.nombre
FROM Cliente c
JOIN Inscripcion i ON c.id = i.idCliente
JOIN Disponibilidad d ON i.idProducto = d.idProducto
JOIN Visitan v ON c.id = v.idCliente AND d.idSucursal = v.idSucursal;
```