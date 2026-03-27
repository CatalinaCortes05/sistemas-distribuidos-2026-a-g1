# 04-Week - Session 2: PostgreSQL y Persistencia con Spring Data JPA

## Actividad 1: Levantar PostgreSQL con Docker

Para esta actividad se configuró PostgreSQL como base de datos del microservicio `users-service`, siguiendo el principio de **database per service**, donde cada microservicio tiene su propia base de datos y ningún otro servicio accede directamente a ella.

### Archivo `docker-compose.yml`

```yml
version: '3.8'

services:
  postgres-users-service:
    image: postgres:16-alpine
    container_name: postgres-users-service
    environment:
      POSTGRES_DB: usersdb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - pgdata-users-service:/var/lib/postgresql/data
    networks:
      - sd-network

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: pgadmin-users
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@corhuila.edu.co
      PGADMIN_DEFAULT_PASSWORD: admin123
    ports:
      - "5050:80"
    networks:
      - sd-network

volumes:
  pgdata-users-service:

networks:
  sd-network:
    driver: bridge
```

### Pasos realizados

1. Se agregó el archivo `docker-compose.yml` en la raíz del monorepo.
2. Se ejecutó el siguiente comando:

```bash
docker-compose up -d
```

3. Se verificó que los contenedores estuvieran activos con:

```bash
docker ps
```

4. Se ingresó a pgAdmin desde:

```text
http://localhost:5050
```

5. Se configuró la conexión con estos datos:
   - **Host:** `postgres-users-service`
   - **Port:** `5432`
   - **User:** `postgres`
   - **Password:** `postgres`

6. Después se arrancó el microservicio `users-service` para verificar que la tabla se creara automáticamente en PostgreSQL.

### Configuración en `application.yml`

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

Con esta configuración, el microservicio `users-service` ya queda conectado a su propia base de datos en PostgreSQL. Además, pgAdmin permite revisar visualmente las tablas creadas y confirmar que la persistencia está funcionando bien.

---

## Actividad 2: Implementar 2+ Entidades con Relación

Para esta actividad, según el dominio del proyecto, se implementaron dos entidades relacionadas dentro del microservicio `users-service`: **Role** y **User**. La relación definida es de **OneToMany / ManyToOne**, donde un rol puede tener muchos usuarios y cada usuario pertenece a un solo rol.

### Entidad `Role`

```java
package co.edu.corhuila.usersservice.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.*;
import java.util.List;

@Entity
@Table(name = "roles")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Role {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 50)
    private String name;

    @OneToMany(mappedBy = "role", cascade = CascadeType.ALL)
    @JsonIgnore
    private List<User> users;
}
```

### Entidad `User`

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

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "role_id", nullable = false)
    private Role role;

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

### DTO de entrada `UserRequestDTO`

```java
package co.edu.corhuila.usersservice.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record UserRequestDTO(
    @NotBlank(message = "El nombre es obligatorio")
    String name,

    @NotBlank(message = "El correo es obligatorio")
    @Email(message = "Debe ingresar un correo válido")
    String email,

    @NotBlank(message = "La contraseña es obligatoria")
    @Size(min = 6, message = "La contraseña debe tener mínimo 6 caracteres")
    String password,

    @NotNull(message = "El roleId es obligatorio")
    Long roleId
) {}
```

### DTO de salida `UserResponseDTO`

```java
package co.edu.corhuila.usersservice.dto;

import co.edu.corhuila.usersservice.entity.User;
import java.time.LocalDateTime;

public record UserResponseDTO(
    Long id,
    String name,
    String email,
    String roleName,
    LocalDateTime createdAt
) {
    public static UserResponseDTO fromEntity(User user) {
        return new UserResponseDTO(
            user.getId(),
            user.getName(),
            user.getEmail(),
            user.getRole().getName(),
            user.getCreatedAt()
        );
    }
}
```

### Repository de `Role`

```java
package co.edu.corhuila.usersservice.repository;

import co.edu.corhuila.usersservice.entity.Role;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface IRoleRepository extends JpaRepository<Role, Long> {
    Optional<Role> findByName(String name);
}
```

### Repository de `User`

```java
package co.edu.corhuila.usersservice.repository;

import co.edu.corhuila.usersservice.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface IUserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);
}
```

### Service de `User`

