# sparql/query_dbpedia.py: Fetches city info (name, country, population) from DBpedia and saves it as JSON.
from SPARQLWrapper import SPARQLWrapper, JSON
import json

sparql = SPARQLWrapper("https://dbpedia.org/sparql")
sparql.setQuery("""
SELECT ?city ?cityLabel ?countryLabel ?population
WHERE {
  ?city a dbo:City ;
        dbo:country ?country ;
        dbo:populationTotal ?population ;
        rdfs:label ?cityLabel .
  ?country rdfs:label ?countryLabel .
  FILTER(lang(?cityLabel) = "en")
  FILTER(lang(?countryLabel) = "en")
}
LIMIT 50
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

cities = []
for r in results["results"]["bindings"]:
    cities.append({
        "city_uri": r["city"]["value"],
        "name": r["cityLabel"]["value"],
        "country": r["countryLabel"]["value"],
        "population": int(r["population"]["value"])
    })

with open("data/cities_dbpedia.json", "w", encoding="utf-8") as f:
    json.dump(cities, f, indent=2)

print(f"Saved {len(cities)} cities to data/cities_dbpedia.json")
