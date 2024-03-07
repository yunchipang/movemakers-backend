# movemakers-fastapi

### lint & format

```
❯ ruff check . --fix # run linter (ruff)
❯ black .  # run formatter (black)
```

### migrations

```
❯ docker compose exec web alembic init alembic # init migration directory
❯ docker compose exec web alembic revision --autogenerate -m "<migration message>" # generate migration file
❯ docker compose exec web alembic upgrade head # apply migrations
```

### run app in docker

```
❯ docker-compose down # shut down
❯ docker-compose down -v # shut down and remove the volumes
❯ docker-compose up -d --build # build & run
```
