#!/bin/bash

if [ "$FLASK_ENV" = "production" ]; then
  echo "Running in production mode...";
else
  echo "Running in development mode...";
fi;

if [ "$USE_GUNICORN" = "1" ]; then
  gunicorn covidapi.wsgi:app\
    -w "$GUNICORN_WORKERS" \
    --bind :8081 \
    --reload  \
    --timeout=240 \
    --graceful-timeout=60 \
    --log-level=DEBUG;
else
   covidapi run --host=0.0.0.0 --port=8081;
fi;
