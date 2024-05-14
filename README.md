# Integración de plataformas

Segunda evaluación, primera entrega de API web services para modulo de ventas "FERREMAX"

## Instalación

### Requisitos previos

Antes de comenzar, asegúrate de tener instalado Python en tu sistema. Si no lo tienes, puedes descargarlo desde [Python.org](https://www.python.org/).

### Configuración del Ambiente Virtual

1. Clona el repositorio a tu máquina local:

```bash
git clone https://github.com/PattySnow/WebServices_Integracion
```

2. Navega hasta el directorio del proyecto:

```
cd tu_proyecto
```
3. Crea un ambiente virtual:

```bash
python -m venv venv
```
4. Activa el ambiente virtual:
5. 
En Windows:

```bash
venv\Scripts\activate
```

En macOS/Linux:

```bash
source venv/bin/activate
```

## Instalación de Dependencias

Una vez que el ambiente virtual esté activado, instala las dependencias del proyecto ejecutando el siguiente comando:

```bash
pip install -r requirements.txt
```
## Uso

Ejecución de la API

Para iniciar cualquiera de las APIs disponibles en el proyecto, utiliza los siguientes comandos en tu terminal:

```bash
uvicorn auth:app --reload
```
```bash
uvicorn user_jwt:app --reload
```
```bash
uvicorn tools:app --reload
```
```bash
uvicorn shopping_cart:app --reload
```
```bash
uvicorn webpay:app --reload
```

## Documentación de la API

Una vez que la API esté en funcionamiento, puedes acceder a la documentación de la API en tu navegador web ingresando la siguiente URL:

```bash
http://localhost:8000/docs
```
O bien, puedes especificar en que otro puerto ejecutar la app con el flag --port 'número de puerto'  por ejemplo, --port 4000.

Esto te llevará a la interfaz interactiva de Swagger UI donde podrás explorar todos los endpoints disponibles y probarlos directamente desde tu navegador.

## Contribución
Si deseas contribuir a este proyecto, sigue estos pasos:

Haz un fork del repositorio
Crea una nueva rama 

```bash
git checkout -b feature/nueva-funcionalidad
```

Realiza tus cambios y haz commit de ellos
```bash
git commit -am 'Agrega nueva funcionalidad'
```
Haz push a la rama
```bash
git push origin feature/nueva-funcionalidad
```
Crea un nuevo Pull Request

```bash
git pull-request
```

## Herramientas utilizadas:

### FastAPI
Documentación Oficial: [FastAPI Documentation](https://fastapi.tiangolo.com/)
GitHub Repository: [FastAPI GitHub](https://github.com/tiangolo/fastapi)

### Uvicorn

Documentación Oficial: [ Uvicorn Documentation](https://www.uvicorn.org/)
GitHub Repository: [Uvicorn GitHub](https://github.com/encode/uvicorn)

### SQLAlchemy

Documentación Oficial: [SQLAlchemy Documentation ](https://docs.sqlalchemy.org/en/20/)
