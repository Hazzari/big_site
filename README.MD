# Проект для изучения Django

### 1. Простой блог на Django


- TODO: Разобраться со времением
```
    ~~from django.db.models.functions import datetime~~

    # naive
    now1 = datetime.datetime.now()
    # TZ aware
    from django.utils.timezone import utc
    now2 = datetime.datetime.utcnow().replace(tzinfo=utc)
    print(now1)
    print(now2)
```