docker stop front-monitoreio-container

docker rm front-monitoreio-container

docker rmi front-monitoreo-img

docker build -t front-monitoreo-img .

docker run -d -p 3001:3001 --name front-monitoreio-container front-monitoreo-img

