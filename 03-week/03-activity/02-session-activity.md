# 03 Week - session 2: API Gateway, Service Discovery y REST APIs

## Actividad 1: Diseñar la API del Proyecto

Para esta actividad se diseñó la API REST del microservicio principal del proyecto, que en este caso es el **microservicio de turnos**, porque es el que maneja la funcionalidad principal del sistema **Gestión-De-Citas-Inteligente**.

### Recurso principal
`/api/v1/turnos`

---

### 1. Listar todos los turnos

**Endpoint:**  
`GET /api/v1/turnos`

**Response esperado:**
```json
[
  {
    "id": 1,
    "fecha": "2026-04-10",
    "hora": "08:00",
    "estado": "PENDIENTE",
    "pacienteId": 12,
    "medico": "Dr. Carlos Ruiz"
  },
  {
    "id": 2,
    "fecha": "2026-04-11",
    "hora": "10:30",
    "estado": "CONFIRMADO",
    "pacienteId": 15,
    "medico": "Dra. Laura Pérez"
  }
]
```

**Código esperado:** `200 OK`

---

### 2. Obtener un turno por ID

**Endpoint:**  
`GET /api/v1/turnos/1`

**Response esperado:**
```json
{
  "id": 1,
  "fecha": "2026-04-10",
  "hora": "08:00",
  "estado": "PENDIENTE",
  "pacienteId": 12,
  "medico": "Dr. Carlos Ruiz"
}
```

**Código esperado:** `200 OK`

**Error posible:**
```json
{
  "message": "Turno no encontrado"
}
```

**Código de error:** `404 Not Found`

---

### 3. Crear un nuevo turno

**Endpoint:**  
`POST /api/v1/turnos`

**Request body:**
```json
{
  "fecha": "2026-04-15",
  "hora": "09:00",
  "estado": "PENDIENTE",
  "pacienteId": 20,
  "medico": "Dr. Andrés Gómez"
}
```

**Response esperado:**
```json
{
  "id": 3,
  "fecha": "2026-04-15",
  "hora": "09:00",
  "estado": "PENDIENTE",
  "pacienteId": 20,
  "medico": "Dr. Andrés Gómez"
}
```

**Código esperado:** `201 Created`

**Error posible:**
```json
{
  "message": "Datos inválidos para crear el turno"
}
```

**Código de error:** `400 Bad Request`

---

### 4. Actualizar un turno

**Endpoint:**  
`PUT /api/v1/turnos/3`

**Request body:**
```json
{
  "fecha": "2026-04-16",
  "hora": "11:00",
  "estado": "CONFIRMADO",
  "pacienteId": 20,
  "medico": "Dr. Andrés Gómez"
}
```

**Response esperado:**
```json
{
  "id": 3,
  "fecha": "2026-04-16",
  "hora": "11:00",
  "estado": "CONFIRMADO",
  "pacienteId": 20,
  "medico": "Dr. Andrés Gómez"
}
```

**Código esperado:** `200 OK`

---

### 5. Eliminar un turno

**Endpoint:**  
`DELETE /api/v1/turnos/3`

**Response esperado:**  
Sin contenido

**Código esperado:** `204 No Content`

**Error posible:**
```json
{
  "message": "No se puede eliminar porque el turno no existe"
}
```

**Código de error:** `404 Not Found`

---

### Códigos HTTP considerados

- `200 OK` → consulta o actualización exitosa
- `201 Created` → recurso creado correctamente
- `204 No Content` → eliminación exitosa
- `400 Bad Request` → datos inválidos
- `404 Not Found` → recurso no encontrado
- `500 Internal Server Error` → error interno del servidor

### Observación

La API se versionó con `/api/v1/` para que en el futuro se puedan hacer cambios sin afectar a los clientes actuales. Además, se usaron los verbos HTTP estándar para mantener una estructura clara, ordenada y fácil de probar.}

---

## Actividad 2: Crear Proyecto Spring Boot del Gateway

Para esta actividad se plantea la creación del proyecto del **API Gateway** usando **Spring Boot** y **Spring Cloud Gateway**, como lo pide la guía. La idea es que el gateway funcione como único punto de entrada para los clientes y redirija las peticiones al microservicio correspondiente.

### Configuración del proyecto en Spring Initializr

- **Project:** Maven
- **Language:** Java
- **Spring Boot:** versión estable
- **Java:** 17
- **Dependencies:**
  - Spring Cloud Gateway
  - Spring Boot Actuator

### Nombre del proyecto
`gateway`

### Ubicación en el monorepo

El proyecto se debe guardar dentro de la carpeta:

```text
gateway/
```

### Archivo `application.yml`

