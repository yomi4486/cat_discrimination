run:
	@start uvicorn api:app --host 0.0.0.0 --port 8008 --reload

install:
	@pip3 install -r requirements.txt

train:
	@python3 model.py