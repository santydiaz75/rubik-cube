# Implementation Plan: Resolución inicial del cubo de Rubik

**Branch**: `[001-rubik-solver-mvp]` | **Date**: 2026-10-09 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-rubik-solver-mvp/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

Construir la primera versión de una aplicación web full-stack para registrar o reutilizar jugadores por `username`, capturar manualmente el estado inicial de un cubo de Rubik 3x3, validar ese estado en tiempo real, solicitar su resolución al backend y reproducir la solución paso a paso guardando tanto los movimientos como los estados intermedios y el total final de movimientos.

## Technical Context

**Language/Version**: Frontend con TypeScript 5.x sobre Vue 3; backend con Python 3.14 sobre FastAPI

**Primary Dependencies**: Vue 3, Vite, Vuetify 3, Pinia, Vue Router, Axios, SCSS; FastAPI, Pydantic, repositorios MongoDB asíncronos, adaptador de solver 3x3

**Storage**: MongoDB para usuarios, partidas, cubos y pasos de solución

**Testing**: Vitest + Vue Test Utils + Playwright en frontend; pytest + httpx/ASGI tests + pruebas de integración con MongoDB en backend

**Target Platform**: Navegadores de escritorio modernos para la SPA y servicio HTTP backend desplegable en entorno Linux/contenerizado

**Project Type**: Aplicación web full-stack (SPA + API REST)

**Performance Goals**: Validación visual inmediata tras cada cambio del cubo; primer paso de solución disponible en menos de 5 segundos en el 95% de las resoluciones exitosas; navegación de pasos fluida sin saltos perceptibles

**Constraints**: Mantener una única pantalla principal sin scroll; respetar Clean Architecture entre web, API, dominio e infraestructura; usar Composition API con `<script setup lang="ts">`; persistir todos los movimientos y estados; no introducir autenticación ni autorización en el MVP

**Scale/Scope**: MVP con un flujo principal de registro → edición del cubo → resolución → reproducción; 4 entidades persistidas principales; 5 endpoints iniciales; soporte para cubo estándar 3x3

## Constitution Check

### Gate Review Before Phase 0

- **Stack obligatorio**: PASS — el plan usa Vue 3 + TypeScript + Vite + Vuetify + Pinia + Axios en frontend y Python + FastAPI + MongoDB en backend.
- **Separación arquitectónica**: PASS — se propone una estructura explícita para web, API, dominio e infraestructura, evitando mezclar UI con acceso HTTP o persistencia.
- **Modelo de dominio obligatorio**: PASS — el diseño conserva `user`, `games`, `cubes` y `cubeStates`, además de mapearlos a entidades y value objects operativos.
- **Criterios UX/UI del proyecto**: PASS — la solución prioriza una SPA de una sola pantalla, edición manual del cubo en red 2D, validación en tiempo real y reproductor paso a paso.
- **Fuera de alcance**: PASS — no se añade autenticación/autorización ni capacidades no pedidas para la v1.

### Gate Review After Phase 1

- **Arquitectura de frontend**: PASS — los componentes quedan divididos por responsabilidad y los stores/composables separan orquestación de presentación.
- **Arquitectura de backend**: PASS — las reglas del cubo, los casos de uso y la persistencia quedan desacoplados.
- **Persistencia y trazabilidad**: PASS — el modelo y el contrato almacenan el estado inicial, cada movimiento y cada estado resultante.
- **Sin violaciones justificables**: PASS — no se requieren excepciones a la constitución en esta fase.

## Project Structure

### Documentation (this feature)

```text
specs/001-rubik-solver-mvp/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── http-api.yaml
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── main.py
│   ├── application/
│   │   ├── dto/
│   │   ├── ports/
│   │   └── use_cases/
│   ├── domain/
│   │   ├── cube/
│   │   ├── game/
│   │   └── user/
│   └── infrastructure/
│       ├── persistence/
│       └── solver/
└── tests/
    ├── contract/
    ├── integration/
    └── unit/

frontend/
├── src/
│   ├── app/
│   │   ├── router/
│   │   ├── providers/
│   │   └── vuetify/
│   ├── application/
│   │   ├── ports/
│   │   └── use_cases/
│   ├── domain/
│   │   ├── cube/
│   │   ├── solution/
│   │   └── user/
│   ├── features/
│   │   ├── player-session/
│   │   │   ├── components/
│   │   │   └── composables/
│   │   ├── cube-editor/
│   │   │   ├── components/
│   │   │   └── composables/
│   │   └── solution-player/
│   │       ├── components/
│   │       └── composables/
│   ├── infrastructure/
│   │   ├── http/
│   │   └── mappers/
│   ├── stores/
│   └── styles/
└── tests/
    ├── component/
    ├── e2e/
    └── unit/
```

**Structure Decision**: Se adopta una estructura de aplicación web con `frontend/` y `backend/` separados para reflejar los límites del sistema desde el inicio. Dentro de cada capa se aplica Clean Architecture; en frontend se combina con un layout por feature para mantener componentes, composables y estado próximos al flujo funcional sin mezclar dominio e infraestructura.

## Complexity Tracking

No se detectan violaciones de la constitución que requieran justificación en esta fase.
