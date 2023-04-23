# Requirements
* Must have the latest version of Python installed
* Must have installed Docker

# Structure
This is a docker-compose application separated into services. The function of each
of each profile is listed below.

## Services
    * redis (RedisCloud)
    * mongodb (Atlas)
    * scrapyd cluster (1+ daemon instances)
    * scrapydweb

The Redis instance is supported thru RedisCloud. MongoDB services are provided by MongoDB Atlas, which allows for offloading of data.

# Data
This is a distributed crawling system which is designed to schedule and execute crawling jobs across one or more daemon services. There is an interactive UI provided by scrapydweb which contains the scheduler as well as the ability to create timer tasks to be run across the daemon instances. Data dupefiltering is supported thru a redis cache which ensures that crawls can be paused and resumed at any point. Crawling data is committed to the MongoDB database or to AWS S3 object storage once jobs have finished.

The production server will allow users to pull data from S3 using a lamba function stored on AWS.

Each month, a full re-crawl of the datasets will be executed so as to ensure the data is up to date.

# Development Environment
To run the environment as a docker-compose service (for testing), run the following
commands.

```commandline
pip install -r requirements.txt
docker build ./scrapyd -t scrapydaemon
docker tag scrapydaemon analytixcr/scrapyd
docker build ./scrapydweb -t webclient
docker tag webclient cr2244/scrapydweb
docker compose up -d
```

# Deployment

## ScrapydWeb
Run

```commandline
docker build --platform=linux/amd64 ./scrapydweb -t cr2244/analytix-scrapydweb:latest
docker login && docker push cr2244/analytix-scrapydweb:latest
```

then restart the Azure App Service instance.

## Scrapyd Daemon Instances
First, confirm the deploy configuration of the daemon instance you wish to target. Replace
all tags with the corresponding container registry and tags below, then run

```commandline
docker build --platform=linux/amd64 ./scrapyd -t cr2244/analytix-scrapyd:daemon0
docker login
docker push cr2244/analytix-scrapyd:daemon0
```

and restart the corresponding Azure App Service instance.