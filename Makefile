port?=8080
repo_name=test

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
	docker rm $(docker_img_tag)
	docker run \
	-v $(pwd)/certifications:/app/certifications \
	--name $(docker_img_tag) \
	-p $(port):8080 \
	movingju/$(repo_name):$(docker_img_tag)

docker-push: docker-build
	docker push movingju/$(repo_name):$(docker_img_tag)

docker-pull:
	docker pull movingju/$(repo_name):$(docker_img_tag)

docker-clear:
	docker stop $$(docker ps -aq)
	docker rm $$(docker ps -aq)
	docker rmi $$(docker image ls -aq)

build:
	./.venv/bin/pyinstaller --log-level=ERROR --noconfirm --add-data ".env:.env" --add-data "data:data" main.py
	rm -r build main.spec

run:
	uv sync
	./.venv/bin/uvicorn main:app --port $(port) --host 0.0.0.0 
# 	uv run main.py

clear:
	rm -r .venv dist 