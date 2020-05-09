FLASK_ENV=development
FLASK_APP=covidapi.app:create_app
SECRET_KEY=changeme
DATABASE_URI=sqlite:////tmp/covidapi.db
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=amqp://guest:guest@localhost/
