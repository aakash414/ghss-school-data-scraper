import json
import time
import requests

# Step 1: Read from pasted txt
stations = []

with open("kerala_stations.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) >= 3:
            code = parts[1].strip()
            name = parts[2].strip()
            place = parts[3].strip() if len(parts) > 3 else ""
            stations.append({"code": code, "name": name, "place": place})

# Step 2: Geocode
def get_lat_lon(name):
    query = f"{name} railway station, Kerala, India"
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={requests.utils.quote(query)}"
    try:
        response = requests.get(url, headers={"User-Agent": "10xDevScript/1.0"})
        if response.ok:
            data = response.json()
            if data:
                return {"lat": float(data[0]["lat"]), "lon": float(data[0]["lon"])}
    except Exception as e:
        print(f"Error for {name}: {e}")
    return {"lat": None, "lon": None}

# Step 3: Enrich with coordinates
enriched = []
for s in stations:
    print(f"Geocoding: {s['name']}")
    coords = get_lat_lon(s["name"])
    enriched.append({**s, **coords})
    time.sleep(1.1)  # Respect Nominatim rate limit

# Step 4: Save
with open("kerala_railway_stations.json", "w", encoding="utf-8") as f:
    json.dump(enriched, f, indent=2, ensure_ascii=False)

print("✅ Saved to kerala_railway_stations.json")
