# CRUD Productos (FastAPI + MySQL)

Proyecto ejemplo con FastAPI, SQLAlchemy (async) y una base de datos MySQL levantada con Docker.

Requisitos
- Python 3.10+
- Docker

Instrucciones rápidas

1. Levantar la base de datos MySQL (sin contraseña, expuesto en el puerto 3306):

```bash
docker-compose up -d db
```

2. Crear y activar entorno virtual (uso `venv`):

Linux / macOS:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Ejecutar la app con uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

La API quedará accesible en `http://127.0.0.1:8000` y la documentación automática en `/docs`.

Notas sobre la base de datos
- La imagen MySQL se configura con `MYSQL_ALLOW_EMPTY_PASSWORD=yes` para permitir contraseña vacía.
- Base de datos por defecto: `products_db`.
- Cadena de conexión por defecto (app): `mysql+asyncmy://root@127.0.0.1:3306/products_db?charset=utf8mb4`.


Endpoints
- `POST /products` crear producto
- `GET /products` listar productos
- `GET /products/{id}` obtener producto
- `PUT /products/{id}` actualizar producto
- `DELETE /products/{id}` eliminar producto

Ejemplos con curl

- Crear un producto:

```bash
curl -s -X POST http://127.0.0.1:8000/products \
	-H "Content-Type: application/json" \
	-d '{"name":"Lapicero","description":"Azul","price":1.5}'
```

- Listar productos:

```bash
curl -s http://127.0.0.1:8000/products
```

- Obtener un producto por id (ej: id = 1):

```bash
curl -s http://127.0.0.1:8000/products/1
```

- Actualizar un producto (ej: id = 1):

```bash
curl -s -X PUT http://127.0.0.1:8000/products/1 \
	-H "Content-Type: application/json" \
	-d '{"name":"Lapicero XL","price":2.0}'
```

- Eliminar un producto (ej: id = 1):

```bash
curl -s -X DELETE http://127.0.0.1:8000/products/1 -w "\nHTTP_STATUS:%{http_code}\n"
```

Notas sobre las respuestas
- `POST` devuelve el objeto creado (`201 Created`).
- `GET` lista y obtiene objetos (`200 OK`) o `404 Not Found` si no existe.
- `PUT` devuelve el objeto actualizado (`200 OK`).
- `DELETE` devuelve `204 No Content` en éxito.


Si quieres que cree una imagen Docker para la app o que ponga variables de entorno en un `.env`, dímelo.
