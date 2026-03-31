# Informe breve — Actividad práctica Docker

## 1. Construcción y ejecución de la imagen

Primero se creó la carpeta `hello-docker` con los archivos `app.py`, `requirements.txt`, `Dockerfile` y `.dockerignore`. Después se construyó la imagen con el comando:

```bash
docker build -t hello-docker:1.0 .
```

Luego se ejecutó el contenedor con:

```bash
docker run -d -p 8000:8000 --name hello hello-docker:1.0
```

Después se verificó que el contenedor estuviera funcionando con `docker ps` y se probó la aplicación con `curl http://localhost:8000`, obteniendo la respuesta esperada: `Hello from Docker! PORT=8000`.

## 2. Qué aprendí sobre variables de entorno y volúmenes

Aprendí que las variables de entorno permiten configurar la aplicación sin cambiar el código fuente. En este caso, la aplicación toma el puerto desde la variable `PORT`, usando `os.getenv`.

También entendí que los volúmenes sirven para conectar carpetas del computador con el contenedor. En la actividad se creó una carpeta `data` en el host y se usó un bind mount para enlazarla con `/data` dentro del contenedor. Esto ayuda a manejar persistencia y compartir archivos entre el host y el contenedor.

## 3. Dificultades y cómo las resolví

Una de las primeras dificultades fue que Docker no estaba iniciado, por lo que el comando `docker build` falló. Esto se resolvió abriendo Docker Desktop y esperando a que el motor quedara activo.

Otra dificultad fue que al principio Docker indicó que el `Dockerfile` estaba vacío. Esto se solucionó guardando correctamente el archivo en VS Code y volviendo a ejecutar el build.

También apareció una advertencia al usar `curl` en PowerShell, ya que se interpreta como `Invoke-WebRequest`. Aun así, la aplicación respondió correctamente y se pudo comprobar que el contenedor estaba funcionando.

## 4. Conclusión

Esta práctica permitió entender el flujo básico de Docker: crear archivos, construir una imagen, ejecutar un contenedor, mapear puertos, usar variables de entorno, trabajar con volúmenes y revisar información del contenedor con comandos como `docker ps`, `docker exec` y `docker inspect`. Fue una buena introducción a la contenerización de aplicaciones.