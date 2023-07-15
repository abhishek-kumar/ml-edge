prediction_service:
	uvicorn app.prediction_service:app --reload

image:
	docker build -t prediction_service .

prediction_service_container:
	docker run --name prediction_service \
		--detach \
		-p 8000:8000 \
		prediction_service



.PHONY: prediction_service image