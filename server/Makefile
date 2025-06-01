build:
	docker build -t kozmodb-api-server .

run_local:
	docker run -p 8000:8000 -v $(shell pwd):/app kozmodb-api-server --env-file .env

.PHONY: build run_local
