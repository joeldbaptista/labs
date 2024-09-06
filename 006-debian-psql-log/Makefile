
up:
	sudo docker compose up -d

upd:
	sudo docker compose up -d

buildd:
	sudo docker compose up -d --build

build:
	sudo docker compose up --build

down:
	sudo docker compose down

ps:
	sudo docker compose ps

############################################
# Get into the containers
############################################

db:
	sudo docker compose exec db psql -h localhost -p 5432 -U postgres -d sandbox

app:
	sudo docker compose exec app bash

prometheus:
	sudo docker compose exec prometheus sh

grafana:
	sudo docker compose exec grafana sh

