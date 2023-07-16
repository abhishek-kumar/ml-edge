IMAGE-NAME=prediction_service
REGION=us-east4
PROJECT-ID=aiedge-masterclass
REPOSITORY=prediction-service
IMAGE=prediction_service

TAG=${REGION}-docker.pkg.dev/${PROJECT-ID}/${REPOSITORY}/${IMAGE}

prediction_service:
	uvicorn app.prediction_service:app --reload

image:
	docker build -t prediction_service -t ${TAG} .

push:
	docker push ${TAG}

# if you're building an amd64 image on an arm64 computer
multi-arch:
	docker buildx build --platform linux/amd64 --push -t ${TAG} .

prediction_service_container:
	docker run --name prediction_service \
		--detach \
		-p 8000:8000 \
		prediction_service



.PHONY: prediction_service image multi-arch push