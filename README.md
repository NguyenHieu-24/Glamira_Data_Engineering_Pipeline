# 🚀 Glamira Data Engineering Pipeline

## 📌 Overview

This project builds an end-to-end data pipeline to process raw event data, enrich it with geolocation information, and extract product insights for downstream analytics.

The pipeline simulates a real-world data engineering workflow using cloud infrastructure and scalable data processing techniques.

---

## 🎯 Objectives

* Process raw BSON data into a structured format
* Enrich IP addresses with geographic location
* Extract product interaction data from event logs
* Crawl product names from URLs
* Produce clean datasets for analytics and visualization

---

## 🏗️ Architecture

```
Google Cloud Storage (Raw Data)
        ↓
Virtual Machine (MongoDB)
        ↓
Python Data Processing
        ↓
Processed Outputs (CSV + MongoDB)
```

---

## ⚙️ Tech Stack

* **Cloud**: Google Cloud Platform (GCS, Compute Engine)
* **Database**: MongoDB
* **Programming**: Python
* **Libraries**:

  * pymongo
  * IP2Location
  * pandas
  * requests
  * BeautifulSoup
  * tqdm

---

## 📂 Dataset

### Input Files

* `summary.bson`: Raw event data
* `summary.metadata.json`: MongoDB metadata
* `IP-COUNTRY-REGION-CITY.BIN`: IP geolocation database

### Data Characteristics

* Event-based schema (single collection: `summary`)
* Contains user activity, product interactions, and metadata

---

## 🔄 Data Pipeline

### 1. Data Ingestion

* Imported BSON data into MongoDB (`countly.summary`)
* Verified schema and indexes

---

### 2. IP Location Enrichment

* Extracted unique IP addresses using MongoDB aggregation
* Enriched IPs with:

  * Country
  * Region
  * City
* Stored results:

  * MongoDB collection: `ip_location`
  * File: `ip_locations.csv`

---

### 3. Product Data Extraction

* Filtered event data using `collection` field (event type)
* Extracted:

  * `product_id`
  * `current_url` / `referrer_url`
* Deduplicated products

---

### 4. Product Name Crawling

* Crawled product names from URLs using HTTP requests
* Parsed HTML using BeautifulSoup
* Ensured one product name per product_id

---

### 5. Data Output

* `ip_locations.csv`
* `products.csv`

---

## ▶️ How to Run

Follow these steps to run the project end-to-end:

---

### 1. Prerequisites

Make sure you have:

* Python 3.8+
* MongoDB installed and running in VM Shell
* Required dataset files:

  * `summary.bson`
  * `IP-COUNTRY-REGION-CITY.BIN`

---

### 2. Install Dependencies

```bash
pip3 install pymongo pandas requests beautifulsoup4 tqdm IP2Location
```

---

### 3. Import Data into MongoDB

```bash
mongorestore --db countly summary.bson
```

Verify data:

```bash
mongosh
use countly
db.summary.countDocuments()
```

---

### 4. Run IP Location Processing

```bash
python3 process_ip.py
```

Output:

* MongoDB collection: `ip_location`
* File: `ip_locations.csv`

---

### 5. Run Product Data Pipeline

```bash
python3 product_pipeline.py
```

Output:

* File: `products.csv`

---

### 6. Validate Outputs

Check generated files:

```bash
ls
```

Preview data:

```bash
head ip_locations.csv
head products.csv
```

---

### 7. (Optional) Data Quality Check

```python
import pandas as pd

df_ip = pd.read_csv("ip_locations.csv")
df_product = pd.read_csv("products.csv")

print(df_ip.isnull().sum())
print(df_product.duplicated(subset=["product_id"]).sum())
```

---

### ✅ Expected Results

* ~284,000 IP records enriched with location data
* ~365 unique products with names and URLs
* Clean, deduplicated datasets ready for analysis

---

## 📊 Data Quality

### IP Location Data

* Total records: **284,021**
* Missing values:

  * ip: 0
  * country: 0
  * region: 1
  * city: 1
* Completeness: **>99.999%**

---

### Product Data

* Total products: **365**
* Duplicate product_id: **0**
* High-quality product name extraction

---

## ✅ Key Achievements

* Built a scalable pipeline avoiding MongoDB 16MB `distinct()` limitation
* Applied aggregation pipeline for large data processing
* Performed data enrichment and web scraping
* Ensured high data quality and deduplication
* Delivered structured datasets ready for analytics

---

## ⚠️ Challenges & Solutions

| Challenge                         | Solution                           |
| --------------------------------- | ---------------------------------- |
| MongoDB `distinct()` limit (16MB) | Replaced with aggregation pipeline |
| Missing collections               | Adapted to event-based schema      |
| Large dataset processing          | Used batch processing & streaming  |
| Web scraping failures             | Added headers & fallback parsing   |

---

## 🚀 Future Improvements

* Parallel crawling for faster performance
* Store processed data in BigQuery
* Automate pipeline using Airflow
* Build dashboards (Power BI / Tableau)
* Containerize using Docker

---

## 📁 Project Structure
```
glamira_project/
│
├── src/
│   ├── process_ip.py
│   ├── product_pipeline.py  
├── result/
│   ├── ip_locations.csv
│   ├── products.csv
├── data/
│   ├── IP-COUNTRY-REGION-CITY.BIN
│   ├── summary.bson
│   ├── summary.metadata.json
└── README.md
```

---

## 📌 Conclusion

This project demonstrates practical data engineering skills, including:

* Data ingestion and transformation
* Working with NoSQL databases
* Handling large-scale data processing constraints
* Data enrichment and web scraping
* Building reproducible data pipelines

---

## 👤 Author

Nguyen Hieu
Aspiring Data Engineer
