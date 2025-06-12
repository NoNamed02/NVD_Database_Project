import time
import threading
from datetime import datetime
from download_and_populate import process_year
import logging

# 로그 설정
logging.basicConfig(
    filename='nvd_update.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

last_update_date = None  # 중복 방지를 위한 날짜 저장

def update_all_data():
    current_year = datetime.now().year
    for year in range(2002, current_year + 1):
        logging.info(f"[+] Processing NVD data for {year}")
        try:
            process_year(year)
        except Exception as e:
            logging.error(f"Failed to process data for {year}: {e}")
    logging.info("[+] All data updated.\n")

def wait_until_midnight():
    global last_update_date
    while True:
        now = datetime.now()
        # 자정(00:00)에 하루 한 번만 실행
        if now.hour == 0 and now.minute == 0:
            if last_update_date != now.date():
                logging.info("[*] Midnight reached. Starting DB update...")
                update_all_data()
                last_update_date = now.date()
        time.sleep(30)  # 30초마다 확인

def main():
    logging.info("[*] Initial data update on program start...")
    update_all_data()
    logging.info("[*] Waiting for midnight to auto-update...")

    # 자정 대기 스레드 시작
    threading.Thread(target=wait_until_midnight, daemon=True).start()

    # 메인 스레드는 대기
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
