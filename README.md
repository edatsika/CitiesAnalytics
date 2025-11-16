# City Analytics

## Overview

This project aggregates city-level metrics using data fetched from **DBpedia** and processed with **Hadoop streaming**. 
This project processes city data from DBpedia to calculate event statistics and air quality indicators. It uses Hadoop Streaming for map-reduce processing and Python for mapper and reducer scripts. The workflow is containerized with Docker, including services for Hadoop (namenode, datanode) and a SPARQL client to fetch city data.

---

## Steps

1. **Fetch city data via SPARQL**:
   Output: data/cities_dbpedia.json
   ```bash
   python3 sparql/query_dbpedia.py
   

2. **Run Hadoop streaming job**:
   This runs mapper.py and reducer.py over the input JSON/NDJSON files.

    ```bash
    bash hadoop/run_job.sh

3. **Fetch results from HDFS**:
    Output saved in results/aggregated_results.json.

    Example Output:
   
    ```bash
    {
      "city": "Ardestan",
      "events_per_100k": 273.12,
      "events_total": 43,
      "population": 15744,
      "avg_aqi": 71.0
    }

---
## Requirements

- Python 3.x

- Hadoop (configured with HDFS)

- SPARQLWrapper (pip install SPARQLWrapper)

## Notes

- Mapper and reducer are compatible with older Python versions and handle UTF-8 city names.

- Missing events/AQI values are simulated for demonstration purposes.
