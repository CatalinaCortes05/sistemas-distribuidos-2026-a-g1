# 03 Week - session 1: Setup del Repositorio y Ambientes

## Actividad 1: Configurar el Monorepo

Para este proyecto se decidió usar una estrategia **Monorepo**, ya que el equipo es pequeño y esta opción facilita la organización, el trabajo colaborativo y la configuración compartida del proyecto. Esta es la estrategia recomendada para el curso. :contentReference[oaicite:1]{index=1}

### Estructura propuesta del monorepo

```text
gestion-de-citas-inteligente/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── gateway/
│   ├── src/main/java/
│   ├── src/main/resources/
│   │   └── application.yml
│   ├── pom.xml
│   └── Dockerfile
│
├── users-service/
│   ├── src/main/java/
│   ├── src/main/resources/
│   │   └── application.yml
│   ├── src/test/java/
│   ├── pom.xml
│   └── Dockerfile
│
├── turnos-service/
│   ├── src/main/java/
│   ├── src/main/resources/
│   │   └── application.yml
│   ├── src/test/java/
│   ├── pom.xml
│   └── Dockerfile
│
├── notifications-service/
│   ├── src/main/java/
│   ├── src/main/resources/
│   │   └── application.yml
│   ├── src/test/java/
│   ├── pom.xml
│   └── Dockerfile
│
├── docker-compose.yml
├── docker-compose.dev.yml
├── .gitignore
├── .editorconfig
└── README.md
```
---

## Archivo .gitignore

### === Java / Maven ===
target/
*.class
*.jar
*.war
*.log

### === Spring Boot ===
application-local.yml
application-secret.yml

### === IDE ===
.idea/
*.iml
.vscode/
*.swp

### === Docker ===
.env
docker-compose.override.yml

### === OS ===
.DS_Store
Thumbs.db

### === Otros ===
*.bak
*.tmp

---
# Contenido inicial del README.md

## Gestión de Citas Inteligente

## Integrantes
- Catalina Cortes
- Yeison Scarpetta
- Sofía Perafán
- Nicolas Alvarez

## Descripción del proyecto
Gestión de Citas Inteligente es un sistema distribuido orientado a la administración de turnos médicos. Permite registrar usuarios, gestionar turnos y enviar notificaciones automáticas.

## Arquitectura
El proyecto se desarrollará bajo una arquitectura de microservicios dentro de un monorepo. Los componentes principales serán:
- API Gateway
- Users Service
- Turnos Service
- Notifications Service

## Tecnologías principales
- Java
- Spring Boot
- Spring Cloud Gateway
- PostgreSQL
- Docker
- GitHub Actions

**Justificación**

El uso de monorepo permite tener todo el código en un solo lugar, compartir configuración entre servicios, centralizar CI/CD y facilitar el trabajo del equipo. Esto coincide con la recomendación de la sesión para equipos pequeños como el del curso.

---
## Actividad 2: Configurar Ramas y Protecciones

La estrategia de branching del proyecto se basará en tres ramas principales: **develop**, **qa** y **main**, siguiendo un flujo ordenado para separar desarrollo, pruebas y producción.

### Ramas principales del proyecto

- **develop:** rama de integración de nuevas funcionalidades
- **qa:** rama para pruebas y validación
- **main:** rama estable de producción

### Comandos para crear las ramas

```bash
git checkout main
git checkout -b develop
git push -u origin develop

git checkout main
git checkout -b qa
git push -u origin qa
```
### Protección de ramas

Se deben configurar reglas de protección en GitHub para evitar cambios directos en ramas importantes y asegurar que todo pase por revisión.

**Protección para main**
- Requerir Pull Request
- Requerir al menos 1 aprobación
- Requerir status checks

**Protección para qa**
- Requerir Pull Request
- Requerir status checks

**Protección opcional para develop**
- Requerir Pull Request

**Verificación esperada**

Al intentar hacer push directo a main, la operación debe fallar si la protección está configurada correctamente. Esto garantiza que todo cambio pase por revisión antes de llegar a producción.

