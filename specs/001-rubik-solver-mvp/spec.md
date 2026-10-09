# Feature Specification: Resolución inicial del cubo de Rubik

**Feature Branch**: `[001-rubik-solver-mvp]`

**Created**: 2026-10-09

**Status**: Implementada

**Input**: User description: "Crear desde cero «Resolución Cubo de Rubik», una aplicación para registrar al jugador, capturar el estado inicial de un cubo de Rubik y mostrar la solución paso a paso guardando todos los movimientos y el total realizado."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Registrar o reutilizar jugador (Priority: P1)

Como persona que quiere resolver su cubo, quiero identificarme con un nombre de usuario y mi nombre completo para comenzar una sesión sin crear cuentas duplicadas.

**Why this priority**: Sin un jugador identificado no se puede asociar la partida ni su resultado a una persona concreta.

**Independent Test**: Puede probarse registrando un nombre de usuario nuevo y luego repitiendo el registro con el mismo nombre de usuario y un nombre completo distinto; en ambos casos la sesión queda lista para iniciar partida.

**Acceptance Scenarios**:

1. **Given** que una persona introduce un nombre de usuario que no existe y un nombre completo válido, **When** envía el formulario de sesión, **Then** el sistema crea el jugador y deja preparada una nueva partida para ese jugador.
2. **Given** que una persona introduce un nombre de usuario ya existente con un nombre completo actualizado, **When** envía el formulario de sesión, **Then** el sistema reutiliza el mismo jugador, actualiza su nombre completo y mantiene disponible su historial asociado.

---

### User Story 2 - Definir el estado inicial del cubo (Priority: P1)

Como jugador, quiero indicar el color de cada casilla del cubo para representar fielmente mi cubo físico antes de pedir la solución.

**Why this priority**: La calidad de la solución depende por completo de que el estado inicial del cubo quede capturado de forma correcta y verificable.

**Independent Test**: Puede probarse completando todas las casillas del cubo, comprobando que el sistema detecta configuraciones incompletas o inválidas y habilita el inicio solo cuando el estado es válido.

**Acceptance Scenarios**:

1. **Given** que el jugador ha completado todas las casillas con una distribución válida, **When** revisa el cubo antes de empezar, **Then** el sistema confirma que el estado está listo para resolverse.
2. **Given** que falta alguna casilla o la distribución de colores no es válida, **When** el jugador intenta empezar, **Then** el sistema bloquea el inicio y muestra qué debe corregirse.

---

### User Story 3 - Resolver y reproducir la solución paso a paso (Priority: P2)

Como jugador, quiero iniciar la resolución y revisar cada movimiento en orden para entender cómo pasar del estado inicial al cubo resuelto.

**Why this priority**: Esta es la propuesta de valor principal del producto: convertir un estado inicial en instrucciones claras y reutilizables para resolver el cubo.

**Independent Test**: Puede probarse iniciando una partida con un cubo válido y verificando que se genera una secuencia ordenada de movimientos, que puede recorrerse paso a paso y que al final se informa el total de movimientos.

**Acceptance Scenarios**:

1. **Given** que el jugador tiene una sesión activa y un cubo válido, **When** pulsa el botón para empezar, **Then** el sistema crea la partida, genera la solución y muestra el primer paso disponible.
2. **Given** que la solución ya fue generada, **When** el jugador avanza o retrocede por los pasos, **Then** el sistema actualiza el paso actual y el estado del cubo asociado a ese movimiento.
3. **Given** que el jugador llega al final de la solución, **When** la resolución termina, **Then** el sistema muestra el número total de movimientos realizados y conserva el detalle completo de la partida.

### Edge Cases

