import csv
import datetime

import pymongo
from pymongo import MongoClient
import uuid

client = MongoClient('mongodb://mongodb:27017')

new_industries = []

with open('2022_titles_descriptions.tsv') as csvfile:
     reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
     for row in reader:
         try:
             cleaned_number = row[0].replace('"','')
             if len(cleaned_number) == 4:
                industry_naics = int(cleaned_number)
                new_industry = {
                    "pid": str(uuid.uuid4()),
                    "naicsCode": industry_naics,
                    "name": row[2].replace('"',''),
                    "description": row[3].replace('"',''),
                    "createdAt": datetime.datetime.utcnow()
                }
                print(new_industry)
                new_industries.append(new_industry)
         except:
             continue
     print('inserting')
     client['analytix'].industries.insert_many(new_industries)