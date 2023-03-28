python3 manage.py flush --no-input
python3 manage.py migrate
python3 manage.py collectstatic --no-input --clear

gunicorn account.wsgi:application --bind 0.0.0.0:8000
