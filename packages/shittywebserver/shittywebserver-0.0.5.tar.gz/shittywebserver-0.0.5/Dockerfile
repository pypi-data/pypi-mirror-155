FROM python:3.10
ENV ENV=DOCKER
RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY . $PWD
RUN pip3 install --no-cache-dir -e .
WORKDIR /opt/app/shittywebserver
CMD [ "python3", "./main.py" ]
