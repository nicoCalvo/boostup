prodserver:
	gunicorn -w 4 app:app

testserver:
	python manage.py runserver


test:
	coverage run -m pytest  -s

urls:
	FLASK_APP='HubspotProxy.app' flask routes