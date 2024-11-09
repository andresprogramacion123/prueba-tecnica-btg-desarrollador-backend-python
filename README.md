# Prueba tecnica desarrollador backend python BTG

**Julian Andres Montoya Carvajal C.C 1214727927**

1. Tecnologias utilizadas para garantizar la solucion:

Para garantizar la solucion del sistema que permite a los clientes BTG realizar las acciones de suscrbirse a un fondo, Salirse de un fondo, ver el historial de sus ultimas transacciones y envio de notificaciones via email o sms. Utilizaria en el backend el lenguaje de programacion python debido a su simplicidad a la hora de escribir codigo y ademas 


3. Como ejecutar el proyecto a nivel local

* Inicialmente clona el proyecto en tu local

* Requisitos de desarrollo:

A continuacion se van a describir los requisitos de desarrollo

* Preferiblemente ejecutar en sistema operativo Ubuntu 22.04 LTS (Jammy) https://releases.ubuntu.com/jammy/
* Tener instalado Python 3.10.12 
* Tener instalado virtualenv para gestionar ambientes virtuales con python y no tener problemas con las dependencias
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

* En caso de tener que dar permisos

```bash
chmod +x app/prestart.sh
```

* Visita `http://localhost:8000/` en tu navegador para acceder a la aplicacion

* Visita `http://localhost:8000/docs` en tu navegador para acceder a la documentación interactiva de la API generada automáticamente por FastAPI