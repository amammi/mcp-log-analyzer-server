docker build -t fastapi-springlog .
docker run -d -p 8050:8050 --name application fastapi-springlog