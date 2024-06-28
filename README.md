# movemakers-backend

(wip) find your favorite instructors, studios, classes, crews, and even choreographies!

### lint & format

```sh
# lint
❯ ruff check --fix .
❯ ruff check --fix --select I

# format
❯ black .
```

### tests

```sh
❯ docker exec -it app bash
```

```sh
root@01c3febebb0d:/app# pytest
```

### run app in docker

```sh
# shut down
❯ docker-compose down

# shut down and remove volumes
❯ docker-compose down -v

# build & run in detached mode
❯ docker-compose up -d --build
```
