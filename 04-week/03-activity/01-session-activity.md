# 04-Week - Session 1: Primer Microservicio con Java y Spring Boot

## Actividad 1: Crear el Microservicio Base

Para esta actividad se propone crear el primer microservicio funcional del proyecto, que en este caso será el **users-service**, porque es uno de los servicios base del sistema **Gestión de Citas Inteligente**. La idea es generarlo con Spring Initializr, copiarlo al monorepo, crear la estructura de paquetes y configurar la conexión a PostgreSQL. :contentReference[oaicite:2]{index=2}

### Configuración usada en Spring Initializr

- **Project:** Maven
- **Language:** Java
- **Spring Boot:** 3.x
- **Java:** 17
- **Group:** `co.edu.corhuila`
- **Artifact:** `users-service`

### Dependencias necesarias

- Spring Web
- Spring Data JPA
- PostgreSQL Driver
- Lombok
- Validation
- Actuator
- Spring Boot Starter Test

### Ubicación dentro del monorepo

```text
users-service/
```

### Estructura propuesta del microservicio

```text
users-service/
└── src/
    └── main/
        ├── java/co/edu/corhuila/usersservice/
        │   ├── UsersServiceApplication.java
        │   ├── controller/
        │   │   └── UserController.java
        │   ├── service/
        │   │   ├── IUserService.java
        │   │   └── UserServiceImpl.java
        │   ├── repository/
        │   │   └── IUserRepository.java
        │   ├── entity/
        │   │   └── User.java
        │   ├── dto/
        │   │   ├── UserRequestDTO.java
        │   │   └── UserResponseDTO.java
        │   └── exception/
        │       ├── GlobalExceptionHandler.java
        │       └── ResourceNotFoundException.java
        └── resources/
            └── application.yml
```

### Archivo `application.yml`

```yml
server:
  port: 8081

spring:
  application:
    name: users-service
  datasource:
    url: jdbc:postgresql://localhost:5432/usersdb
    username: postgres
    password: postgres
    driver-class-name: org.postgresql.Driver
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
    properties:
      hibernate:
        format_sql: true
        dialect: org.hibernate.dialect.PostgreSQLDialect

management:
  endpoints:
    web:
      exposure:
        include: health,info
```

### Observación

En esta primera parte se deja listo el proyecto base para comenzar a desarrollar el CRUD del microservicio. La guía muestra esta misma lógica: generar el proyecto, organizarlo por capas y configurar PostgreSQL desde `application.yml`. También advierte que `ddl-auto: update` es solo para desarrollo. 

---

## Actividad 2: Implementar CRUD Completo

En esta actividad se implementa el CRUD del microservicio de usuarios con los 5 endpoints básicos: listar todos, obtener por id, crear, actualizar y eliminar. También se define la entidad, el repository, el service y el controller, como muestra la estructura por capas de la sesión. 

### Entidad principal: `User`

```java
package co.edu.corhuila.usersservice.entity;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "users")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, unique = true, length = 150)
    private String email;

    @Column(nullable = false)
    private String password;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        this.updatedAt = LocalDateTime.now();
    }
}
```

### Repository: `IUserRepository`

```java
package co.edu.corhuila.usersservice.repository;

import co.edu.corhuila.usersservice.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface IUserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);
}
```

### Interface del servicio: `IUserService`

```java
package co.edu.corhuila.usersservice.service;

import co.edu.corhuila.usersservice.entity.User;
import java.util.List;

public interface IUserService {
    List<User> findAll();
    User findById(Long id);
    User save(User user);
    User update(Long id, User user);
    void deleteById(Long id);
}
```

### Implementación del servicio: `UserServiceImpl`

```java
package co.edu.corhuila.usersservice.service;

import co.edu.corhuila.usersservice.entity.User;
import co.edu.corhuila.usersservice.repository.IUserRepository;
import co.edu.corhuila.usersservice.exception.ResourceNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements IUserService {

    private final IUserRepository userRepository;

    @Override
    public List<User> findAll() {
        return userRepository.findAll();
    }

    @Override
    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException(
                "Usuario no encontrado con id: " + id));
    }

    @Override
    public User save(User user) {
        if (userRepository.existsByEmail(user.getEmail())) {
            throw new RuntimeException("El email ya existe: " + user.getEmail());
        }
        return userRepository.save(user);
    }

    @Override
    public User update(Long id, User user) {
        User existing = findById(id);
        existing.setName(user.getName());
        existing.setEmail(user.getEmail());
        existing.setPassword(user.getPassword());
        return userRepository.save(existing);
    }

    @Override
    public void deleteById(Long id) {
        User existing = findById(id);
        userRepository.delete(existing);
    }
}
```

