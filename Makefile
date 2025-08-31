port?=8080
repo_name=public

platform=linux/arm64,linux/amd64#,linux/arm/v7
docker_img_tag=pigo_rec

.PHONY: build run
docker-build:
	docker buildx build \
		--platform  $(platform) \
		-t movingju/$(repo_name):$(docker_img_tag) \
		.

docker-test:
	docker build \
	-t movingju/$(repo_name):$(docker_img_tag) \
	.

docker-run:
	docker run -p $(port):8080 movingju/$(repo_name):$(docker_img_tag)

docker-push: docker-build
	docker push movingju/$(repo_name):$(docker_img_tag)

docker-pull:
	docker pull movingju/$(repo_name):$(docker_img_tag)

docker-clear:
	docker stop $$(docker ps -aq)
	docker rm $$(docker ps -aq)
	docker rmi $$(docker image ls -aq)

build:
	pyinstaller --log-level=ERROR main.py
	rm -r build main.spec

run:
	./.venv/bin/uvicorn main:app --reload --port $(port) --host 0.0.0.0 --reload-exclude .venv
# 	uv run main.py

clear:
	rm -r .venv dist 