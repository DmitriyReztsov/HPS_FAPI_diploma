# HPS_FAPI_diploma
High Programminh School of Bobrovsky diploma work on FastAPI

To start the app:
```uvicorn main:app --reload --port 8001```

To generate migration
```alembic revision --autogenerate -m "Migration message"```
```alembic upgrade head```

To start in containers:
```docker-compose up --build```

Then run migrations in backend-fastapi container