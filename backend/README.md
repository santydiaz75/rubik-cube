# Backend

API FastAPI para registrar jugadores, validar cubos 3x3, resolver partidas y persistir movimientos.

## Scripts útiles

```powershell
python -m pip install -r backend/requirements-dev.txt
python -m uvicorn backend.src.api.main:app --reload
python -m pytest backend/tests
```
