# Example Dash App for Docker Containers

Using yfinance data for WTI, RBOB and HO to plot candlestick charts

## Start Docker Daemon
sudo dockerd

## To run:
sudo docker build -t example_app .

sudo docker run -d -p 8080:8000 example_app

Then go to:
http://127.0.0.1:8080


To run this image from Docker Hub use the following commands

sudo docker build -t bbcho/example_app

sudo docker run -d -p 8080:8000 bbcho/example_app

Then go to:
http://127.0.0.1:8080


## To Push to Docker Hub

docker images

docker tag ef54e9712cca bbcho/example_app:latest

docker push bbcho/example_app:latest
