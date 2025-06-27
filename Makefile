s:
	uvicorn app:APP --reload --port=8000

log:
	git log --all --oneline --graph

up:
	docker compose up --build -d
down:
	docker compose down
