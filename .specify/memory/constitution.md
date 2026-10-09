# Constitucion del Proyecto 
> Este archivo define las reglas inmutables del proyecto. Ninguna spec, plan ni task puede contradecirlo. Ante cualquier duda o conflicto, este documento es la fuente de verdad superior.

---

## 1. Descripcion del proyecto1
Aplicacion web de **Pasos para resolver cubo de Rubik** construida utilizando el Spec-Driven Development. Permite indicar el estado original del cunode Rubik y como salida tendra los movimientos efectuar por el usuario paar resolverlo explicando en cada caso el porqué de cada movimiento.

## 2. Stack tecnologico

- **Lenguajes permitidos para el Frontend:** La aplicación es una aplicación de página única (SPA) de Vue 3 que utiliza TypeScript, Vite, Vuetify 3, Pinia, Vue Router, Axios y SCSS. Vite es el servidor de desarrollo y empaquetador (build); no se debe introducir Webpack para los nuevos desarrollos.
La nueva interfaz de usuario debe seguir las reglas de Prioridad A de la guía de estilos de Vue, lo que incluye nombres de componentes válidos, elementos v-for con clave (key) y un uso controlado de las props. Se debe seguir la guía de Prioridad B cuando mejore la legibilidad, incluyendo plantillas (templates) simples, nombres de componentes estables y definiciones claras de las props.

- **Lenguajes permitidos para el Backend:** Python para el Backend con Fast Api.
- **Persistencia:** MongoDB.
- **Prohibido:** Quedan prohibidos los Mixins, la manipulación directa del DOM, la mutación directa de props y los nuevos componentes con la Options API, a menos que un plan de migración o la integración de un tercero lo justifiquen explícitamente.
- **Uso gestor de paquetes:** Usar npm. El proyecto tiene `package.json`.

## 3. Estructura de archivos

Usar Clean Architecture separando claramente la web (Vue), la Api (Python y Fast Api), el dominio (Python), la infrestructura (MongoDb peristencia)

## 5. Persistencia y datos

MongoDB

## 6. Entidades de dominio

El sistema tiene tres entidades. Las specs deben respetar estos modelos.

**user:** `userId`, 'username', `fullname`, `score`

**games:** `idGame`, `userId`, 'idCube', `createdAt`, 'score'

**cubes:** `idCube`, `initialState`

**cubeStates:** `idCube`, 'movement', `cubeState`


- El score es el numero de movimientos necesarios para resolver el cubo de Rubik

- movement es un ordinal que se incrememnta con cada movimiento

- initialState y cubeState son un json que mantiene el estado del cubo de la siguiente manera:

cubo resuelto
{
  "cubeId": "rubik-3x3-standard",
  "status": "solved",
  "faces": {
    "u": ["white", "white", "white", "white", "white", "white", "white", "white", "white"],
    "d": ["yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow"],
    "f": ["green", "green", "green", "green", "green", "green", "green", "green", "green"],
    "b": ["blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue"],
    "l": ["orange", "orange", "orange", "orange", "orange", "orange", "orange", "orange", "orange"],
    "r": ["red", "red", "red", "red", "red", "red", "red", "red", "red"]
  }
} 

cubo sin resolver
{
  "cubeId": "user-match-78923",
  "status": "in progress",
  "faces": {
    "u": ["W", "W", "Y", "W", "W", "G", "O", "W", "W"],
    "d": ["Y", "Y", "W", "Y", "Y", "R", "B", "Y", "Y"],
    "f": ["G", "G", "R", "G", "G", "W", "Y", "G", "G"],
    "b": ["B", "B", "O", "B", "B", "Y", "W", "B", "B"],
    "l": ["O", "O", "B", "O", "O", "W", "R", "O", "O"],
    "r": ["R", "R", "G", "R", "R", "Y", "O", "R", "R"]
  }
}

---

## 7. Criterios de UI/UX


- Criterios de UX (Experiencia de Usuario)

• Carga Cognitiva Reducida (Single Screen Focus): Al ser una SPA, toda la acción principal (Cubo 3D/2D, controles de movimientos y panel de solución) debe ocurrir en una sola vista sin scroll. Los subapartados (historial, ajustes) deben ser paneles colapsables o diálogos de Vuetify (v-dialog).
• Interactividad Híbrida (Input del Estado): El usuario debe poder introducir el estado de su cubo físico de dos formas:
	• Visual/Manual: Haciendo clic en una paleta de colores y luego en el sticker del cubo desplegado (despliegue en cruz 2D).
• Feedback Inmediato de Validación: El sistema debe validar el cubo en tiempo real mediante Pinia antes de enviar la petición a Axios. Si hay un número incorrecto de stickers de un color (ej. 10 blancos en lugar de 9), se debe bloquear el botón "Resolver" y mostrar un v-alert indicando el error exacto.
• Accesibilidad en los Controles de Movimiento: Si la web permite girar las caras con botones, estos deben seguir la notación WCA (U, D, R, L, F, B). Se deben incluir tooltips (v-tooltip) que expliquen qué hace cada botón (ej. "Girar cara derecha en sentido horario") para usuarios principiantes.

- Criterios de UI (Diseño de Interfaz con Vuetify 3 y SCSS)

• Representación Visual del Cubo:
	• Vista 2D (Modo Editor): Una red en forma de cruz que represente el desarrollo plano del cubo. Es la forma más fácil para que el usuario pinte los colores en TypeScript de forma limpia.
• Paleta de Colores de Alto Contraste: Los colores del cubo de Rubik tradicional deben contrastar fuertemente entre sí y con el fondo (especialmente el Blanco vs. Amarillo y el Azul vs. Verde). Utiliza variables SCSS para mapear los colores oficiales y cumplir con las pautas WCAG de accesibilidad visual.
• Sección de Pasos de la Solución (Player Controls): La respuesta de Axios entregará una secuencia de movimientos. La UI debe mostrar un reproductor con botones de Play, Pausa, Avanzar paso, Retroceder paso y un control de velocidad (v-slider). El paso actual de la solución debe estar fuertemente resaltado en un timeline horizontal o vertical.

---

## 10. Organizacion de specs

- Cada feature/capacidad de negocio vive en su propia spec dentro de `.specify/specs/`.
- No se permite un spec monolítico.
- Orden de lectura obligatorio antes de cualquier cambio: `constitution.md` → `spec.md` → `plan.md` → `tasks.md`.
  
---

## 11. Fuera de alcance

Los siguientes temas están explícitamente excluidos de este proyecto:

- Autenticación y autorización
---
