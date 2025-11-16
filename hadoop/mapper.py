#!/usr/bin/env python3
import sys, json

for line in sys.stdin:
    try:
        record = json.loads(line)
        city = record.get("city") or record.get("name")
        if not city:
            continue
        # Only include relevant fields
        output = {}
        if "population" in record:
            output["population"] = record["population"]
        if "events" in record:
            output["events"] = record["events"]
        if "aqi" in record:
            output["aqi"] = record["aqi"]
        #print(f"{city}\t{json.dumps(output)}")
        # Python 3.5 compatible
        print("{}\t{}".format(city, json.dumps(output)))
    except Exception as e:
        #print(f"Mapper error: {e}", file=sys.stderr)
        print("Reducer error: {}".format(e), file=sys.stderr)
        continue
