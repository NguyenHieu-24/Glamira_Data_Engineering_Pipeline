from pymongo import MongoClient
import pandas as pd
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import time


def connect_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    return client["countly"]


# -----------------------------------
# Extract product từ summary
# -----------------------------------
def extract_product_urls(db):
    collection = db["summary"]

    product_map = {}

    print("Extracting product data...")

    query = {
        "collection": {
            "$in": [
                "view_product_detail",
                "select_product_option",
                "select_product_option_quality",
                "add_to_cart_action",
                "product_detail_recommendation_visible",
                "product_detail_recommendation_noticed",
                "product_view_all_recommend_clicked"
            ]
        }
    }

    projection = {
        "product_id": 1,
        "current_url": 1,
        "referrer_url": 1,
        "viewing_product_id": 1
    }

    cursor = collection.find(query, projection)

    for doc in tqdm(cursor):
        product_id = doc.get("product_id") or doc.get("viewing_product_id")
        url = doc.get("current_url") or doc.get("referrer_url")

        if product_id and url:
            if product_id not in product_map:
                product_map[product_id] = url

    print(f"Total unique products: {len(product_map)}")
    return product_map


# -----------------------------------
# Crawl product name
# -----------------------------------
def crawl_product_name(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=5)

        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, "html.parser")

        # Try multiple selectors
        for tag in ["h1", "title"]:
            el = soup.find(tag)
            if el and el.text.strip():
                return el.text.strip()

        return None

    except Exception:
        return None


# -----------------------------------
# Main pipeline
# -----------------------------------
def build_product_dataset():
    db = connect_mongo()

    product_map = extract_product_urls(db)

    results = []
    success = 0
    fail = 0

    print("Crawling product names...")

    for pid, url in tqdm(product_map.items()):
        name = crawl_product_name(url)

        if name:
            results.append({
                "product_id": pid,
                "product_name": name,
                "url": url
            })
            success += 1
        else:
            fail += 1

        time.sleep(0.05)

    print(f"Success: {success}, Fail: {fail}")

    df = pd.DataFrame(results)
    df.to_csv("products.csv", index=False)

    print("Saved to products.csv")


if __name__ == "__main__":
    build_product_dataset()