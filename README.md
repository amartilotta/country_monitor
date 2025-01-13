
El proyecto se encuentra desarrollado con **Django** y **Django REST framework** , utilizado dentro de un ambiente de desarrollo con **Docker**, y utilizando la imagen de **Python 3.11**.



## Index

- [Index](#index)
- [1. Setup - Primer uso](#1-setup---primer-uso)
  - [1.1 Prerrequisitos](#11-prerrequisitos)
  - [1.2 Clona el repositorio](#12-clona-el-repositorio)
  - [1.3 Variables de entorno](#13-variables-de-entorno)
  - [1.4 Instalación de dependencias (Opcional)](#14-instalación-de-dependencias-opcional)
- [2. Levantar contenedor](#2-levantar-contenedor)
  - [2.1 Comandos dentro del contenedor](#21-comandos-dentro-del-contenedor)
- [3. Linter y Extensiones](#3-linter-y-extensiones)
  - [3.1 Recommended IDE Setup](#31-recommended-ide-setup)
  - [3.2 Formateo de código y Linter](#32-formateo-de-código-y-linter)
- [4. Descripción de servicios basicos](#4-descripción-de-servicios-basicos)
- [5. Ejecución de la tarea programada](#5-ejecución-de-la-tarea-programada)

<br />

## 1. Setup - Primer uso

### 1.1 Prerrequisitos

- [Docker](https://docs.docker.com/engine/install/)
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
- [Python 3.11](https://www.python.org/)



### 1.2 Clona el repositorio

Empezar clonando el repo y usando la branch **main**:

```bash
git clone git@github.com:amartilotta/country_monitor.git
```

### 1.3 Variables de entorno

Para este paso es necesario ejecutar los dos siguientes scripts:

```bash
cp .env.example .env

```

Dentro de los mismos se hara lo siguiente:

- Cargar **variables de entorno** para el proyecto.


### 1.4 Instalación de dependencias (Opcional)

Para instalar las dependencias del proyecto es necesario **ejecutar** el siguiente comando en la **raíz** del proyecto:

```bash
poetry env use 3.11
poetry install
```

Ahora para utilizar el entorno de desarrollo es necesario **activar** el **entorno** virtual con el siguiente comando:

```bash
poetry shell
```


Ahora en el **IDE** seleccionar el **entorno** virtual que se encuentra en la **raíz** del proyecto.


- Presionar: `Ctrl + Shift + P`
- Busca: `> Python: Select Interpreter`
- Seleccionar el entorno virtual `defaultInterpreterPath` o en su defecto `./venv`


Esto solo nos beneficiara para el desarrollo del proyecto, ya que nos permitirá utilizar las **dependencias** instaladas dentro de **docker**.



## 2. Levantar contenedor

Para utilizar el contenedor es necesario **ejecutar** el siguiente comando en la **raíz** del proyecto:

```bash
docker compose up
```
o en su defecto para dejarlo corriendo en segundo plano
```bash
docker compose up -d
```

En una terminal, arrojar el siguiente comando
```bash
docker exec -it country-monitor python manage.py migrate
```
Una vez que la aplicación esté en funcionamiento, es posible que aparezca un mensaje en rojo que indique lo siguiente:
"Run 'python manage.py migrate' to apply them."

Para solucionar esto, abre una terminal y ejecuta el siguiente comando para aplicar las migraciones necesarias:
```bash
docker exec -it country-monitor python manage.py migrate
```

En este punto, tienes dos opciones para asegurarte de que las tareas programadas en Celery se ejecuten correctamente:

Esperar una hora a que se vuelva a ejecutar automáticamente la tarea programada, ya que en el primer intento las migraciones aún no estaban aplicadas.

Reiniciar el contenedor de Celery para que las tareas comiencen de inmediato.

Si optas por la segunda opción, puedes hacerlo desde la interfaz gráfica de Docker Desktop o ejecutar este comando en la terminal:
```bash
docker compose restart celery-country-monitor
```
Si se siguieron los pasos hasta este punto, ya puedes entrar al proyecto desde el puerto 4040:

[**http://localhost:4040**](http://localhost:4040)


> 💡 **Tip:** En caso de necesitar una instalación **limpia**. Es posible utilizar make fresh-install antes de ejecutar el contenedor para que se instalen las dependencias desde cero.


### 2.1 Comandos dentro del contenedor

Para utilizar **comandos** específicos en el **contenedor** de docker, se hara de la siguiente forma:

```bash
make shell-docker
```

## 3. Linter y Extensiones

Nuestro proyecto cuenta con un **linter** que nos ayuda a mantener un código **limpio y ordenado**. Para poder utilizarlo es necesario instalar las siguientes **extensiones** en tu IDE:

- [VSCode](https://code.visualstudio.com/).
- [Python IntelliSense](vscode:extension/ms-python.python).
- [Black Formatter](vscode:extension/ms-python.black-formatter).
- [Ruff](vscode:extension/charliermarsh.ruff).
- [Pylance](vscode:extension/ms-python.vscode-pylance).
- [Mypy Checker](vscode:extension/ms-python.mypy-type-checker).


### 3.1 Recommended IDE Setup

Las siguientes extensiones son **recomendadas** para un mejor uso del IDE:

- [Debugpy](vscode:extension/ms-python.debugpy).
- [Docker](vscode:extension/ms-azuretools.vscode-docker).
- [Error Lens](vscode:extension/usernamehw.errorlens).
- [Better Comments](vscode:extension/aaron-bond.better-comments).
- [VsCode Action Buttons](vscode:extension/seunlanlege.action-buttons).

### 3.2 Formateo de código y Linter


Para correr el formateo de código utilizamos:

```sh
make format
```
Junto al check linter:
```sh
make linter
```


## 4. Descripción de servicios basicos

La **visualizacion** de la **API** se encuentra en esta  [**`url`**](http://localhost:4040/api/v1/countries/)

Los servicios más utilizados son:

| Resumen de servicio               | Método |                   URL                    |
| --------------------------------- | ------ | ---------------------------------------- |
| Consulta de paises (paginado)     |   GET  | /api/v1/countries/?offset=int&limit=int  |
| Consulta a pais por ID            |   GET  | /api/v1/countries/{id}                   |

## 5. Ejecución de la tarea programada

Para ejecutar la tarea programada, sigue estos pasos:

**Iniciar el contenedor de Celery en segundo plano**:
```bash
docker compose up -d celery-country-monitor
```

Mostrar los últimos 1000 registros de logs:
```bash
docker logs --tail 1000 celery-country-monitor
```
Adjuntar la terminal al contenedor:
```bash
docker attach --detach-keys='ctrl-c' celery-country-monitor
```
Para visualizar las tareas programadas, se instala la dependencia Flower, una herramienta que permite monitorear gráficamente el estado de las tareas programadas de Celery. Esta herramienta se encuentra expuesta en el [**`puerto 4041`**](http://localhost:4041/).

Su funcionamiento es el siguiente:

En la pestaña principal **Worker**, se muestra la instancia de Celery activa.
- Dentro de esta, en la subpestaña Queues, se pueden visualizar las tareas activas en tiempo real.
- En la subpestaña de Worker llamada Tasks, se encuentra el listado de tareas procesadas.
- En la pestaña principal **Tasks**, se presenta el historial completo de tareas programadas ejecutadas, junto con su estado y la instancia de Celery asociada (Worker).