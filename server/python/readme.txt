# how to run from root folder for tests

docker build -t fastapi-server ./server/python/
docker run -it -p 8000:8000 fastapi-server bash
uvicorn app:app --host 0.0.0.0 --port 8000


# how to run from root folder

docker build -t fastapi-server ./server/python/