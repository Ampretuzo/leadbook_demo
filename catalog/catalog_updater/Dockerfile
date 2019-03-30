FROM ubuntu:latest
RUN apt-get -q update -y
RUN apt-get -q install -y python3-pip
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["celery", "-A", "updater", "worker", "--loglevel=INFO"]

# To build execute:
# docker build -t catalog-updater .
# To deploy container:
# docker run --name catalog-updater -d catalog-updater
