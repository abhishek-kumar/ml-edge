app:
	GOOGLE_APPLICATION_CREDENTIALS=cloud-vision-credentials.json uvicorn app:app --reload

tests:
	pytest --capture=no test_cloud_vision.py

.PHONY: app tests