- ¿Qué ocurre si el jugador intenta iniciar una partida sin haber completado primero su identificación?
- ¿Cómo responde el sistema cuando el cubo ya está resuelto y no requiere movimientos?
- ¿Qué sucede si el estado introducido no corresponde a un cubo físicamente resoluble?
- ¿Cómo se comporta la reproducción cuando el jugador intenta avanzar más allá del último paso o retroceder antes del primero?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST permitir que una persona inicie una sesión de juego proporcionando un nombre de usuario y un nombre completo.
- **FR-002**: El sistema MUST reutilizar el jugador existente cuando se registre un nombre de usuario ya conocido.
- **FR-003**: El sistema MUST actualizar el nombre completo asociado a un nombre de usuario existente cuando el jugador envíe un valor distinto.
- **FR-004**: El sistema MUST crear un nuevo jugador cuando el nombre de usuario enviado no exista todavía.
- **FR-005**: El sistema MUST permitir indicar el color de cada casilla de un cubo estándar antes de iniciar la resolución.
- **FR-006**: El sistema MUST validar que el estado del cubo esté completo y sea coherente antes de permitir el inicio de una partida.
- **FR-007**: El sistema MUST bloquear el inicio de la resolución cuando falte la sesión del jugador o el cubo no sea válido, indicando la causa concreta del bloqueo.
- **FR-008**: El sistema MUST crear una partida nueva asociada al jugador y al estado inicial del cubo cuando el jugador solicite empezar.
- **FR-009**: El sistema MUST generar una secuencia ordenada de movimientos que lleve el cubo desde el estado inicial registrado hasta un estado resuelto, o informar explícitamente cuando no exista una solución válida para el estado recibido.
- **FR-010**: El sistema MUST guardar el estado inicial del cubo, cada movimiento en su orden correspondiente y el estado resultante tras cada movimiento para que la resolución completa quede registrada.
- **FR-011**: El sistema MUST mostrar la solución paso a paso, destacando en todo momento cuál es el movimiento actual y el estado del cubo asociado.
- **FR-012**: El sistema MUST permitir al jugador avanzar y retroceder por la solución sin perder la referencia del paso actual.
- **FR-013**: El sistema MUST permitir reproducir la solución de forma continua y pausarla para continuar revisándola manualmente.
- **FR-014**: El sistema MUST mostrar al finalizar la resolución un resumen con el número total de movimientos necesarios para resolver el cubo.
- **FR-015**: El sistema MUST informar un resultado de cero movimientos cuando el cubo introducido ya esté resuelto.

### Key Entities *(include if feature involves data)*

- **Jugador**: Persona identificada por un nombre de usuario único y un nombre completo, a la que se asocian partidas y resultados.
- **Partida**: Registro de una resolución solicitada por un jugador, incluyendo cuándo se inicia, qué cubo se intentó resolver y cuántos movimientos requirió.
- **Cubo**: Representación del estado inicial del cubo que el jugador desea resolver, compuesta por sus caras y casillas coloreadas.
- **Paso de solución**: Movimiento individual dentro de una partida, con su posición en la secuencia y el estado del cubo resultante tras aplicarlo.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 95% de los jugadores puede iniciar o reutilizar su sesión en menos de 30 segundos desde que abre el formulario.
- **SC-002**: El 100% de los intentos de inicio con un cubo incompleto o inválido queda bloqueado con un mensaje que identifica el problema antes de comenzar la resolución.
- **SC-003**: El 95% de las resoluciones exitosas muestra el primer paso de solución en menos de 5 segundos desde que el jugador pulsa empezar.
- **SC-004**: El 100% de las partidas resueltas muestra al finalizar el total de movimientos y conserva la secuencia completa de pasos para su revisión inmediata.
- **SC-005**: Al menos el 90% de los jugadores de prueba puede seguir la solución y localizar el paso actual sin ayuda externa en su primer intento.

## Assumptions

- La primera versión cubre únicamente un cubo estándar de 3x3.
- La identificación por nombre de usuario y nombre completo es suficiente para esta etapa inicial y no incluye autenticación ni autorización adicional.
- El estado inicial del cubo será introducido manualmente por el jugador dentro de la aplicación.
- Cada nueva solicitud de resolución genera una partida independiente, incluso cuando el jugador reutiliza un nombre de usuario existente.
- Quedan fuera de alcance en esta fase funciones adicionales como rankings, autenticación avanzada o modos de juego alternativos.