### Excepción personalizada: `ResourceNotFoundException`

```java
package co.edu.corhuila.usersservice.exception;

public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}
```

### Controller: `UserController`

```java
package co.edu.corhuila.usersservice.controller;

import co.edu.corhuila.usersservice.entity.User;
import co.edu.corhuila.usersservice.service.IUserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class UserController {

    private final IUserService userService;

    @GetMapping
    public ResponseEntity<List<User>> findAll() {
        return ResponseEntity.ok(userService.findAll());
    }

    @GetMapping("/{id}")
    public ResponseEntity<User> findById(@PathVariable Long id) {
        return ResponseEntity.ok(userService.findById(id));
    }

    @PostMapping
    public ResponseEntity<User> save(@RequestBody User user) {
        User saved = userService.save(user);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @PutMapping("/{id}")
    public ResponseEntity<User> update(@PathVariable Long id, @RequestBody User user) {
        return ResponseEntity.ok(userService.update(id, user));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteById(@PathVariable Long id) {
        userService.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
```

### Endpoints implementados

- `GET /api/v1/users` → listar todos los usuarios
- `GET /api/v1/users/{id}` → obtener usuario por id
- `POST /api/v1/users` → crear usuario
- `PUT /api/v1/users/{id}` → actualizar usuario
- `DELETE /api/v1/users/{id}` → eliminar usuario

### Ejemplo para probar en Postman

#### Crear usuario
```json
{
  "name": "Catalina Cortes",
  "email": "catalina@mail.com",
  "password": "Pass123!"
}
```

#### Respuesta esperada
```json
{
  "id": 1,
  "name": "Catalina Cortes",
  "email": "catalina@mail.com",
  "password": "Pass123!",
  "createdAt": "2026-03-27T16:00:00",
  "updatedAt": "2026-03-27T16:00:00"
}
```

### Observación

Con esto ya queda implementado el CRUD completo del primer microservicio del proyecto. La guía pide exactamente esos cinco endpoints y probarlos con Postman verificando que los datos sí queden guardados en PostgreSQL. 

---

## Actividad 3: Hacer Commit y PR

En esta actividad se organiza el trabajo con Git usando una feature branch, commits descriptivos y un Pull Request hacia `develop`, tal como lo pide la práctica. La idea es simular un flujo de trabajo real en equipo. :contentReference[oaicite:6]{index=6}

### Nombre de la rama

```bash
git checkout develop
git pull origin develop
git checkout -b feature/SD-001-first-microservice
```

### Commits sugeridos

```bash
git add .
git commit -m "feat(users-service): crear entidad User"

git add .
git commit -m "feat(users-service): crear repository IUserRepository"

git add .
git commit -m "feat(users-service): implementar service y interfaz IUserService"

git add .
git commit -m "feat(users-service): crear controller con endpoints CRUD"

git add .
git commit -m "chore(users-service): configurar application.yml y conexion PostgreSQL"
```

### Push de la rama

```bash
git push -u origin feature/SD-001-first-microservice
```

### Pull Request esperado

Después del push, se debe crear un Pull Request desde:

```text
feature/SD-001-first-microservice → develop
```

### Code Review esperado

Un compañero del equipo debe revisar el código y validar aspectos como:

- que la estructura por capas esté bien organizada
- que los nombres de paquetes y clases sean claros
- que los endpoints funcionen correctamente
- que el CRUD sí guarde y lea datos desde PostgreSQL
- que no haya errores de compilación o malas prácticas evidentes

### Observación

Este flujo de trabajo ayuda a mantener orden en el repositorio, separar el desarrollo en ramas y asegurar que los cambios pasen por revisión antes de integrarse a `develop`. Eso coincide con la actividad de clase, que pide crear la rama, hacer commits por partes, subirla y abrir un PR para revisión. :contentReference[oaicite:7]{index=7}

---

## Reflexión final

Usamos interfaces como `IUserService` porque ayudan a separar el contrato de la implementación, lo que hace el código más ordenado, más fácil de mantener y más flexible para cambios futuros. JPA e Hibernate tienen ventaja frente a escribir SQL manualmente porque reducen trabajo repetitivo, permiten mapear objetos a tablas más fácil y aceleran el desarrollo del microservicio. Finalmente, la estructura **Controller → Service → Repository** se relaciona con SOLID porque separa responsabilidades, evita mezclar lógica de negocio con acceso a datos y hace el proyecto más limpio y escalable. 