```yml
server:
  port: 8080

spring:
  application:
    name: api-gateway
  cloud:
    gateway:
      routes:
        - id: turnos-service
          uri: http://localhost:8082
          predicates:
            - Path=/api/v1/turnos/**
          filters:
            - StripPrefix=0

      globalcors:
        corsConfigurations:
          '[/**]':
            allowedOrigins: "*"
            allowedMethods:
              - GET
              - POST
              - PUT
              - DELETE
            allowedHeaders: "*"
```

### Explicación de la configuración

- El gateway corre en el puerto `8080`.
- Se registra con el nombre `api-gateway`.
- Se define una ruta hacia el microservicio de turnos.
- Toda petición que llegue a `/api/v1/turnos/**` será redirigida al servicio que corre en `http://localhost:8082`.
- También se configura CORS global para permitir peticiones desde el frontend u otros clientes.

### Dependencias principales del `pom.xml`

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-gateway</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
</dependencies>
```

### Observación

El API Gateway simplifica el acceso de los clientes porque evita que tengan que conocer la URL de cada microservicio. Además, permite centralizar tareas como autenticación, CORS y logging. Esto ayuda a que la arquitectura del sistema esté más organizada y sea más fácil de mantener.

---

## Actividad 3: Probar con Postman / Thunder Client

Para esta actividad se propone documentar y probar los endpoints diseñados en la Actividad 1 usando **Postman** o **Thunder Client**. La idea es crear una colección que sirva como evidencia de prueba y como documentación viva de la API.

### Herramienta elegida
**Thunder Client** en Visual Studio Code

### Nombre de la colección
`Turnos API - Gestion de Citas Inteligente`

### Requests incluidos en la colección

---

### 1. Listar turnos

**Método:** `GET`  
**URL:** `http://localhost:8080/api/v1/turnos`

**Response esperado:**
```json
[
  {
    "id": 1,
    "fecha": "2026-04-10",
    "hora": "08:00",
    "estado": "PENDIENTE",
    "pacienteId": 12,
    "medico": "Dr. Carlos Ruiz"
  }
]
```

---

### 2. Obtener turno por ID

**Método:** `GET`  
**URL:** `http://localhost:8080/api/v1/turnos/1`

**Response esperado:**
```json
{
  "id": 1,
  "fecha": "2026-04-10",
  "hora": "08:00",
  "estado": "PENDIENTE",
  "pacienteId": 12,
  "medico": "Dr. Carlos Ruiz"
}
```

---

### 3. Crear turno

**Método:** `POST`  
**URL:** `http://localhost:8080/api/v1/turnos`

**Body:**
```json
{
  "fecha": "2026-04-15",
  "hora": "09:00",
  "estado": "PENDIENTE",
  "pacienteId": 20,
  "medico": "Dr. Andrés Gómez"
}
```

**Response esperado:**
```json
{
  "id": 3,
  "fecha": "2026-04-15",
  "hora": "09:00",
  "estado": "PENDIENTE",
  "pacienteId": 20,
  "medico": "Dr. Andrés Gómez"
}
```

---

### 4. Actualizar turno

**Método:** `PUT`  
**URL:** `http://localhost:8080/api/v1/turnos/3`

**Body:**
```json
{
  "fecha": "2026-04-16",
  "hora": "11:00",
  "estado": "CONFIRMADO",
  "pacienteId": 20,
  "medico": "Dr. Andrés Gómez"
}
```

**Response esperado:**
```json
{
  "id": 3,
  "fecha": "2026-04-16",
  "hora": "11:00",
  "estado": "CONFIRMADO",
  "pacienteId": 20,
  "medico": "Dr. Andrés Gómez"
}
```

---

### 5. Eliminar turno

**Método:** `DELETE`  
**URL:** `http://localhost:8080/api/v1/turnos/3`

**Response esperado:**  
Sin contenido

**Código esperado:** `204 No Content`

---

### Utilidad de la colección

Esta colección permite:

- probar rápidamente el funcionamiento de la API
- verificar request y response esperados
- documentar ejemplos reales de uso
- dejar una base lista para futuras pruebas del sistema

### Verificación esperada

Después de crear la colección y guardar los endpoints, se debe comprobar lo siguiente:

- los requests aparecen organizados dentro de la colección
- cada endpoint tiene su método y URL correcta
- los bodies de `POST` y `PUT` están bien definidos
- las respuestas coinciden con los ejemplos esperados
- la colección puede servir como evidencia de prueba del microservicio

### Observación

La colección en Thunder Client o Postman funciona como documentación viva, porque guarda ejemplos de requests, bodies y respuestas. Además, facilita volver a probar los endpoints cuando el proyecto siga avanzando.

<p align="center">
  <img src="./images/mochi.gif" alt="Mochi" width="250">
</p>
