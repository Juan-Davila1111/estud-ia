**Arquitectura**

- **FastAPI**: servidor ASGI que expone REST endpoints.
- **SQLAlchemy (async)**: ORM para persistencia.
- **MySQL (Docker)**: base de datos relacional expuesta en el puerto 3306.

Diagrama (Mermaid):

```mermaid
graph LR
  Client -->|HTTP| FastAPI[FastAPI (uvicorn)]
  FastAPI -->|async DB| MySQL[(MySQL container:3306)]
```

Descripción breve:
- La app arranca y ejecuta `init_db()` para crear tablas si hace falta.
- Las conexiones a la DB usan `asyncmy` mediante SQLAlchemy async engine.
