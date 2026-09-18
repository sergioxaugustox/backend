# AGENTS.md — Bitácora del proyecto (contexto para el agente)

> Este archivo se carga automáticamente en cada sesión del agente. Es la bitácora viva del proyecto: actualizarla al cerrar cada bloque de trabajo. Versión canónica del plan en `Downloads/plan_backend_api_fase3.md`.

## Proyecto

API REST de cálculo de costos de construcción (APU) — Python + FastAPI + SQLAlchemy + PostgreSQL (Supabase), deploy en Render.

- **Meta del autor:** ser contratable para puesto entry de backend/API. Ritmo 10 h/semana. Regla de oro: no avanzar de fase sin evidencia en GitHub.
- **URL pública:** https://backend-7p18.onrender.com (docs: /docs). Plan gratuito: la primera carga tarda ~1 min (arranque en frío).
- **Repo:** https://github.com/sergioxaugustox/backend

## DÓNDE ME QUEDÉ

**Fase 3. APU vivo en internet, auth completo. PASO 7: pool_pre_ping + manejador de errores + README HECHOS. Falta: SECRET_KEY en Render, RLS. Luego el SEGUNDO PROYECTO (motor de reservas).**

Fases 0-2 COMPLETAS. Fase 3 pasos 1-6 COMPLETOS. Paso 7 (pulido) en curso.

**Método:** construir a mano (libreta primero), recall activo, Leitner. Repaso espaciado al inicio. Traceback: leer ambas puntas.

## Estado — Checklist Fase 3

- [x] Motor completo + deploy (pasos 1-5 + C).
- [x] PASO 6 — Auth JWT completo y probado (401 sin token, 200 GET, 201 con token).
- [~] PASO 7 — Pulido + README. EN CURSO:
  - [x] pool_pre_ping=True + pool_recycle=300 en el engine.
  - [x] Manejador global de errores (500 genérico, sin Traceback al cliente).
  - [x] Borrados usuarios de prueba de Supabase.
  - [x] README: molde SOURCE/SYSTEM/ENGINEERING/ROLE + endpoints + diagrama ER (Mermaid) + URL viva + notas.
  - [ ] SECRET_KEY en el panel de Render (sin ella, el login falla en producción). 5 min.
  - [ ] Activar RLS en Supabase (tablas UNRESTRICTED).
- [ ] SEGUNDO PROYECTO (motor de reservas) — Fase 3 pide 2 proyectos con README.

## Arquitectura y convenciones del repo

- `main.py`: todos los endpoints. `def` síncrono a propósito (async es tema futuro).
- `database.py`: engine (`pool_pre_ping=True, pool_recycle=300`) + 6 modelos + `Base.metadata.create_all`.
- Escritura protegida con `Depends(get_usuario_actual)`; lectura pública. Login con form-data (OAuth2 lo exige), token Bearer JWT.
- Manejador global `@app.exception_handler(Exception)` → 500 genérico. NO reemplaza guards 404/401; atrapa lo imprevisto (DRY).
- Esquema: insumos, conceptos, composicion (receta puente), precios (histórico con fecha_vigencia), tareas (CRUD práctica Fase 1), usuarios.
- Cálculo `/conceptos/{id}/costo?fecha=`: precio vigente más reciente `<= fecha` por insumo.
- Commits en español, estilo "Fase X: descripción".
- Código y comentarios en español.
- `.env` NUNCA se commitea (verificar con `git status`). Secretos solo en panel de Render.
- Versiones fijas en requirements.txt: `bcrypt==4.3.0` (la 5.0.0 rompe passlib).

## BUGS/PATRONES CONFIRMADOS

- DEFINIR ANTES DE USAR. Cambio a medias (firma vs cuerpo) → NameError.
- bcrypt 5.0.0 → bcrypt==4.3.0. "server closed connection" → pool_pre_ping.
- Argumento DENTRO del string de la ruta (`@app.put("/tareas/{id}, response_model=...")`) → ruta literal registrada, PUT da 404. Argumentos del decorador van FUERA del string. Después de tocar un decorador, verificar la ruta en /docs.
- NameError = no existe al usar. UnboundLocalError = no creada/mal indentada. 422 = formato. 401 = no autorizado. 500 = error interno. SyntaxError rompe archivo.
- Capturas cortan @app/def del borde → verificar corriendo.

## Secuencia de proyectos

1. **APU** (este repo) — calculador de costos con precios históricos. Dominio real: precios Cruz Azul 2024.
2. **Motor de reservas** — proyecto de MODELADO DE DATOS: la regla que rechaza traslapes vive en el diseño del esquema (rangos de fecha + constraint), no en ifs sueltos.
3. #3 según vacante.

Los proyectos son la evidencia: portafolio sólido en GitHub > lista de cursos.

## PENDIENTES (paso 7)

- SECRET_KEY en panel de Render.
- Activar RLS en Supabase.
- Precios 2026 para demo histórico + caso límite `<=`. Etiquetar ejemplo.
- Mano de obra no cargada. v1 con 3 insumos.
- pytest sobre APU DESPUÉS de cerrar APU ("código que corre ≠ código correcto"; probar aprueba/rechaza/límite/combinado). async también es tema futuro.

**Datos Cruz Azul (2024):** block hueco $15.22, macizo $16.80, arena $6.30, cal $68.25/bulto. RENDIMIENTOS = ejemplo, no verificados (ya etiquetado en README).

## Método de aprendizaje del autor

1h lectura = 1h código sin copiar. Leitner libreta cerrada. Repaso espaciado al inicio (Anki primeros 10 min). Mañana perdida = saltada. Traceback ambas puntas. Ctrl+S antes de probar. Cerrar en bloque con evidencia. Temas densos con cabeza fresca. NUNCA secretos en capturas. Sueño > una sesión suelta.

## Fuentes (gratuitas)

FastAPI: https://fastapi.tiangolo.com/tutorial/ · Auth/JWT: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ · SQL: https://sqlbolt.com · Diagramas: https://dbdiagram.io · Deploy: https://render.com
