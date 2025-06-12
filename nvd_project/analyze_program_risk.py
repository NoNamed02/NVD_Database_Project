import sqlite3

def analyze_program_risk(program_keyword, version_keyword=None, db_path="nvd_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 조건 구성
    like_clause = f"%{program_keyword}%"
    if version_keyword:
        like_clause = f"%{program_keyword}%{version_keyword}%"

    query = '''
    SELECT id, baseScore, exploitabilityScore, description
    FROM cve_data
    WHERE vulnerableProducts LIKE ?
      AND baseScore IS NOT NULL
      AND exploitabilityScore IS NOT NULL
    '''
    cursor.execute(query, (like_clause,))
    rows = cursor.fetchall()

    if not rows:
        print("❗ 관련 취약점이 없습니다.")
        return

    total_score = 0
    for row in rows:
        cve_id, base, exploit, _ = row
        total_score += base * exploit

    average_score = round(total_score / len(rows), 2)

    print(f"\n[+] '{program_keyword}' ({version_keyword if version_keyword else '전체 버전'}) 관련 취약점 개수: {len(rows)}")
    print(f"[+] 평균 위험도 지수 (Base × Exploit): {average_score}\n")

    if average_score >= 20:
        print("🔴 이 버전은 매우 위험합니다!")
    elif average_score >= 10:
        print("🟠 보안 위협이 존재합니다. 업그레이드 검토 필요")
    elif average_score >= 5:
        print("🟡 낮은 수준의 위험이 있습니다.")
    else:
        print("🟢 보안 위험은 낮은 편입니다.")

    conn.close()

if __name__ == "__main__":
    program = input("제품 이름 또는 CPE 키워드 입력: ").lower()
    version = input("버전 (예: 1.2.3) [엔터로 생략]: ").strip()
    analyze_program_risk(program, version if version else None)
