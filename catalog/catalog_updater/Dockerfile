FROM python:3.7.3-alpine3.8
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["celery", "-A", "updater", "worker", "--loglevel=INFO"]

# To build execute:
# docker build -t catalog-updater .
# To deploy container:
# docker run --name catalog-updater -d catalog-updater
