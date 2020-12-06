prodserver:
	gunicorn -w 4 app:app

testserver:
	python manage.py runserver


test:
	python -m pytest --cov=./

urls:
	FLASK_APP='HubspotProxy.app' flask routes