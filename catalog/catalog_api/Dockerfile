FROM python:3.7.3-alpine3.8
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["sh", "gunicorn_server.dev.sh"]

# To build execute:
# docker build -t catalog-api .
# To deploy container:
# docker run --name catalog-api -d -p 80:80 catalog-api
