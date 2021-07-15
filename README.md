# Django REST API Template

## How To Run
### 1. Create environment
```
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Run DB from docker-compose
```
docker-compose up -d db
```

### 3. Run migrate for db
```
python manage.py migrate
```

### 4. Run server
```
python manage.py runserver
```
Server will run at localhost and listen on port 8000
