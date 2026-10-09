# Quickstart: Resolución inicial del cubo de Rubik

## Purpose

Validar de extremo a extremo que el MVP permite registrar/reutilizar jugadores, capturar un cubo 3x3 válido, resolverlo y reproducir la solución con persistencia del historial.

## Related Artifacts

- [spec.md](./spec.md)
- [plan.md](./plan.md)
- [research.md](./research.md)
- [data-model.md](./data-model.md)
- [http-api.yaml](./contracts/http-api.yaml)

## Prerequisites

- Node.js 22+ y `npm`
- Python 3.14+
- MongoDB disponible localmente
- Variables de entorno configuradas para backend y frontend según la implementación

## Initial Setup

### Backend

1. Crear o activar el entorno virtual de Python.
2. Instalar dependencias del backend:

   ```powershell
   python -m pip install -r backend/requirements.txt
   ```

3. Configurar la cadena de conexión de MongoDB.

### Frontend

1. Instalar dependencias del frontend:

   ```powershell
   npm --prefix frontend install
   ```

2. Configurar la URL base del API para desarrollo local.

## Run the Application

### Start backend

```powershell
python -m uvicorn backend.src.api.main:app --reload
```

**Expected outcome**:

- El servicio HTTP queda escuchando localmente.
- El contrato de [http-api.yaml](./contracts/http-api.yaml) puede atender peticiones de usuario y partidas.

### Start frontend

```powershell
npm --prefix frontend run dev
```

**Expected outcome**:

- Se abre la SPA principal.
- La vista inicial muestra el formulario de jugador, el editor del cubo y el área de solución en una sola pantalla.

## Validation Scenarios

### Scenario 1: Crear un jugador nuevo

1. Introducir un `username` nuevo y un `fullname`.
2. Enviar el formulario.

**Expected outcome**:

- Se crea el jugador.
- La interfaz indica que la sesión está activa y lista para preparar el cubo.

### Scenario 2: Reutilizar jugador existente

1. Repetir el formulario con el mismo `username` y un `fullname` distinto.
2. Enviar nuevamente.

**Expected outcome**:

- No se crea un duplicado.
- El nombre completo visible se actualiza.

### Scenario 3: Bloquear cubo incompleto o inválido

1. Dejar al menos una casilla sin color o desequilibrar el conteo de colores.
2. Intentar empezar la resolución.

**Expected outcome**:

- El botón de resolver permanece deshabilitado o la acción es bloqueada.
- Se muestra un mensaje con el error específico y, si aplica, la casilla/cara afectada.

### Scenario 4: Resolver un cubo ya resuelto

1. Pintar las seis caras con el patrón resuelto.
2. Lanzar la resolución.

**Expected outcome**:

- La partida se completa sin pasos intermedios.
- El resumen final informa `0` movimientos.

### Scenario 5: Resolver un cubo válido y reproducir pasos

1. Registrar o reutilizar un jugador.
2. Introducir un cubo válido no resuelto.
3. Pulsar el botón de empezar.

**Expected outcome**:

- Se crea una partida.
- La UI muestra la secuencia ordenada de movimientos.
- El paso actual queda resaltado.
- Los botones siguiente/anterior/play/pausa funcionan dentro de sus límites.
- Al final se muestra el número total de movimientos.

## Test Commands

### Backend tests

```powershell
python -m pytest backend/tests
```

**Expected outcome**:

- Pasan las pruebas unitarias, de contrato e integración del backend.

### Frontend unit/component tests

```powershell
npm --prefix frontend run test
```

**Expected outcome**:

- Pasan pruebas de stores, componentes del editor, registro y reproductor.

### Frontend end-to-end tests

Todavía no hay una suite automatizada de Playwright/Cypress en el repositorio.
La validación end-to-end pendiente para este MVP sigue siendo manual y requiere backend + MongoDB levantados localmente.

## Validation Notes

- La semántica de datos persistidos debe alinearse con [data-model.md](./data-model.md).
- Cualquier cambio de forma en requests/responses debe mantenerse compatible con [http-api.yaml](./contracts/http-api.yaml).
- Si el solver devuelve error por estado irresoluble, la UI debe conservar el contexto y exponer un mensaje recuperable al usuario.

## Evidencia de validación

- `python -m pip install -r backend/requirements-dev.txt` ✅
- `python -m pytest backend/tests` ✅ (12 pruebas superadas, incluidas seis pruebas de regresión para verificar que la solución generada devuelve a estado resuelto los giros U, D, L, R, F y B)
- `python -c "from backend.src.api.main import app; print(app.title)"` ✅ (`Rubik Solver API`)
- `npm --prefix frontend install` ✅
- `npm --prefix frontend run test` ✅ (3 pruebas superadas)
- `npm --prefix frontend run build` ✅
- MongoDB autenticado: conexión `ping` correcta; URI omitida intencionalmente de esta evidencia.
- Registro y reutilización de jugador desde la SPA ✅; se actualizó el mismo usuario sin duplicarlo.
- Cubo inválido desde la SPA ✅; con 8 stickers blancos y 10 rojos, se mostró el error y el botón **Empezar** quedó deshabilitado.
- Cubo resuelto desde la SPA ✅; partida completada con 0 movimientos.
- Cubo alcanzable generado con los giros `R U` desde la SPA ✅; solución `U' R'`, 2 pasos ordenados, navegación siguiente/anterior funcional.
- Persistencia MongoDB/API ✅; usuario actualizado, partidas completadas y 2 estados intermedios persistidos; `GET /games/{gameId}/steps` y `GET /games/{gameId}/steps/1` devolvieron los pasos guardados. El estado final almacenado quedó resuelto.
- Validación manual E2E de los escenarios 1–5: ✅ completada el 2026-10-09.
