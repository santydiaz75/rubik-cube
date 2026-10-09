# Resolución Cubo de Rubik

Aplicación web para registrar o reutilizar un jugador, introducir el estado de un cubo Rubik 3x3, obtener una solución y reproducir sus movimientos paso a paso. Las partidas, los cubos y sus estados intermedios se guardan en MongoDB.

## Funcionalidades

- Registro o actualización idempotente de jugadores por `username`.
- Editor visual del cubo en una red 2D, con paleta de seis colores.
- Validación inmediata del conteo de stickers y bloqueo de cubos inválidos.
- Resolución de cubos 3x3 mediante el solver Kociemba.
- Reproductor con navegación, reproducción y control de velocidad.
- Persistencia de partidas y estados de cada movimiento en MongoDB.

## Tecnologías

- **Frontend:** Vue 3, TypeScript, Vite, Vuetify, Pinia, Vue Router y Axios.
- **Backend:** Python, FastAPI, Pydantic y PyMongo.
- **Persistencia:** MongoDB.

## Requisitos

- Node.js 22 o superior y npm.
- Python 3.14 o superior.
- MongoDB accesible desde el backend (local o remoto).

## Configuración

### Frontend

Desde la raíz del repositorio, crea el archivo de entorno local y configura la URL de la API:

```powershell
Copy-Item frontend\.env.example frontend\.env
```

El valor predeterminado de `VITE_API_BASE_URL` es `http://localhost:8000`.

### Backend

Crea `backend\.env` con la URI de MongoDB y el nombre de la base de datos:

```dotenv
MONGO_URI=mongodb://localhost:27017
MONGO_DATABASE=rubik_solver
```

Para una instancia con autenticación, proporciona una URI apropiada, por ejemplo:

```dotenv
MONGO_URI=mongodb://<usuario>:<contraseña>@localhost:27017/?authSource=admin
MONGO_DATABASE=rubik_solver
```

No compartas ni confirmes archivos `.env` con credenciales. El backend lee este archivo cuando se inicia con el parámetro `--env-file`.

## Instalación y ejecución

Abre dos terminales desde la raíz del repositorio.

### Terminal 1: API

```powershell
python -m pip install -r backend\requirements.txt
python -m uvicorn backend.src.api.main:app --env-file backend\.env --reload
```

La API queda disponible en `http://localhost:8000`. La documentación interactiva está en `http://localhost:8000/docs`.

### Terminal 2: aplicación web

```powershell
npm --prefix frontend install
npm --prefix frontend run dev
```

Abre la URL que indique Vite, normalmente `http://localhost:5173`.

## Uso

1. Registra un jugador con su `username` y nombre completo.
2. Selecciona un color de la paleta y pinta las casillas en la red del cubo para reproducir el estado físico.
3. Confirma que el conteo muestre nueve stickers de cada color.
4. Pulsa **Empezar** para crear la partida y solicitar la solución.
5. Usa los controles del reproductor para recorrer los movimientos y sus estados.

Un cubo ya resuelto genera una partida de cero movimientos. El botón de resolución se deshabilita cuando los conteos de colores no son válidos.

### Cómo orientar las caras al introducir los colores

Cada cara se copia **mirándola directamente desde fuera**, respetando la orientación del desplegado. Tener nueve casillas de cada color no garantiza que el estado sea físicamente resoluble: copiar una cara girada o reflejada puede provocar el error `The provided cube state is not physically solvable`.

#### Posición de referencia

Sujeta el cubo con una cara delante (**F**) y otra arriba (**U**). Los centros identifican las caras y no cambian al mezclar el cubo.

Por ejemplo, puedes colocar el centro blanco arriba y el centro verde delante. Los demás centros determinan las caras derecha, izquierda, trasera e inferior; no debes asumir sus colores, sino copiar los de tu cubo.

La aplicación muestra este desplegado:

```text
        U
    L   F   R   B
        D
```

#### Orientación de cada cara

La última columna indica qué cara está junto al **borde superior** de la cuadrícula que estás copiando:

| Cara | Cómo mirarla | Borde superior junto a |
|---|---|---|
| **F** — delante | Mira el frente directamente | **U** |
| **R** — derecha | Mira el lateral derecho manteniendo arriba lo que estaba arriba | **U** |
| **B** — atrás | Mira desde detrás manteniendo arriba lo que estaba arriba | **U** |
| **L** — izquierda | Mira el lateral izquierdo manteniendo arriba lo que estaba arriba | **U** |
| **U** — arriba | Mira desde arriba | **B** |
| **D** — abajo | Mira desde abajo | **F** |

Gira el cubo entero para verlo, **sin girar sus capas**. Para copiar los laterales, puedes girarlo alrededor del eje vertical manteniendo siempre U arriba.

#### Orden de las casillas

Copia cada cara de izquierda a derecha y de arriba abajo:

```text
1  2  3
4  5  6
7  8  9
```

La casilla **5** es el centro. Presta especial atención a **U** y **D**: en U, el borde que toca F queda abajo; en D, el borde que toca F queda arriba. No reflejes las caras como si las miraras desde dentro del cubo.

Si aparece el error de estado no resoluble, revisa primero los colores y la orientación de las seis caras. Un cubo desmontado y montado incorrectamente también puede tener un estado imposible aunque conserve nueve casillas de cada color.

## API

| Método | Ruta | Descripción |
|---|---|---|
| `PUT` | `/users/{username}` | Crear o actualizar un jugador |
| `POST` | `/games/` | Crear una partida y resolver el cubo |
| `GET` | `/games/{game_id}` | Consultar una partida |
| `GET` | `/games/{game_id}/steps` | Consultar los estados de solución |
| `GET` | `/games/{game_id}/steps/{movement}` | Consultar un movimiento concreto |

## Pruebas y build

### Backend

Instala las dependencias de desarrollo y ejecuta las pruebas:

```powershell
python -m pip install -r backend\requirements-dev.txt
python -m pytest backend\tests
```

Las pruebas unitarias, de contrato e integración usan dobles de prueba cuando no requieren una instancia MongoDB.

### Frontend

```powershell
npm --prefix frontend run test
npm --prefix frontend run build
```

El frontend no tiene actualmente una suite automatizada de navegador. Los escenarios manuales de registro, validación, resolución y reproducción están descritos en [quickstart.md](specs/001-rubik-solver-mvp/quickstart.md).

## Estructura del repositorio

```text
backend/   API FastAPI, dominio, casos de uso, persistencia y pruebas
frontend/  SPA Vue, features, stores y pruebas
specs/     Especificación, plan, tareas y guía de validación
```
