# Week 1 - 02-session Actividades

<p align="center">
  <img src="./images/cat.gif" alt="Cat" width="150">
</p>
## Actividad 1: Análisis CAP

Para cada sistema se identifica la combinación del Teorema CAP que prioriza.

### a) Sistema bancario de transferencias
**Clasificación CAP:** CP (Consistency + Partition Tolerance)

**Justificación:**  
Un sistema bancario debe garantizar que los datos sean consistentes, especialmente en operaciones como transferencias o saldos.  
Si ocurre una partición de red, es preferible rechazar temporalmente una operación antes que mostrar datos incorrectos o inconsistentes.

---

### b) Feed de Twitter/X
**Clasificación CAP:** AP (Availability + Partition Tolerance)

**Justificación:**  
En un feed de red social, se prioriza que el servicio siga disponible incluso si la información tarda un poco en sincronizarse completamente.  
Es aceptable cierta consistencia eventual, porque el usuario puede ver publicaciones con pequeños retrasos.

---

### c) Sistema de reservas de cine
**Clasificación CAP:** CP (Consistency + Partition Tolerance)

**Justificación:**  
En un sistema de reservas no se pueden vender dos veces los mismos asientos.  
Por eso es más importante mantener consistencia en la información de disponibilidad, incluso si algunas operaciones deben esperar ante fallos de red.

---

### d) DNS
**Clasificación CAP:** AP (Availability + Partition Tolerance)

**Justificación:**  
El DNS prioriza responder rápidamente y mantenerse disponible.  
Puede existir consistencia eventual entre servidores, pero se prefiere que el sistema siga resolviendo dominios en lugar de quedar inactivo.

---

## Actividad 2: Setup de Git

Cada integrante del equipo realizó la configuración básica de Git y GitHub.

### Verificación del equipo

| Integrante | Git instalado | user.name configurado | user.email configurado | Cuenta GitHub | Práctica de commits y rama |
|-----------|---------------|-----------------------|------------------------|---------------|----------------------------|
| Catalina Cortes | Sí | Sí | Sí | Sí | Sí |
| Yeison Scarpetta | Sí | Sí | Sí | Sí | Sí |
| Sofía Perafán | Sí | Sí | Sí | Sí | Sí |
| Nicolas Alvarez | Sí | Sí | Sí | Sí | Sí |

### Evidencia de práctica

Como parte del trabajo del equipo, ya se realizó la configuración y uso básico de Git y GitHub dentro del fork de la asignatura. Se verificó que el repositorio local estuviera conectado correctamente, se revisaron los remotos configurados y se identificó que `origin` corresponde al fork personal y `upstream` al repositorio original del profesor. Además, se trajeron cambios desde el repositorio principal, se fusionaron en la rama `main` y luego se hizo `push` al fork personal.

### Comandos utilizados

```bash
git status
git remote -v
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```
---

## Actividad 3: Crear Repositorio del Proyecto

### Repositorio creado
**Nombre del repositorio:** Gestión-De-Citas-Inteligente

**Enlace del repositorio:**  
[Pegar aquí enlace del repositorio]

### Ramas configuradas
- `main`
- `develop`
- `qa`

### Colaboradores agregados
- Catalina Cortes
- [Sofia Perafan]
- [Yeison Scarpte]
- [Nicolas Alvarez]

### README creado
Se creó un archivo `README.md` con el nombre del proyecto y los integrantes del equipo.

### Observación
El repositorio servirá como base para organizar el trabajo del proyecto durante el semestre, separando los cambios por ramas según el flujo definido por el equipo.