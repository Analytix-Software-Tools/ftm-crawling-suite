# Requirements
* Must have the latest version of Python installed
* Must have installed Docker

# Structure
This is a docker-compose application separated into services. The function of each
of each profile is listed below.

## Services
    * redis
    * mongodb
    * scrapyd cluster (1+ daemon instances)
    * scrapydweb

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
docker tag webclient analytixcr/scrapydweb
docker compose up -d
```