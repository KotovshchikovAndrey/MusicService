.PHONY: server

server:
	python src/index.py


.PHONY: psql

psql:
	docker exec -it postgres bash -c \
	"psql postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:5432/${POSTGRES_DB_NAME}"


.PHONY: minio

minio:
	docker exec -it minio bash
	# mc alias set localhost http://localhost:9000 andrey 12345test
	# mc mb localhost/tracks


.PHONY: formating

formating:
	isort .
	black .


.PHONY: consumer

consumer:
	faststream run src/adapters/driving/rabbitmq/index:app


.PHONY: migrations

migrations:
	alembic revision --autogenerate
	alembic upgrade head