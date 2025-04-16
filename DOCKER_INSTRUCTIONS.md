## Development

### Start up Dev Environment

```
docker-compose up --build
```

### Clear the Dev Enviroment

This also clears the databases since it removes the volumes

```
docker-compose down -v
```

## Start up Production Environment (TBD)

docker-compose -f docker-compose.prod.yml up -d --build

docker-compose -f docker-compose.prod.yml down -v

-d --> detached mode
