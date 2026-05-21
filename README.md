# django-primer

How to install
------------  
*If **poetry** is not installed then run ``pip install poetry``
```
  poetry install
```
To set up environment variables copy `.env_example` to `.env` file and set service variables:
```
  cp .env_example .env
```

How to use
------------    
To migrate DB:
```
  python manage.py migrate
```

To start DEV server:
```
  python manage.py runserver
```
