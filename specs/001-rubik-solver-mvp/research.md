# Research: Resolución inicial del cubo de Rubik

## Decision 1: Arquitectura general full-stack con SPA + API

- **Decision**: Construir una SPA en Vue 3 con TypeScript para la experiencia de usuario y un servicio FastAPI separado para orquestar validación, resolución y persistencia.
- **Rationale**: La constitución exige explícitamente Vue 3 en frontend, FastAPI en backend y MongoDB como persistencia. Separar la SPA del API mantiene límites claros entre presentación y lógica de dominio.
- **Alternatives considered**:
  - Resolver todo en frontend: rechazado porque dificulta persistir partidas y mezcla la experiencia de usuario con la lógica de resolución.
  - Backend monolítico sirviendo HTML tradicional: rechazado porque contradice la decisión de SPA y empobrece la interacción visual del editor/reproductor.

## Decision 2: Clean Architecture desde el primer commit

- **Decision**: Estructurar backend y frontend con capas de dominio, aplicación e infraestructura, dejando FastAPI, Axios, Pinia y MongoDB en bordes externos.
- **Rationale**: El proyecto exige separar web, API, dominio e infraestructura. Además, esta división permite probar la lógica del cubo y los casos de uso sin depender de frameworks.
- **Alternatives considered**:
  - Componentes y rutas llamando directamente a MongoDB/Axios: rechazado por acoplar presentación y acceso a datos.
  - Un único store con toda la lógica: rechazado por concentrar demasiadas responsabilidades y dificultar pruebas unitarias.

## Decision 3: Solver ejecutado en backend mediante un puerto de dominio

- **Decision**: Ejecutar la resolución del cubo en el backend a través de un puerto `CubeSolver`, implementado por un adaptador de solver 3x3 probado, manteniendo la interfaz sin conocimiento del algoritmo concreto.
- **Rationale**: La persistencia de pasos, la detección de errores explícitos y la posible validación de estados físicamente imposibles encajan mejor en un servicio backend controlado.
- **Alternatives considered**:
  - Solver en el hilo principal del navegador: rechazado por riesgo de bloquear la UI.
  - Solver en Web Worker: viable, pero descartado para el MVP porque la constitución ya introduce un backend y la persistencia debe ocurrir allí.

## Decision 4: Representación canónica del cubo orientada a caras

- **Decision**: Modelar el cubo con seis caras (`u`, `d`, `f`, `b`, `l`, `r`), cada una con nueve stickers coloreados, preservando el formato esperado por la constitución y los contratos HTTP.
- **Rationale**: La red 2D del editor visual se mapea de forma directa a este formato, y la constitución ya documenta el JSON de `initialState` y `cubeState`.
- **Alternatives considered**:
  - Arreglo plano de 54 stickers: rechazado como representación pública por ser menos legible y más difícil de depurar.
  - Modelo de cubies como contrato principal: rechazado porque complica la entrada manual del usuario.

## Decision 5: Validación por capas con errores accionables

- **Decision**: Validar el cubo en cuatro niveles: completitud visual, distribución de colores, coherencia de centros/orientación y solvencia física antes de invocar el solver.
- **Rationale**: El usuario debe recibir feedback inmediato y específico antes de resolver; además, los estados físicamente imposibles no deben producir falsas esperanzas ni respuestas ambiguas.
- **Alternatives considered**:
  - Validar solo que existan 54 stickers: rechazado porque permite cubos inconsistentes.
  - Validar solo en backend: rechazado porque contradice el requisito de validación en tiempo real previo a la llamada HTTP.

## Decision 6: Upsert idempotente de jugador por `username`

- **Decision**: Exponer el registro de jugador como operación idempotente: crea un usuario cuando el `username` es nuevo y actualiza el `fullname` cuando ya existe.
- **Rationale**: Esta decisión implementa directamente el comportamiento funcional del MVP y evita duplicados.
- **Alternatives considered**:
  - Crear siempre un usuario nuevo: rechazado porque rompe FR-002/FR-003.
  - Tratar `fullname` como identificador: rechazado porque no es estable ni único.

## Decision 7: Persistencia separada de partidas y pasos de solución

- **Decision**: Guardar `users`, `games`, `cubes` y `solution_steps/cubeStates` en colecciones diferenciadas, con `games` conteniendo el resumen y `cubeStates` el historial ordenado de movimientos.
- **Rationale**: El historial paso a paso es una capacidad central y debe ser consultable de forma ordenada, eficiente y trazable.
- **Alternatives considered**:
  - Embutir todos los pasos dentro del documento `games`: aceptable en demos pequeñas, pero menos flexible para consultas, límites de documento y evolución futura.

## Decision 8: Frontend dividido por features y componentes pequeños

- **Decision**: Partir la UI en tres features principales: `player-session`, `cube-editor` y `solution-player`, cada una con componentes y composables dedicados.
- **Rationale**: Registro, edición/validación del cubo y reproducción de la solución tienen responsabilidades y límites de prueba distintos. Esta división sigue las mejores prácticas de Vue 3 con Composition API.
- **Alternatives considered**:
  - Una vista única con toda la lógica: rechazada por complejidad y baja mantenibilidad.
  - Hacer toda la lógica en componentes sin composables: rechazado por dificultar reutilización y limpieza del ciclo de vida.

## Decision 9: Stores Pinia enfocados por responsabilidad

- **Decision**: Utilizar stores independientes para jugador, editor del cubo, partida y reproducción de solución; cada store orquesta estado y delega reglas complejas al dominio o casos de uso.
- **Rationale**: El estado debe ser compartido entre formulario, editor, validación y reproductor, pero sin crear una fuente de verdad global inmanejable.
- **Alternatives considered**:
  - Estado local en componentes: rechazado porque complica sincronización entre secciones.
  - Un único mega-store: rechazado por mezclar fases del flujo y dificultar el mantenimiento.

## Decision 10: Contrato HTTP orientado a flujo y reproducción

- **Decision**: Definir endpoints para upsert de usuario, creación de partida con resolución, consulta de resumen de partida y recuperación de pasos ordenados.
- **Rationale**: El flujo funcional necesita crear/reutilizar jugador, resolver, mostrar resumen y navegar por pasos sin recalcular.
- **Alternatives considered**:
  - Un único endpoint que resuelva todo sin persistir detalles: rechazado porque no cubre la trazabilidad ni el reproductor paso a paso.

## Decision 11: Estrategia de pruebas multicapa

- **Decision**: Probar dominio, casos de uso, componentes, contratos API e integración end-to-end con escenarios reales del cubo.
- **Rationale**: La funcionalidad combina UI interactiva, reglas de dominio sensibles y persistencia histórica; un único nivel de pruebas no cubre los riesgos principales.
- **Alternatives considered**:
  - Solo pruebas manuales: rechazado por insuficiente para reglas de validación y reproducción.
  - Solo e2e: rechazado por alto coste y pobre localización de fallos.
