from datetime import datetime
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

def read_json(file_path):
    """ JSON 파일 읽기 """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def insert_data(data):
    """ 데이터베이스에 데이터 삽입 """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for item in data["CVE_Items"]:
        cve_id = item["cve"]["CVE_data_meta"]["ID"]
        published_date = item["publishedDate"]
        description = item["cve"]["description"]["description_data"][0]["value"]

        # 기본 값
        severity = "UNKNOWN"
        base_score = None
        exploitability_score = None
        impact_score = None
        attack_vector = None
        attack_complexity = None

        # CVSS v3 데이터 존재 시 추출
        if "impact" in item and "baseMetricV3" in item["impact"]:
            bm = item["impact"]["baseMetricV3"]
            cvss = bm.get("cvssV3", {})
            base_score = cvss.get("baseScore")
            severity = cvss.get("baseSeverity", "UNKNOWN")
            exploitability_score = bm.get("exploitabilityScore")
            impact_score = bm.get("impactScore")
            attack_vector = cvss.get("attackVector")
            attack_complexity = cvss.get("attackComplexity")

        # 취약 제품 목록
        vulnerable_products = []
        for node in item.get("configurations", {}).get("nodes", []):
            for match in node.get("cpeMatch", []):
                vulnerable_products.append(match["cpe23Uri"])
        vulnerable_products_str = ", ".join(vulnerable_products)

        # 삽입 쿼리
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO cve_data (
                    id, publishedDate, description, severity, vulnerableProducts,
                    baseScore, exploitabilityScore, impactScore, attackVector, attackComplexity
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                cve_id, published_date, description, severity, vulnerable_products_str,
                base_score, exploitability_score, impact_score, attack_vector, attack_complexity
            ))
        except sqlite3.IntegrityError:
            print(f"Duplicate entry for {cve_id}. Skipping...")

    conn.commit()
    conn.close()
    print("Data inserted successfully.")

def process_year(year):
    """ 연도별 데이터 처리 """
    gz_file = download_nvd_data(year)
    if gz_file:
        json_file = extract_gz(gz_file)
        data = read_json(json_file)
        insert_data(data)

# 아래 main()은 자동 실행을 위한 용도는 아님 (auto_update.py에서 호출됨)
if __name__ == "__main__":
    for y in range(2002, datetime.now().year + 1):
        process_year(y)
