# Requirements
* Must have the latest version of Python installed
* Must have installed Docker

# Structure
This is a docker-compose application separated by crawling-agent/api. The function of each
of each profile is listed below.

## Crawling-Agent
This application hosts the main crawling scripts supported thru use of a library called
Scrapy. The library instance manages task scheduling for each of the crawling tasks. Each
spider hooks into a MongoDB item pipeline, which offloads the raw data into a Mongo collection
to be later cleaned and sent for analysis.

The application is designed to offload data into JSON files if a critical exception occurs
and after every successful run of a spider. The temporary data can be found in ``data``.

## API
There is a simplistic internal-use Flask API that exposes endpoints that will retrieve and return the data. This is primarily to communicate with other services that rely on any of the crawled raw data or to retrieve machine learning translations.

# Deployment
Deployment of the application is supported thru a docker-compose process. There are npm scripts provided to deploy the API and crawling suite as separate units to a container registry.