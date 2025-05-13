# download_and_populate.py
import requests
import gzip
import os
import json
import sqlite3

DB_NAME = 'nvd_data.db'

def download_nvd_data(year):
    """ NVD 데이터 다운로드 """
    url = f"https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-{year}.json.gz"
    filename = f"nvdcve-1.1-{year}.json.gz"
    
    print(f"Downloading {filename}...")
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"{filename} downloaded successfully.")
        return filename
    else:
        print(f"Failed to download data for {year}.")
        return None

def extract_gz(filename):
    """ 압축 해제 """
    json_filename = filename.replace(".gz", "")
    with gzip.open(filename, "rb") as gz_file:
        with open(json_filename, "wb") as json_file:
            json_file.write(gz_file.read())
    print(f"{filename} extracted to {json_filename}")
    return json_filename

def insert_data(data):
    """ 데이터베이스에 데이터 삽입 """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for item in data["CVE_Items"]:
        cve_id = item["cve"]["CVE_data_meta"]["ID"]
        published_date = item["publishedDate"]
        description = item["cve"]["description"]["description_data"][0]["value"]

        # Severity가 없는 경우 기본값 "UNKNOWN"
        severity = item.get("impact", {}).get("baseMetricV3", {}).get("cvssV3", {}).get("baseSeverity", "UNKNOWN")

        # 취약점 제품 정보 추출
        vulnerable_products = []
        for node in item["configurations"]["nodes"]:
            if "cpeMatch" in node:
                for match in node["cpeMatch"]:
                    vulnerable_products.append(match["cpe23Uri"])

        vulnerable_products_str = ", ".join(vulnerable_products)

        # 데이터 삽입
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO cve_data (id, publishedDate, description, severity, vulnerableProducts)
                VALUES (?, ?, ?, ?, ?)
            ''', (cve_id, published_date, description, severity, vulnerable_products_str))
        except sqlite3.IntegrityError:
            print(f"Duplicate entry for {cve_id}. Skipping...")
    
    conn.commit()
    conn.close()
    print("Data inserted successfully.")

def read_json(file_path):
    """ JSON 파일 읽기 """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def process_year(year):
    """ 연도별 데이터 처리 """
    gz_file = download_nvd_data(year)
    if gz_file:
        json_file = extract_gz(gz_file)
        data = read_json(json_file)
        insert_data(data)

def main():
    start_year = int(input("Enter start year (e.g., 2002): "))
    end_year = int(input("Enter end year (e.g., 2025): "))

    for year in range(start_year, end_year + 1):
        print(f"\nProcessing data for year: {year}")
        process_year(year)

if __name__ == "__main__":
    main()
