# Semana 2 - Sesión 2: Microservicios — DDD y Bounded Contexts

## Actividad 1: Identificar Subdominios
Para el proyecto **Gestión-De-Citas-Inteligente**, se identifican tres subdominios principales. En cada uno se definen las entidades, value objects y su clasificación como **Core**, **Supporting** o **Generic**.

---

### 1. Subdominio: Gestión de Usuarios
**Tipo:** Supporting

#### Entidades principales
- **Usuario**
- **Rol**
- **Sesión**

#### Value Objects
- **Email**
- **Contraseña**
- **Nombre completo**
- **Documento**
- **Teléfono**

#### Justificación
Este subdominio se encarga del registro, autenticación y administración de usuarios del sistema. Aunque es muy importante para el funcionamiento general, no representa el corazón del negocio, porque el valor principal del proyecto está en la gestión de turnos médicos.

---

### 2. Subdominio: Gestión de Turnos
**Tipo:** Core

#### Entidades principales
- **Turno**
- **Médico**
- **Paciente**
- **Agenda**

#### Value Objects
- **Fecha**
- **Hora**
- **Estado del turno**
- **Especialidad**
- **Motivo de consulta**

#### Justificación
Este es el subdominio principal del sistema, porque aquí ocurre la funcionalidad más importante: crear, consultar, cancelar y reprogramar turnos. Por eso se considera el **Core Domain** del proyecto.

---

### 3. Subdominio: Notificaciones
**Tipo:** Generic

#### Entidades principales
- **Notificación**
- **Plantilla de mensaje**
- **Historial de envíos**

#### Value Objects
- **Mensaje**
- **Asunto**
- **Fecha de envío**
- **Canal de envío**
- **Estado de entrega**

#### Justificación
Este subdominio se encarga de enviar recordatorios y avisos al usuario. Es útil y mejora la experiencia, pero no define por sí solo el valor principal del negocio. Por eso se clasifica como **Generic**, ya que es un servicio común que podría reutilizarse en muchos sistemas. La guía pide precisamente distinguir entre subdominios y clasificarlos como core, supporting o generic. :contentReference[oaicite:2]{index=2} :contentReference[oaicite:3]{index=3}

---

## Actividad 2: Dibujar Context Map

Con base en los subdominios identificados, se propone el siguiente **Context Map** del sistema.

### Bounded Contexts identificados
- **Usuarios**
- **Turnos**
- **Notificaciones**

### Relaciones entre contextos
- **Usuarios → Turnos:** comunicación por **REST**
- **Turnos → Notificaciones:** comunicación por **eventos asíncronos**
- **Usuarios → Notificaciones:** comparte información básica del usuario para envío de mensajes

### Datos que se comparten
- Desde **Usuarios** hacia **Turnos**:
  - `user_id`
  - nombre del paciente
  - rol del usuario

- Desde **Turnos** hacia **Notificaciones**:
  - fecha del turno
  - hora del turno
  - estado del turno
  - médico asignado
  - paciente relacionado

- Desde **Usuarios** hacia **Notificaciones**:
  - correo electrónico
  - nombre del usuario

### Context Map en ASCII

```text
┌────────────────────┐
│      USUARIOS      │
│                    │
│ • Registro         │
│ • Autenticación    │
│ • Perfil           │
└─────────┬──────────┘
          │
          │ REST API
          │ comparte: user_id, nombre, rol
          ▼
┌────────────────────┐
│      TURNOS        │
│                    │
│ • Crear turno      │
│ • Cancelar turno   │
│ • Reprogramar      │
│ • Consultar agenda │
└─────────┬──────────┘
          │
          │ Eventos asíncronos
          │ comparte: fecha, hora, estado, médico, paciente
          ▼
┌────────────────────┐
│   NOTIFICACIONES   │
│                    │
│ • Recordatorios    │
│ • Avisos de cambio │
│ • Confirmaciones   │
└────────────────────┘
```

### Explicación del diseño
Dentro del bounded context de Usuarios, la palabra “usuario” significa identidad, acceso y perfil.
Dentro del bounded context de Turnos, lo importante es la reserva, el horario y el estado del turno.
Dentro del bounded context de Notificaciones, el foco está en los mensajes, su contenido y su entrega.

Esto sigue la idea de DDD de que cada bounded context tiene un significado propio y consistente para sus términos, y que el context map muestra claramente las relaciones entre contextos y su forma de comunicación.

---
## Actividad 3: Mapear Bounded Contexts a Microservicios

A continuación se mapea cada bounded context a su microservicio correspondiente, indicando base de datos, método de comunicación y release estimada.

| Bounded Context | Microservicio | Base de Datos | Método de Comunicación | Release |
|---|---|---|---|---|
| Usuarios | `users-service` | PostgreSQL | REST API + JWT | Release 1 |
| Turnos | `turnos-service` | PostgreSQL | REST API | Release 1 |
| Notificaciones | `notifications-service` | PostgreSQL | Eventos asíncronos | Release 2 |

### Explicación del mapeo

#### Users Context → `users-service`
Este microservicio se encarga del registro, inicio de sesión, autenticación y administración de usuarios. Se implementa en **Release 1** porque el sistema necesita identificar y validar a los usuarios desde el inicio.

#### Turnos Context → `turnos-service`
Este microservicio representa el núcleo del negocio, ya que administra la creación, consulta, cancelación y reprogramación de turnos. También se implementa en **Release 1** por ser la funcionalidad principal del MVP.

#### Notificaciones Context → `notifications-service`
Este microservicio se encarga de enviar recordatorios y avisos automáticos relacionados con los turnos. Se deja para **Release 2**, ya que complementa el sistema pero no bloquea el funcionamiento básico del MVP.

### Observación
Este mapeo permite que cada microservicio tenga una responsabilidad clara, su propia base de datos y una comunicación definida con los demás servicios. Además, facilita el mantenimiento, la escalabilidad y la evolución del sistema por etapas.

---

### Reflexión final
#### ¿Por qué DDD es más efectivo que dividir por capas técnicas?
DDD es más efectivo porque organiza el sistema según el negocio y no solo según la estructura técnica. Dividir por capas como controller, service y repository puede mezclar responsabilidades de distintos dominios, mientras que DDD ayuda a encontrar límites claros entre contextos y servicios. La sesión lo presenta como la metodología más efectiva para identificar los límites correctos de microservicios.

#### ¿Qué pasa si dos microservicios necesitan acceder a la misma tabla?
Eso genera acoplamiento fuerte y rompe el principio de database per service. Cada microservicio debe tener su propia base de datos y acceder a la información de otros servicios mediante APIs o eventos, no entrando directamente a sus tablas. La guía insiste en que cada servicio tenga su propia BD para evitar acoplamiento por datos compartidos.

#### ¿Cómo el Ubiquitous Language reduce los malentendidos en el equipo?
El Ubiquitous Language hace que todos usen los mismos términos con el mismo significado dentro de cada contexto. Así se reducen confusiones entre negocio y desarrollo, y cada bounded context mantiene un lenguaje claro y consistente. La sesión lo define como un lenguaje compartido entre desarrolladores y negocio.

---
<p align="center">
  <img src="./images/gato.gif" alt="Gato" width="150">
</p>
