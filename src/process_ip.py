import IP2Location
from pymongo import MongoClient
from tqdm import tqdm
import pandas as pd

DB_FILE = "IP-COUNTRY-REGION-CITY.BIN"

def process_ip_locations():
    # 1. Connect MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["countly"]
    collection = db["summary"]
    location_collection = db["ip_location"]

    # (Optional) Clear old data
    location_collection.drop()

    # 2. Load IP database
    ip_db = IP2Location.IP2Location(DB_FILE)

    # 3. Use aggregation instead of distinct
    pipeline = [
        {"$match": {"ip": {"$ne": None}}},
        {"$group": {"_id": "$ip"}}
    ]

    cursor = collection.aggregate(pipeline, allowDiskUse=True)

    results = []
    count = 0

    print("Processing IPs...")

    # 4. Process each IP
    for doc in tqdm(cursor):
        ip = doc["_id"]

        try:
            record = ip_db.get_all(ip)

            data = {
                "ip": ip,
                "country": record.country_long,
                "region": record.region,
                "city": record.city
            }

            results.append(data)
            count += 1

            # Insert batch every 1000 records
            if len(results) >= 1000:
                location_collection.insert_many(results)
                results = []

        except Exception as e:
            print(f"Error with IP {ip}: {e}")

    # Insert remaining
    if results:
        location_collection.insert_many(results)

    print(f"Total processed IPs: {count}")

    # 5. Save to CSV
    df = pd.DataFrame(location_collection.find({}, {"_id": 0}))
    df.to_csv("ip_locations.csv", index=False)

    print("Processing completed!")


if __name__ == "__main__":
    process_ip_locations()