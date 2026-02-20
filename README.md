# Django + Redis + Celery Demo

Цей проект демонструє, як інтегрувати Redis (як брокер повідомлень та кеш) та Celery (для фонових завдань) у Django.

## Як запустити

Тобі знадобляться три термінали.

### 1. Підготовка (в будь-якому терміналі)
Встанови залежності:
```bash
pip install -r requirements.txt
```
### 1. Підготовка (в будь-якому терміналі)
Встанови залежності:
```bash
pip install -r requirements.txt
```

⚠️ **Важливо: Redis Сервер**
Помилка `Error 10061 connection refused` означає, що у тебе не запущений Redis.
На Windows його треба встановити окремо:
1.  **Варіант А (Простий):** Завантаж та встанови [Memurai Developer](https://www.memurai.com/get-memurai) (це Redis для Windows).
2.  **Варіант Б (Класичний):** Використовуй порт [Redis for Windows](https://github.com/tporadowski/redis/releases) (завантаж .msi або .zip і запусти `redis-server.exe`).
3.  **Варіант В (Docker):** Якщо є Docker, запусти: `docker run -p 6379:6379 -d redis`.


### 2. Запуск Django (Термінал 1)
Це основний веб-сервер.
```bash
python manage.py runserver
```

### 3. Запуск Celery Worker (Термінал 2)
Це процес, який буде виконувати фонові завдання.
В Windows (через обмеження) іноді треба додавати `-P gevent` або `solo`, якщо є проблеми:
```bash
python -m celery -A config worker --loglevel=info -P solo
```
(для Linux/Mac просто `celery -A config worker --loglevel=info`)

### 4. Тестування
Відкрий браузер і перейди за посиланнями:

1.  **http://127.0.0.1:8000/trigger-task/**
    - Ти побачиш миттєву відповідь JSON.
    - Подивись у **Термінал 2** (Celery) — там з'явиться повідомлення про старт завдання, воно "почекає" 5 секунд і завершиться. Веб-сторінка при цьому не зависла!

2.  **http://127.0.0.1:8000/cache-test/**
    - Оновлюй сторінку кілька разів.
    - Лічильник буде зростати, і дані зберігаються у Redis (а не в базі даних SQL).
