@echo off
cd /d "%~dp0"

echo Starting Django Server...
start "Django Server" cmd /k "python manage.py runserver"

echo Starting Celery Worker...
start "Celery Worker" cmd /k "python -m celery -A config worker --loglevel=info -P solo"

echo Starting Celery Beat (Scheduler)...
start "Celery Beat" cmd /k "python -m celery -A config beat --loglevel=info"

echo Done!
timeout /t 5
