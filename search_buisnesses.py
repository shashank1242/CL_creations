import requests
import csv

def search_businesses_osm(city, business_type="restaurant"):
    query = f"""
    [out:json];
    area[name="{city}"]->.searchArea;
    node[amenity={business_type}](area.searchArea);
    out body;
    """
    response = requests.get(
        "https://overpass-api.de/api/interpreter",
        params={"data": query}
    ).json()

    businesses = []
    for place in response["elements"]:
        tags = place.get("tags", {})
        businesses.append({
            "name": tags.get("name", "N/A"),
            "type": tags.get("amenity"),
            "phone": tags.get("phone", "N/A"),
            "website": tags.get("website", "N/A"),
            "address": tags.get("addr:full", tags.get("addr:street", "N/A")),
            "lat": place.get("lat"),
            "lon": place.get("lon"),
        })

    with open("businesses.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=businesses[0].keys())
        writer.writeheader()
        writer.writerows(businesses)

    print(f"Saved {len(businesses)} results")


search_businesses_osm("Bengaluru", "cafe")
