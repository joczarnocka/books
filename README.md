## requirements:
- python 3.9 `(pip install -r requirement.txt)`
- redis server 3.2
## development

### configuration:
Create config.json with the following content:
```
{
  "DEBUG": "1",
  "SECRET_KEY": "", #write something
  "REDIS_HOST": "localhost",
  "REDIS_PORT": "6379",
  "HUEY_ENABLED": "0"
}
```

### commands:
```
python manage.py runserver

# run worker
python manage.py run_huey
```

## deployment:
Procfile when Redis is available:
```
web: gunicorn Books.wsgi
worker: python manage.py run_huey
release: python manage.py migrate
```
otherwise:
```
web: gunicorn Books.wsgi
release: python manage.py migrate
```