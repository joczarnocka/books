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
  "REDIS_PORT": "6379"
}
```

### commands:
```
python manage.py runserver

# run worker
python manage.py run_huey
```