```java
package co.edu.corhuila.usersservice.service;

import co.edu.corhuila.usersservice.dto.UserRequestDTO;
import co.edu.corhuila.usersservice.dto.UserResponseDTO;
import java.util.List;

public interface IUserService {
    List<UserResponseDTO> findAll();
    UserResponseDTO findById(Long id);
    UserResponseDTO save(UserRequestDTO dto);
    UserResponseDTO update(Long id, UserRequestDTO dto);
    void deleteById(Long id);
}
```

### Implementación del service

```java
package co.edu.corhuila.usersservice.service;

import co.edu.corhuila.usersservice.dto.UserRequestDTO;
import co.edu.corhuila.usersservice.dto.UserResponseDTO;
import co.edu.corhuila.usersservice.entity.Role;
import co.edu.corhuila.usersservice.entity.User;
import co.edu.corhuila.usersservice.exception.ResourceNotFoundException;
import co.edu.corhuila.usersservice.repository.IRoleRepository;
import co.edu.corhuila.usersservice.repository.IUserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements IUserService {

    private final IUserRepository userRepository;
    private final IRoleRepository roleRepository;

    @Override
    public List<UserResponseDTO> findAll() {
        return userRepository.findAll()
                .stream()
                .map(UserResponseDTO::fromEntity)
                .toList();
    }

    @Override
    public UserResponseDTO findById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Usuario no encontrado con id: " + id));
        return UserResponseDTO.fromEntity(user);
    }

    @Override
    public UserResponseDTO save(UserRequestDTO dto) {
        if (userRepository.existsByEmail(dto.email())) {
            throw new RuntimeException("El correo ya está registrado");
        }

        Role role = roleRepository.findById(dto.roleId())
                .orElseThrow(() -> new ResourceNotFoundException("Rol no encontrado con id: " + dto.roleId()));

        User user = User.builder()
                .name(dto.name())
                .email(dto.email())
                .password(dto.password())
                .role(role)
                .build();

        return UserResponseDTO.fromEntity(userRepository.save(user));
    }

    @Override
    public UserResponseDTO update(Long id, UserRequestDTO dto) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Usuario no encontrado con id: " + id));

        Role role = roleRepository.findById(dto.roleId())
                .orElseThrow(() -> new ResourceNotFoundException("Rol no encontrado con id: " + dto.roleId()));

        user.setName(dto.name());
        user.setEmail(dto.email());
        user.setPassword(dto.password());
        user.setRole(role);

        return UserResponseDTO.fromEntity(userRepository.save(user));
    }

    @Override
    public void deleteById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Usuario no encontrado con id: " + id));
        userRepository.delete(user);
    }
}
```

### Controller de `User`

```java
package co.edu.corhuila.usersservice.controller;

import co.edu.corhuila.usersservice.dto.UserRequestDTO;
import co.edu.corhuila.usersservice.dto.UserResponseDTO;
import co.edu.corhuila.usersservice.service.IUserService;
import jakarta.validation.Valid;
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
    public ResponseEntity<List<UserResponseDTO>> findAll() {
        return ResponseEntity.ok(userService.findAll());
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserResponseDTO> findById(@PathVariable Long id) {
        return ResponseEntity.ok(userService.findById(id));
    }

    @PostMapping
    public ResponseEntity<UserResponseDTO> save(@Valid @RequestBody UserRequestDTO dto) {
        return ResponseEntity.status(HttpStatus.CREATED).body(userService.save(dto));
    }

    @PutMapping("/{id}")
    public ResponseEntity<UserResponseDTO> update(@PathVariable Long id, @Valid @RequestBody UserRequestDTO dto) {
        return ResponseEntity.ok(userService.update(id, dto));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteById(@PathVariable Long id) {
        userService.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
```

### Prueba en Postman

#### Crear rol
```json
{
  "name": "ADMIN"
}
```

#### Crear usuario
```json
{
  "name": "Catalina Cortes",
  "email": "catalina@corhuila.edu.co",
  "password": "123456",
  "roleId": 1
}
```

### Observación

Con esta actividad ya se tienen dos entidades relacionadas dentro del dominio del microservicio, usando DTOs para no exponer directamente la entidad completa. Esto mejora la seguridad, el orden del código y la claridad de la API.

---

## Actividad 3: Manejo de Errores y Validación

En esta actividad se agregó el manejo global de excepciones y la validación de datos usando anotaciones como `@NotBlank`, `@Email` y `@Size` en los DTOs. La idea es que cuando el usuario envíe información inválida, el sistema responda con un error claro y bien estructurado.

### Excepción personalizada

