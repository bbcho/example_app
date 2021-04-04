# Example Dash App for Docker Containers

Using yfinance data for WTI, RBOB and HO to plot candlestick charts

## To run:
sudo docker build -t ex_app .
sudo docker run -d -p 8080:8000 ex_app

Then go to:
http://127.0.0.1:8080