---

### Ejemplo de feature branch
```bash
git checkout develop
git pull origin develop
git checkout -b feature/SD-001-user-registration
Ejemplo de commits en la feature
git add .
git commit -m "feat(users-service): crear modelo User"
git add .
git commit -m "feat(users-service): implementar registro de usuario"
git add .
git commit -m "test(users-service): agregar pruebas de registro"
git push -u origin feature/SD-001-user-registration
```
**Pull Request esperado**

Después del push de la feature branch, se debe crear un Pull Request desde:
```
feature/SD-001-user-registration → develop
```

**Justificación**

Este flujo permite separar desarrollo, validación y producción. Además, evita que cambios no revisados lleguen directamente a la rama principal del proyecto.

---

## Actividad 3: Primer GitHub Action

Como primera automatización del proyecto, se propone crear un workflow básico de integración continua con **GitHub Actions**. Este workflow permitirá validar el código automáticamente cada vez que se haga un **push** o un **pull request** sobre las ramas principales del proyecto.

### Objetivo

El objetivo de esta actividad es configurar un pipeline sencillo que permita:

- descargar el código del repositorio
- configurar el entorno de Java
- compilar el microservicio
- ejecutar pruebas automáticas
- verificar que el proyecto está listo para integrarse sin errores

### Archivo a crear

La ruta del archivo debe ser:

`.github/workflows/ci.yml`

### Contenido del archivo `ci.yml`

```yml
name: CI Pipeline

on:
  push:
    branches: [ develop, qa, main ]
  pull_request:
    branches: [ develop, qa, main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout código
        uses: actions/checkout@v4

      - name: Setup Java 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Build users-service
        run: |
          cd users-service
          mvn clean compile

      - name: Run tests users-service
        run: |
          cd users-service
          mvn test

      - name: Build verificado
        run: echo "Build y tests exitosos"
```

### Explicación del workflow

Este workflow funciona de la siguiente manera:

- **name:** define el nombre del pipeline, en este caso `CI Pipeline`.
- **on:** indica que el workflow se ejecutará cuando haya `push` o `pull_request` en las ramas `develop`, `qa` y `main`.
- **jobs:** agrupa las tareas que se van a ejecutar.
- **runs-on:** indica que el proceso se correrá en una máquina virtual con `ubuntu-latest`.

Dentro del job se definen varios pasos:

1. **Checkout código**  
   Descarga el contenido del repositorio para que GitHub Actions pueda trabajar con él.

2. **Setup Java 17**  
   Configura el entorno con Java 17, que es la versión que se usará para el desarrollo del proyecto.

3. **Build users-service**  
   Ingresa al microservicio `users-service` y ejecuta la compilación con Maven.

4. **Run tests users-service**  
   Corre las pruebas automáticas definidas en ese microservicio.

5. **Build verificado**  
   Muestra un mensaje final para indicar que la compilación y las pruebas terminaron correctamente.

### Verificación esperada

Después de crear el archivo y subirlo al repositorio, se debe comprobar lo siguiente:

- el workflow aparece en la pestaña **Actions** de GitHub
- el pipeline se ejecuta automáticamente al hacer push
- la compilación del servicio se realiza sin errores
- las pruebas automáticas se ejecutan correctamente
- el estado del workflow aparece como exitoso si todo sale bien

### Resultado esperado

Al finalizar esta actividad, el proyecto contará con una primera automatización de integración continua. Esto permitirá validar cambios de manera automática y servirá como base para agregar más verificaciones en el futuro, como análisis de calidad, pruebas de otros microservicios o despliegues automáticos.

### Justificación

GitHub Actions es una herramienta muy útil para automatizar tareas repetitivas dentro del desarrollo de software. En este caso, ayuda a comprobar que el código compila y que las pruebas funcionan antes de integrar cambios importantes al proyecto. Esto mejora la calidad del desarrollo, reduce errores manuales y hace más seguro el trabajo colaborativo del equipo.        

---
<p align="center">
  <img src="./images/peach.gif" alt="Peach" width="250">
</p>
