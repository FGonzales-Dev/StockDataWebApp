

web: gunicorn --timeout 120 cb_dj_weather_app.wsgi --log-file -

celery: celery -A cb_dj_weather_app worker --loglevel=info