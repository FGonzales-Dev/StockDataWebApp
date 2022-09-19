web: gunicorn cb_dj_weather_app.wsgi --timeout 600 --log-file -
worker: celery -A cb_dj_weather_app worker --beat