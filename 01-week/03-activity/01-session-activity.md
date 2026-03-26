# Week 1 - 01-session Actividades
<p align="center">
  <img src="./images/miau.gif" alt="Miau" width="150">
</p>


## Actividad 1: Identificar sistemas distribuidos

### 1. Spotify — Sistema distribuido 

Spotify es un sistema distribuido porque integra varios servicios que trabajan al mismo tiempo, como reproducción de música, gestión de usuarios, búsqueda, recomendaciones y almacenamiento de canciones. Aunque el usuario ve una sola aplicación, realmente por detrás existen varios componentes conectados que permiten escuchar música desde distintos dispositivos y en tiempo real.

### 2. Uber — Sistema distribuido

Uber es un sistema distribuido porque coordina usuarios, conductores, ubicaciones, pagos, rutas y notificaciones en tiempo real. Toda esa información se procesa desde diferentes servicios que se comunican entre sí para mostrar al usuario una sola plataforma. Además, debe funcionar de forma simultánea para muchas personas en distintos lugares.

### 3. Bloc de notas — Sistema monolítico

El bloc de notas es un sistema monolítico porque funciona como una sola aplicación local en un único equipo. Su tarea principal es escribir y guardar texto, sin depender de múltiples servidores, nodos o servicios distribuidos para operar normalmente.

## Actividad 2: Formación de equipos

El equipo de trabajo estará conformado por 3 o 4 integrantes. Los roles iniciales propuestos son:


| Rol | Integrante |
|---|---|
| Tech Lead | Yeison Scarpetta |
| Backend Dev | Catalina Cortes |
| Frontend Dev | Sofía Perafán |
| DevOps | Nicolas Alvarez |

Estos roles nos permiten organizar mejor el trabajo, repartir responsabilidades y facilitar el desarrollo del proyecto durante el semestre. Según las necesidades del equipo, los roles podrán ajustarse o rotarse.

## Actividad 3: Brainstorming del proyecto

### Idea 1: Sistema de reservas médicas
**Problema que resuelve:**  
Permite a los pacientes agendar citas médicas de forma más rápida y organizada, evitando filas y mejorando la atención.

**Microservicios que necesitaría:**  
- Microservicio de usuarios  
- Microservicio de turnos   
- Microservicio de notificaciones  

**Datos que manejaría:**  
Información de pacientes, médicos, horarios, especialidades, citas programadas y recordatorios.

### Idea 2: Plataforma de domicilios para restaurantes
**Problema que resuelve:**  
Facilita la gestión de pedidos a domicilio, conectando clientes, restaurantes y repartidores en una sola plataforma.

**Microservicios que necesitaría:**  
- Microservicio de usuarios  
- Microservicio de restaurantes  
- Microservicio de pedidos  
- Microservicio de pagos  
- Microservicio de entregas  

**Datos que manejaría:**  
Clientes, menús, pedidos, direcciones, pagos, repartidores y estados de entrega.

## Conclusión

Las dos ideas propuestas se benefician del uso de sistemas distribuidos, ya que permiten separar funciones, mejorar la organización del sistema y facilitar su crecimiento. Además, este tipo de arquitectura ayuda a soportar múltiples usuarios y procesos al mismo tiempo.