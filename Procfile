web: gunicorn cb_dj_weather_app.wsgi --timeout 600 --log-file -

orker: celery -A cb_dj_weather_app worker -l info -B