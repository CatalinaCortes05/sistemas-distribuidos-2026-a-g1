# Week 2 - session 1: Definición del Proyecto
<p align="center">
  <img src="./images/gatoo.gif" alt="Gatoo" width="150">
</p>

## Actividad 1: Escribir User Stories

A continuación se presentan 10 User Stories para el proyecto **Gestión-De-Citas-Inteligente**, usando el formato solicitado: **Como [rol], quiero [acción], para [beneficio]**. También se incluyen criterios de aceptación, story points y priorización MoSCoW. :contentReference[oaicite:1]{index=1}

---

### US-001: Registro de usuario

**Como** paciente  
**Quiero** crear una cuenta con correo y contraseña  
**Para** poder acceder a la plataforma y gestionar mis citas

#### Criterios de aceptación
- [ ] El formulario valida que el correo tenga formato correcto
- [ ] La contraseña debe tener mínimo 8 caracteres
- [ ] No se permiten correos duplicados
- [ ] El usuario queda registrado correctamente
- [ ] El sistema muestra mensaje de registro exitoso

**Story Points:** 5  
**Prioridad:** Must Have

---

### US-002: Inicio de sesión

**Como** usuario registrado  
**Quiero** iniciar sesión con mis credenciales  
**Para** acceder a mi cuenta y usar las funcionalidades del sistema

#### Criterios de aceptación
- [ ] El sistema valida correo y contraseña
- [ ] Si las credenciales son correctas, permite el acceso
- [ ] Si son incorrectas, muestra mensaje de error
- [ ] El sistema crea una sesión válida

**Story Points:** 5  
**Prioridad:** Must Have

---

### US-003: Consultar disponibilidad médica

**Como** paciente  
**Quiero** ver los horarios disponibles de los médicos  
**Para** elegir una cita que se ajuste a mi tiempo

#### Criterios de aceptación
- [ ] El sistema muestra lista de médicos disponibles
- [ ] Se visualizan fechas y horas disponibles
- [ ] No se muestran horarios ya ocupados
- [ ] La información se actualiza después de cada reserva

**Story Points:** 5  
**Prioridad:** Must Have

---

### US-004: Agendar cita médica

**Como** paciente  
**Quiero** reservar una cita con un médico  
**Para** recibir atención en la fecha y hora seleccionada

#### Criterios de aceptación
- [ ] El usuario puede seleccionar médico, fecha y hora
- [ ] El sistema verifica disponibilidad antes de guardar
- [ ] La cita queda registrada correctamente
- [ ] El sistema confirma la reserva al usuario

**Story Points:** 8  
**Prioridad:** Must Have

---

### US-005: Cancelar cita

**Como** paciente  
**Quiero** cancelar una cita agendada  
**Para** liberar el horario y reorganizar mi agenda

#### Criterios de aceptación
- [ ] El usuario puede ver sus citas activas
- [ ] El sistema permite cancelar una cita antes de la fecha programada
- [ ] El estado de la cita cambia a cancelada
- [ ] El horario vuelve a quedar disponible

**Story Points:** 5  
**Prioridad:** Must Have

---

### US-006: Reprogramar cita

**Como** paciente  
**Quiero** cambiar la fecha u hora de una cita  
**Para** ajustarla a una nueva necesidad

#### Criterios de aceptación
- [ ] El usuario puede seleccionar una nueva fecha disponible
- [ ] El sistema verifica que el nuevo horario esté libre
- [ ] La cita se actualiza correctamente
- [ ] El sistema confirma la reprogramación

**Story Points:** 5  
**Prioridad:** Should Have

---

### US-007: Gestión de agenda médica

**Como** médico  
**Quiero** administrar mis horarios de atención  
**Para** organizar mi disponibilidad de citas

#### Criterios de aceptación
- [ ] El médico puede agregar horarios disponibles
- [ ] El médico puede bloquear horarios no disponibles
- [ ] Los cambios se reflejan para los pacientes
- [ ] No se pueden crear horarios superpuestos

**Story Points:** 8  
**Prioridad:** Must Have

---

### US-008: Recordatorio de cita

**Como** paciente  
**Quiero** recibir un recordatorio de mi cita  
**Para** no olvidarla

#### Criterios de aceptación
- [ ] El sistema envía recordatorio antes de la cita
- [ ] El recordatorio incluye fecha, hora y médico
- [ ] El envío puede realizarse por correo o notificación
- [ ] Solo aplica a citas activas

**Story Points:** 3  
**Prioridad:** Should Have

---

### US-009: Historial de citas

**Como** paciente  
**Quiero** consultar mi historial de citas  
**Para** revisar mis atenciones anteriores

#### Criterios de aceptación
- [ ] El usuario puede ver citas pasadas y canceladas
- [ ] La información muestra fecha, médico y estado
- [ ] El historial está ordenado por fecha

**Story Points:** 3  
**Prioridad:** Could Have

---

### US-010: Panel administrativo

**Como** administrador  
**Quiero** gestionar usuarios, médicos y citas  
**Para** supervisar el funcionamiento general del sistema

#### Criterios de aceptación
- [ ] El administrador puede visualizar usuarios registrados
- [ ] Puede consultar médicos y citas activas
- [ ] Puede desactivar usuarios si es necesario
- [ ] Puede ver el estado general del sistema

**Story Points:** 8  
**Prioridad:** Should Have

---

## Priorización MoSCoW

