---
name: 001-rubik-solver-mvp
description: "Planifica una nueva funcionalidad antes de tocar código"
agent: speckit.specify
---

## Rol

Actúa como un desarrollador frontend sénior. Escribe código simple, claro y fácil de entender para alguien que está empezando a programar. Ten en cuenta que el proyecto se llama «Resolución Cubo de Rubik».

## Contexto

Quiero crear desde cero «Resolución Cubo de Rubik», una aplicación web para visualizar los movimientos necesarios para resolver un cubo de Rubik a partir de su estado inicial. Esta es la primera versión y debe ser muy sencilla. La aplicación se desarrollará poco a poco; por ahora, solo necesito una base limpia que funcione correctamente desde el primer momento.

## Tarea

Crea la aplicación web con las siguientes funcionalidades:

1. Un formulario para registrar una sesión con estos datos:
   - `username`
   - `fullname`

## Restricciones y reglas

### Usuario

- Si el `username` ya existe, reutilízalo y actualiza el `fullname`.
- Si no existe, crea un usuario nuevo.

### Juego

- Muestra un cubo de Rubik cuyo estado inicial se pueda indicar seleccionando el color de cada casilla.
- Incluye un botón para empezar.
- Muestra la solución paso a paso una vez iniciado el juego.

## Formato de salida

1. Guarda en la persistencia de la aplicación todos los movimientos necesarios para resolver el cubo de Rubik.
2. Al terminar, responde con un resumen del número total de movimientos realizados para resolverlo.