```java
package co.edu.corhuila.usersservice.exception;

public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}
```

### GlobalExceptionHandler

```java
package co.edu.corhuila.usersservice.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<Map<String, Object>> handleNotFound(ResourceNotFoundException ex) {
        Map<String, Object> error = new HashMap<>();
        error.put("timestamp", LocalDateTime.now().toString());
        error.put("status", 404);
        error.put("error", "Not Found");
        error.put("message", ex.getMessage());

        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }

    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<Map<String, Object>> handleRuntime(RuntimeException ex) {
        Map<String, Object> error = new HashMap<>();
        error.put("timestamp", LocalDateTime.now().toString());
        error.put("status", 400);
        error.put("error", "Bad Request");
        error.put("message", ex.getMessage());

        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, Object>> handleValidation(MethodArgumentNotValidException ex) {
        Map<String, Object> error = new HashMap<>();
        error.put("timestamp", LocalDateTime.now().toString());
        error.put("status", 400);
        error.put("error", "Validation Error");

        Map<String, String> fieldErrors = new HashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(fieldError ->
                fieldErrors.put(fieldError.getField(), fieldError.getDefaultMessage())
        );

        error.put("message", fieldErrors);

        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    }
}
```

### Validaciones en el DTO de entrada

```java
package co.edu.corhuila.usersservice.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record UserRequestDTO(
    @NotBlank(message = "El nombre es obligatorio")
    String name,

    @NotBlank(message = "El correo es obligatorio")
    @Email(message = "Debe ingresar un correo válido")
    String email,

    @NotBlank(message = "La contraseña es obligatoria")
    @Size(min = 6, message = "La contraseña debe tener mínimo 6 caracteres")
    String password,

    @NotNull(message = "El roleId es obligatorio")
    Long roleId
) {}
```

### Ejemplo de request inválido

```json
{
  "name": "",
  "email": "correo-malo",
  "password": "123",
  "roleId": null
}
```

### Respuesta esperada

```json
{
  "timestamp": "2026-03-28T10:30:00",
  "status": 400,
  "error": "Validation Error",
  "message": {
    "name": "El nombre es obligatorio",
    "email": "Debe ingresar un correo válido",
    "password": "La contraseña debe tener mínimo 6 caracteres",
    "roleId": "El roleId es obligatorio"
  }
}
```

### Observación

Con esta configuración, el microservicio devuelve errores más claros y organizados cuando algo falla. Esto mejora mucho la experiencia al probar la API y también facilita encontrar errores durante el desarrollo.

---

## Actividad 4: Commit, PR y Merge

Para esta última actividad se documenta el flujo de trabajo con Git usando una rama feature, commits descriptivos y un Pull Request hacia `develop`.

### Crear la rama de trabajo

```bash
git checkout develop
git pull origin develop
git checkout -b feature/SD-002-postgresql-persistence
```

### Commits sugeridos

```bash
git add .
git commit -m "feat(users-service): add PostgreSQL persistence"

git add .
git commit -m "feat(users-service): add role entity and relationship with user"

git add .
git commit -m "feat(users-service): add DTOs and validation"

git add .
git commit -m "feat(users-service): add global exception handler"
```

### Push de la rama

```bash
git push -u origin feature/SD-002-postgresql-persistence
```

### Pull Request esperado

Después del push, se debe crear un Pull Request desde:

```text
feature/SD-002-postgresql-persistence → develop
```

### Review cruzado esperado

Otro compañero del equipo debe revisar:

- que la conexión a PostgreSQL funcione correctamente
- que las entidades estén bien relacionadas
- que los DTOs se estén usando en las respuestas
- que las validaciones funcionen en Postman
- que los errores regresen mensajes claros
- que el proyecto compile y arranque sin problemas

### Observación

Este flujo ayuda a mantener el trabajo ordenado, con cambios revisados antes de pasar a `develop`. Además, deja evidencia clara en GitHub de commits, PRs y revisión de código.

---

## Reflexión final

El principio **database per service** es importante porque evita que varios microservicios dependan de la misma base de datos, lo cual reduce el acoplamiento y mejora la autonomía de cada servicio. PostgreSQL es una buena opción para este proyecto porque es robusto, soporta muy bien SQL estándar y funciona bien en arquitecturas de microservicios. También, usar DTOs en lugar de exponer directamente las entidades ayuda a proteger datos sensibles como la contraseña, mejora la validación y hace que la API sea más limpia y más fácil de mantener.