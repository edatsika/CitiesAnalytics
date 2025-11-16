# couchdb/load_citydata.py: Loads simulated local data (events, AQI, etc.) into CouchDB.
import couchdb
import random
import datetime

COUCHDB_URL = "http://admin:admin@couchdb:5984/"
DB_NAME = "citydata"

couch = couchdb.Server(COUCHDB_URL)

if DB_NAME in couch:
    db = couch[DB_NAME]
else:
    db = couch.create(DB_NAME)

sample_cities = ["Paris", "Berlin", "Madrid", "London", "Rome", "Warsaw"]

for city in sample_cities:
    doc = {
        "city": city,
        "aqi": random.randint(20, 120),
        "events": random.randint(100, 500),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    db.save(doc)

print(f"Inserted {len(sample_cities)} documents into CouchDB '{DB_NAME}'")
