---
description: Start Django Backend and Celery Worker
---

# Start Backend Services
// turbo-all

1. Start Django Server
   - Command: `python manage.py runserver`
   - Directory: `c:\Development\P4\Development\HuntersGarage\Tests\django_celery_demo`
   - Async: Yes

2. Start Celery Worker
   - Command: `python -m celery -A config worker --loglevel=info -P solo`
   - Directory: `c:\Development\P4\Development\HuntersGarage\Tests\django_celery_demo`
   - Async: Yes
