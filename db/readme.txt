# how to run from root folder

docker build -t custom-postgres ./db

docker run -d --name postgres-db -p 5432:5432 custom-postgres
