
## Development

docker-compose -f docker-compose.yml up --build

## prod

docker-compose -f docker-compose.prod.yml up -d --build

docker-compose -f docker-compose.prod.yml down -v

-d --> detached mode