### Must Have
- US-001 Registro de usuario
- US-002 Inicio de sesión
- US-003 Consultar disponibilidad médica
- US-004 Agendar cita médica
- US-005 Cancelar cita
- US-007 Gestión de agenda médica

### Should Have
- US-006 Reprogramar cita
- US-008 Recordatorio de cita
- US-010 Panel administrativo

### Could Have
- US-009 Historial de citas

### Won't Have (por ahora)
- Videollamadas médicas
- Integración con pagos en línea
- Despliegue en nube pública

---

## Actividad 2: Diagrama de Arquitectura

La arquitectura inicial del proyecto se plantea con base en microservicios, definiendo el API Gateway, los servicios principales, las bases de datos y la forma de comunicación entre componentes.

### Arquitectura propuesta del sistema

El sistema **Gestión-De-Citas-Inteligente** tendrá una arquitectura base con los siguientes componentes:

### 1. API Gateway
- Será el punto de entrada único del sistema
- Se encargará del enrutamiento de solicitudes
- También podrá centralizar autenticación y control de acceso
- Tecnología sugerida: **Spring Cloud Gateway**

### 2. Microservicio de Users
- Maneja el registro, inicio de sesión y gestión de usuarios
- Tecnología sugerida: **Java + Spring Boot**
- Base de datos: **PostgreSQL**

### 3. Microservicio de Turnos
- Maneja la creación, consulta, cancelación y reprogramación de turnos
- Tecnología sugerida: **Java + Spring Boot**
- Base de datos: **PostgreSQL**

### 4. Microservicio de Notificaciones
- Se encarga de enviar recordatorios y avisos relacionados con los turnos
- Tecnología sugerida: **Java + Spring Boot**
- Base de datos: **PostgreSQL**

### Comunicación entre servicios
- El cliente envía solicitudes al **API Gateway**
- El **API Gateway** redirige la petición al microservicio correspondiente
- Los microservicios se comunican inicialmente mediante **HTTP**
- En una futura mejora se podría implementar comunicación asíncrona para eventos y recordatorios

### Diagrama ASCII

```text
┌─────────────┐
│   Cliente   │
└──────┬──────┘
       │ HTTP
       ▼
┌────────────────────┐
│    API Gateway     │
│ Spring Cloud Gate. │
└──────┬─────────────┘
       │
       ├───────────────┬──────────────────┐
       ▼               ▼                  ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ User Service │ │ Turnos Serv. │ │ Notification │
│ Spring Boot  │ │ Spring Boot  │ │ Service      │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ PostgreSQL   │ │ PostgreSQL   │ │ PostgreSQL   │
│ Users DB     │ │ Turnos DB    │ │ Notify DB    │
└──────────────┘ └──────────────┘ └──────────────┘
```

### Observación

Esta arquitectura permite separar responsabilidades, organizar mejor el sistema y escalar cada componente de forma independiente. Además, el uso de un API Gateway facilita centralizar el acceso a los microservicios y mejorar el control de las solicitudes del sistema.

---

## Actividad 3: Configurar GitHub Project

Para la organización del proyecto **Gestión-De-Citas-Inteligente** se propone crear un tablero en GitHub Projects tipo **Kanban**, con columnas, issues, labels y milestone relacionados con los microservicios **users**, **turnos** y **notificaciones**.

### Nombre del proyecto

**Gestión-De-Citas-Inteligente Board**

### Tipo de tablero

**Kanban**

### Columnas del tablero
- Backlog
- To Do
- In Progress
- In Review
- Done

### Milestone
- **Release 1 — MVP**

### Labels propuestas

#### Prioridad
- `priority:high`
- `priority:medium`
- `priority:low`

#### Tipo
- `type:feature`
- `type:bug`
- `type:docs`
- `type:refactor`

#### Servicio
- `service:gateway`
- `service:users`
- `service:turnos`
- `service:notificaciones`

#### Sprint / Release
- `sprint:1`
- `release:mvp`

### 5 Issues iniciales del proyecto

#### Issue 1: US-001 Registro de usuario
- Tipo: `type:feature`
- Prioridad: `priority:high`
- Servicio: `service:users`
- Sprint: `sprint:1`
- Release: `release:mvp`

#### Issue 2: US-002 Inicio de sesión
- Tipo: `type:feature`
- Prioridad: `priority:high`
- Servicio: `service:users`
- Sprint: `sprint:1`
- Release: `release:mvp`

#### Issue 3: US-004 Agendar turno
- Tipo: `type:feature`
- Prioridad: `priority:high`
- Servicio: `service:turnos`
- Sprint: `sprint:1`
- Release: `release:mvp`

#### Issue 4: US-005 Cancelar turno
- Tipo: `type:feature`
- Prioridad: `priority:high`
- Servicio: `service:turnos`
- Sprint: `sprint:1`
- Release: `release:mvp`

#### Issue 5: US-008 Enviar recordatorio de turno
- Tipo: `type:feature`
- Prioridad: `priority:medium`
- Servicio: `service:notificaciones`
- Sprint: `sprint:1`
- Release: `release:mvp`

### Observación

La configuración de GitHub Projects permitirá organizar el trabajo del equipo de forma visual, relacionando cada historia de usuario con el microservicio correspondiente. Además, el uso de labels y milestones facilitará el seguimiento del avance del MVP y la distribución de tareas por prioridad, servicio y sprint.