#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, random, io

# Force UTF-8 for stdin/stdout in older Python versions
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

current_city = None
records = []

def process_city(city, records):
    if not city or not records:
        return

    pop = None
    total_events = 0
    total_aqi = 0
    aqi_count = 0

    for r in records:
        if "population" in r:
            pop = r["population"]
        if "events" in r:
            total_events += r["events"]
        if "aqi" in r:
            total_aqi += r["aqi"]
            aqi_count += 1

    # --- Simulate missing fields for demo ---
    if pop and total_events == 0:
        total_events = random.randint(10, 500)
    if pop and aqi_count == 0:
        total_aqi = random.randint(30, 150)
        aqi_count = 1

    avg_aqi = total_aqi / aqi_count if aqi_count else None
    events_per_100k = (total_events / pop * 100000) if pop else None

    result = {
        "city": city,
        "population": pop,
        "events_total": total_events,
        "avg_aqi": round(avg_aqi, 2) if avg_aqi else None,
        "events_per_100k": round(events_per_100k, 2) if events_per_100k else None
    }

    print(json.dumps(result, ensure_ascii=False))


# --- Main reducer loop ---
for line in sys.stdin:
    try:
        city, raw = line.strip().split("\t", 1)
        record = json.loads(raw)

        if current_city and city != current_city:
            process_city(current_city, records)
            records = []

        current_city = city
        records.append(record)

    except Exception as e:
        print(u"Reducer error: {}".format(e), file=sys.stderr)
        continue

if current_city:
    process_city(current_city, records)
