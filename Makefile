.PHONY: install dev web mobile server worker test lint format seed docker-up docker-down

install:
	pnpm install

dev: docker-up
	pnpm --filter web dev

web:
	pnpm --filter web dev

mobile:
	pnpm --filter mobile start

server:
	cd apps/server && uvicorn app.main:app --reload

worker:
	cd apps/worker && poetry run fashion3d-worker

test:
	pnpm -r test

lint:
	pnpm -r lint

format:
	pnpm -r format

seed:
	cd apps/server && poetry run python app/scripts/seed.py

docker-up:
	docker compose up -d

docker-down:
	docker compose down
