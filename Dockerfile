FROM python:3.9.2-slim-buster

# RUN apt-get update

# COPY . /opt/src

# RUN pip install -r /opt/src/requirements.txt

#EXPOSE 8050

#ENTRYPOINT [ "python", "/opt/src/app.py" ]


# Create a working directory.
RUN mkdir /wd
WORKDIR /wd

# Install Python dependencies.
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the rest of the codebase into the image
COPY . ./

# Finally, run gunicorn.
CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:8000", "app:server"]