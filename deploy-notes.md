# Despliegue simulado de la aplicación Django

## Objetivo

Este documento describe cómo reproducir el despliegue continuo simulado de la
aplicación. El workflow ejecuta las pruebas, construye una imagen Docker, prepara
una etiqueta para DockerHub, publica evidencia del build, levanta Django y
PostgreSQL con Docker Compose y valida automáticamente la URL del administrador.

## Requisitos

- Git.
- Docker Desktop iniciado y con Docker Compose disponible.
- Puertos locales `8000` y `5433` libres.

## Automatización en GitHub Actions

El archivo `.github/workflows/ci.yml` contiene dos trabajos:

1. `test`: instala las dependencias, ejecuta las migraciones y las pruebas.
2. `docker-build-deploy`: construye y etiqueta la imagen, crea el artefacto de
   evidencia, inicia los servicios y comprueba la respuesta HTTP de Django.

El artefacto `evidencia-build-<SHA>` contiene:

- `image-id.txt`: identificador de la imagen construida.
- `dockerhub-image.txt`: etiqueta preparada para DockerHub.
- `Dockerfile` y `docker-compose.yml`: archivos utilizados en el build.
- `deploy-notes.md`: estas instrucciones.

El artefacto `evidencia-despliegue-<SHA>` contiene el estado de Docker Compose,
los registros de los contenedores y el código HTTP obtenido durante la
validación. La simulación no utiliza credenciales ni publica la imagen en un
registro real.

## Despliegue desde una copia externa del proyecto

Abrir PowerShell y crear una carpeta fuera del repositorio de trabajo:

```powershell
New-Item -ItemType Directory -Path C:\despliegue-practica3
Set-Location C:\despliegue-practica3
git clone --branch cd-setup https://github.com/ricardolandivar69/-S9-TRABAJO-PR-CTICO-EXPERIMENTAL_3.git .
```

Construir e iniciar los contenedores:

```powershell
docker compose up --build --detach
docker compose ps
```

La salida de `docker compose ps` debe mostrar los contenedores
`practica3_django` y `practica3_postgres` en ejecución. PostgreSQL debe aparecer
como `healthy`.

Abrir la siguiente dirección en el navegador:

```text
http://localhost:8000/admin/
```

La página de inicio de sesión del administrador confirma que Django responde
desde el contenedor.

## Detener el despliegue

```powershell
docker compose down
```

Para eliminar también el volumen de datos creado durante esta simulación:

```powershell
docker compose down --volumes
```

## Guía para obtener las Figuras 15 a 21

### Figura 15. Workflow ampliado para la construcción de la imagen Docker

Abrir `.github/workflows/ci.yml` en Visual Studio Code o en GitHub y capturar el
trabajo `docker-build-deploy`. Deben verse los pasos `Construir imagen Docker`,
`Publicar artefacto del build` e `Iniciar despliegue simulado con Docker
Compose`.

**Descripción sugerida:** Se amplió el flujo de integración continua mediante el
trabajo `docker-build-deploy`, encargado de construir la imagen Docker, preparar
la evidencia del build y ejecutar una simulación automatizada del despliegue.

### Figura 16. Build de la imagen Docker en GitHub Actions

En GitHub, abrir `Actions > Django CI > ejecución más reciente > Construir
imagen y simular despliegue`. Expandir el paso `Construir imagen Docker` y
capturar el registro donde termina correctamente la construcción de la imagen.

**Descripción sugerida:** La ejecución de GitHub Actions construyó correctamente
la imagen `practica3-django` a partir del Dockerfile del proyecto, confirmando
que las dependencias y el código fueron incorporados sin errores.

### Figura 17. Artefacto generado o preparado por el workflow

En la parte inferior del resumen de la misma ejecución de GitHub Actions,
capturar la sección `Artifacts`. Deben aparecer `evidencia-build-<SHA>` y
`evidencia-despliegue-<SHA>`.

**Descripción sugerida:** El workflow publicó los artefactos de evidencia del
build y del despliegue. Estos conservan el identificador de la imagen, la
etiqueta simulada para DockerHub, el estado de los servicios, los registros y el
resultado de la validación HTTP.

### Figura 18. Proyecto descargado en la carpeta externa de despliegue

Abrir el Explorador de archivos en `C:\despliegue-practica3` y capturar la
carpeta mostrando `manage.py`, `Dockerfile`, `docker-compose.yml`,
`deploy-notes.md`, `project` y `app`. Puede acompañarse con la terminal mostrando
el `git clone` finalizado.

**Descripción sugerida:** El repositorio fue descargado en una carpeta externa al
entorno de desarrollo original, simulando la obtención del paquete en un equipo
o directorio destinado al despliegue.

### Figura 19. Ejecución del despliegue simulado con Docker Compose

En PowerShell, dentro de `C:\despliegue-practica3`, ejecutar `docker compose up
--build --detach` y luego `docker compose ps`. Capturar la salida donde ambos
contenedores aparezcan en ejecución y PostgreSQL figure como saludable.

**Descripción sugerida:** Docker Compose construyó e inició los servicios de
Django y PostgreSQL. La salida confirma que ambos contenedores se encuentran en
ejecución y que la base de datos superó su comprobación de salud.

### Figura 20. Validación del sistema desde el navegador

Abrir `http://localhost:8000/admin/` y capturar la página de inicio de sesión
de Django. La barra de direcciones debe estar visible para demostrar el acceso al
contenedor local.

**Descripción sugerida:** La pantalla de administración de Django respondió
correctamente desde `localhost:8000`, validando que la aplicación desplegada en
el contenedor puede ser accedida desde el navegador.

### Figura 21. Documento deploy-notes.md

Abrir `deploy-notes.md` en GitHub o Visual Studio Code y capturar el encabezado,
el objetivo y la sección de despliegue desde una copia externa.

**Descripción sugerida:** El archivo `deploy-notes.md` documenta los requisitos,
los comandos de despliegue simulado, la validación del sistema y el procedimiento
para detener y limpiar los contenedores utilizados.
