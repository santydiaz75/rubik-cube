# Data Model: Resolución inicial del cubo de Rubik

## Overview

El MVP persiste cuatro conceptos principales: jugador, partida, cubo inicial y secuencia de estados/movimientos que resuelven el cubo. El modelo conserva la semántica de la constitución y añade los campos operativos mínimos para validar, reproducir y resumir la resolución.

## Entities

### 1. User

**Purpose**: Identificar de forma única a la persona que inicia o reutiliza una sesión.

**Core fields**

| Field | Type | Required | Description |
|------|------|----------|-------------|
| `userId` | string | Yes | Identificador único interno del jugador |
| `username` | string | Yes | Identificador público único usado para reutilizar la sesión |
| `fullname` | string | Yes | Nombre visible actualizado en cada upsert válido |
| `score` | integer | Yes | Último total de movimientos resuelto o resumen acumulado definido por el negocio |
| `createdAt` | datetime | Yes | Fecha de creación |
| `updatedAt` | datetime | Yes | Fecha de última actualización |

**Validation rules**

- `username` debe ser único y normalizado.
- `fullname` no puede estar vacío.
- `score` no puede ser negativo.

**Relationships**

- Un `User` puede tener muchas `Game`.

---

### 2. Game

**Purpose**: Representar una solicitud de resolución concreta hecha por un jugador sobre un cubo inicial.

**Core fields**

| Field | Type | Required | Description |
|------|------|----------|-------------|
| `idGame` | string | Yes | Identificador único de la partida |
| `userId` | string | Yes | Referencia al jugador que lanzó la resolución |
| `idCube` | string | Yes | Referencia al cubo inicial asociado |
| `createdAt` | datetime | Yes | Fecha de creación de la partida |
| `score` | integer | Yes | Número total de movimientos de la solución |
| `status` | enum | Yes | `created`, `solving`, `completed`, `failed` |
| `currentStep` | integer | Yes | Posición actual reproducida, usada para reanudar el player |
| `errorMessage` | string/null | No | Motivo de fallo si no se puede resolver |

**Validation rules**

- `userId` debe apuntar a un `User` existente.
- `idCube` debe apuntar a un `Cube` existente.
- `score` debe ser `0` o mayor.
- `currentStep` debe mantenerse entre `0` y `score`.

**Relationships**

- Una `Game` pertenece a un `User`.
- Una `Game` referencia un `Cube`.
- Una `Game` tiene muchos `CubeStateStep`.

**State transitions**

| From | To | Trigger |
|------|----|---------|
| `created` | `solving` | La solicitud de resolución es aceptada |
| `solving` | `completed` | El solver devuelve una secuencia válida |
| `solving` | `failed` | El solver informa un error o el cubo es irresoluble |
| `created` | `completed` | El cubo ya estaba resuelto y el total es 0 |

---

### 3. Cube

**Purpose**: Guardar el estado inicial introducido por el jugador.

**Core fields**

| Field | Type | Required | Description |
|------|------|----------|-------------|
| `idCube` | string | Yes | Identificador único del cubo |
| `initialState` | object | Yes | Estado inicial completo del cubo |

**`initialState` structure**

| Field | Type | Required | Description |
|------|------|----------|-------------|
| `cubeId` | string | Yes | Identificador lógico del cubo o de la sesión |
| `status` | enum | Yes | `in-progress` o `solved` |
| `faces` | object | Yes | Seis caras del cubo (`u`, `d`, `f`, `b`, `l`, `r`) |

Cada cara contiene exactamente 9 stickers de color controlado.

**Validation rules**

- Deben existir las 6 caras.
- Cada cara debe contener exactamente 9 stickers.
- Deben existir exactamente 9 stickers por color permitido.
- La orientación de centros y la disposición de piezas deben describir un cubo físicamente resoluble.

**Relationships**

- Un `Cube` puede estar asociado a una única `Game` inicial en el MVP.
- Un `Cube` origina muchos `CubeStateStep`.

---

### 4. CubeStateStep

**Purpose**: Representar cada movimiento de la solución y el estado del cubo tras aplicarlo.

**Core fields**

| Field | Type | Required | Description |
|------|------|----------|-------------|
| `idCube` | string | Yes | Referencia al cubo de la partida |
| `idGame` | string | Yes | Referencia a la partida dueña del historial |
| `movement` | integer | Yes | Ordinal del paso dentro de la solución |
| `notation` | string | Yes | Movimiento en notación estándar (`R`, `U'`, `F2`, etc.) |
| `cubeState` | object | Yes | Estado del cubo después de aplicar el movimiento |

**Validation rules**

- `movement` debe comenzar en 1 y avanzar de uno en uno.
- `notation` debe pertenecer al conjunto permitido por el solver.
- `cubeState` debe conservar el mismo esquema que `initialState`.

**Relationships**

- Muchos `CubeStateStep` pertenecen a una `Game`.
- Muchos `CubeStateStep` pertenecen a un `Cube`.

---

## Derived Views

### Game Summary

Vista derivada devuelta a la UI al finalizar o consultar una partida:

| Field | Source |
|------|--------|
| `idGame` | `Game.idGame` |
| `userId` | `Game.userId` |
| `status` | `Game.status` |
| `score` | `Game.score` |
| `currentStep` | `Game.currentStep` |
| `isSolved` | `score === 0` o `status === completed` |

### Validation Result

Objeto derivado usado por frontend y backend antes de resolver:

| Field | Type | Description |
|------|------|-------------|
| `valid` | boolean | Indica si el cubo puede resolverse |
| `code` | string | Código de error (`MISSING_STICKER`, `COLOR_COUNT`, `UNSOLVABLE_STATE`, etc.) |
| `message` | string | Mensaje orientado a la corrección |
| `locations` | array | Casillas afectadas cuando sea posible |

## Relationship Summary

```text
User 1 --- * Game 1 --- 1 Cube
                    \
                     \--- * CubeStateStep
Cube 1 --- * CubeStateStep
```
