# Run
```
docker run -it --name fastapi --rm -p 8001:8000 -v $(pwd)/app:/app fastapi:test
```


# Migration
```
cd app
alembic revision --autogenerate -m "comment"
alembic upgrade head
```