# Week 5 - Session 2: Retrospectiva y Planificación Release 2

## Actividad 1: Retrospectiva del Equipo

Para esta actividad se realizó una retrospectiva usando el formato **Start - Stop - Continue**, con el fin de identificar mejoras para el siguiente release.

### Start
- Empezar a hacer tests unitarios.
- Hacer revisiones de PR más rápidas.
- Mejorar la documentación del README.
- Organizar mejor las tareas en GitHub Projects.

### Stop
- Dejar PRs sin revisar por mucho tiempo.
- Depender de una sola persona para casi todo.
- Trabajar solo por chat sin dejar evidencia en issues.
- Hacer commits con poca descripción.

### Continue
- Seguir usando commits con convención `feat`, `fix` y `docs`.
- Seguir usando Docker Compose para la base de datos.
- Seguir trabajando con ramas.
- Seguir haciendo code review antes del merge.

### Action items más importantes
1. Agregar tests unitarios en Release 2.  
2. Revisar PRs en menos de 24 horas.  
3. Mejorar el README del proyecto.  

---

## Actividad 2: Analizar Métricas en GitHub

Para esta actividad se revisaron las métricas principales del Release 1 en GitHub.

### Métricas revisadas
- **Commits por miembro:** todos participaron, aunque algunos aportaron más que otros.
- **Pull Requests:** se usaron PRs, pero se puede mejorar el tiempo de revisión.
- **Issues cerrados vs planificados:** se completó la mayoría de los issues del Release 1.
- **Lead Time:** en algunos casos las revisiones tardaron más de lo esperado.

### Autoevaluación del equipo

| Pregunta | Evaluación |
|---|---|
| ¿Todos contribuyeron equitativamente? | 4/5 |
| ¿El código fue revisado? | 4/5 |
| ¿Seguimos Git Flow? | 4/5 |
| ¿La comunicación fue efectiva? | 3/5 |

### Velocity del equipo
- **Issues completados en 5 semanas:** 8  
- **Issues planificados:** 10  

### Observación
Estas métricas ayudan a identificar fortalezas y puntos de mejora para el Release 2.

---

## Actividad 3: Planificar Release 2

Para el Release 2 se definió un segundo microservicio del proyecto.

### Segundo Bounded Context
**Notificaciones**

### Segundo microservicio
**notifications-service**

### Base de datos
**PostgreSQL independiente** (`notificationsdb`)

### Issues propuestos

#### Issue 1: [SD-015] Crear notifications-service
- Proyecto Spring Boot creado
- PostgreSQL independiente configurado
- Estructura base por capas
- Configurado en docker-compose
- Ruta agregada en el API Gateway

**Assignee:** Catalina Cortes

#### Issue 2: [SD-016] Crear entidad Notification
- Entidad creada con JPA
- Campos principales definidos
- Tabla creada en PostgreSQL
- Repository funcionando

**Assignee:** Yeison Scarpetta

#### Issue 3: [SD-017] Implementar CRUD de notifications-service
- Endpoint para listar
- Endpoint para obtener por id
- Endpoint para crear
- Endpoint para actualizar
- Endpoint para eliminar

**Assignee:** Sofía Perafán

#### Issue 4: [SD-018] Agregar ruta en el API Gateway
- Ruta agregada al `application.yml`
- Gateway redirige peticiones correctamente
- Prueba desde Postman

**Assignee:** Nicolas Alvarez

#### Issue 5: [SD-019] Comunicación turnos-service → notifications-service
- Comunicación entre servicios definida
- Endpoint funcional
- Manejo de errores si el servicio no responde

**Assignee:** Catalina Cortes

#### Issue 6: [SD-020] Configurar OpenFeign en turnos-service
- Dependencia agregada
- Cliente Feign creado
- Llamada al notifications-service funcionando

**Assignee:** Yeison Scarpetta

### Organización del tablero
- Backlog
- To Do
- In Progress
- In Review
- Done

---

## Actividad 4: Aplicar un Action Item de Mejora

El action item más votado fue:

**Mejorar el README del proyecto**

### Mejora aplicada
Se actualizó el README con:
- descripción del sistema
- arquitectura de microservicios
- tecnologías usadas
- pasos para ejecutar PostgreSQL con Docker
- pasos para correr los microservicios
- rutas principales de la API
- integrantes del equipo

### Ejemplo agregado al README

```md
## Ejecución del proyecto

### Levantar PostgreSQL con Docker
```bash
docker-compose up -d
```

### Ejecutar users-service
```bash
cd users-service
mvn spring-boot:run
```

### Ejecutar turnos-service
```bash
cd turnos-service
mvn spring-boot:run
```
```

---

## Reflexión final

El Release 1 fue una buena base para construir el primer microservicio y organizar mejor el trabajo del equipo. Con la retrospectiva y la planificación del Release 2, ahora se tiene una visión más clara para mejorar procesos, repartir mejor las tareas y avanzar hacia una arquitectura realmente distribuida.