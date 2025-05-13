# view_data.py
import sqlite3

def view_data(limit=10, severity_filter=None, order="DESC"):
    """ 데이터베이스에서 데이터 확인 """
    conn = sqlite3.connect('nvd_data.db')
    cursor = conn.cursor()

    query = "SELECT * FROM cve_data"
    params = []

    # Severity 필터링
    if severity_filter:
        query += " WHERE severity = ?"
        params.append(severity_filter)

    # 정렬 순서
    query += f" ORDER BY publishedDate {order}"

    # 데이터 개수 제한
    query += " LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    print("1. 전체 데이터 보기 (오래된 순서)")
    print("2. 전체 데이터 보기 (최신 순서)")
    print("3. 특정 Severity만 보기")
    print("4. 데이터 개수 지정해서 보기 (최신 순서)")

    choice = input("선택: ")

    if choice == "1":
        view_data(order="ASC")
    elif choice == "2":
        view_data(order="DESC")
    elif choice == "3":
        severity = input("Severity를 입력하세요 (e.g., CRITICAL): ").upper()
        view_data(severity_filter=severity, order="DESC")
    elif choice == "4":
        limit = int(input("몇 개의 데이터를 출력할까요? "))
        view_data(limit=limit, order="DESC")
    else:
        print("잘못된 선택입니다.")
