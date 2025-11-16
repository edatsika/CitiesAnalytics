#!/bin/bash
set -e

NDJSON_PATH="/app/data/cities_dbpedia.ndjson"

echo "Starting Hadoop job..."

# --- Step 1: Prepare HDFS directories ---
docker exec -it namenode hdfs dfs -mkdir -p /data/input
docker exec -it namenode hdfs dfs -rm -r /data/output || true

# --- Step 2: Upload input data to HDFS ---
echo "Uploading NDJSON data to HDFS..."
docker exec -it namenode hdfs dfs -put -f $NDJSON_PATH /data/input/

# --- Step 3: Run Hadoop streaming job ---
echo "Running Hadoop streaming job..."
docker exec -it namenode bash -c "
hadoop jar /opt/hadoop-3.1.3/share/hadoop/tools/lib/hadoop-streaming-3.1.3.jar \
  -files /app/hadoop/mapper.py,/app/hadoop/reducer.py \
  -mapper '/usr/bin/python3 mapper.py' \
  -reducer '/usr/bin/python3 reducer.py' \
  -input /data/input/ \
  -output /data/output/
"

# --- Step 4: Fetch results from HDFS ---
echo "Fetching results from HDFS..."
docker exec -it namenode bash -c "
hdfs dfs -cat /data/output/* > /app/results/aggregated_results.json
"

echo "Hadoop job completed successfully!"
echo "Results saved to ./results/aggregated_results.json"
