server:
	python src/index.py

psql:
	docker exec -it postgres bash -c \
	"psql postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:5432/${POSTGRES_DB_NAME}"

minio:
	docker exec -it minio bash
	# mc alias set localhost http://localhost:9000 andrey 12345test
	# mc mb localhost/tracks

format:
	isort .
	black .

consume:
	faststream run src/adapters/driving/rabbitmq/index:app