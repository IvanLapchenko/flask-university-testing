docker stop app && docker rm app
docker image rm app
docker build -t app:latest .
docker run --name app -p 80:5000 app