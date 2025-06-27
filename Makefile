up:
	uvicorn app:APP --reload --port=8000

log:
	git log --all --oneline --graph