server:
	poetry run start

postgres:
	docker exec -it postgres bash -c "psql -U postgres -d music_db"

minio:
	docker exec -it minio bash
	# mc alias set localhost http://localhost:9000 andrey 12345test
	# mc mb localhost/tracks

a:
	python andrey.py