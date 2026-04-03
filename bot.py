import time
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://khandaia2.me"

def get_m3u8():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # bật bắt network
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(URL)
    time.sleep(15)

    # lấy log network
    logs = driver.get_log("performance")
    driver.quit()

    for log in logs:
        try:
            message = json.loads(log["message"])["message"]

            if message["method"] == "Network.responseReceived":
                url = message["params"]["response"]["url"]

                if ".m3u8" in url:
                    return url
        except:
            continue

    return None


def create_m3u(link):
    if not link:
        link = "http://0.0.0.0"

    content = "#EXTM3U\n"
    content += f'#EXTINF:-1 group-title="Khandaia",Live\n{link}\n'

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(content)


def main():
    print("🔍 Đang lấy m3u8 từ network...")

    try:
        link = get_m3u8()
    except Exception as e:
        print("❌ Lỗi:", e)
        link = None

    if link:
        print("✅ Lấy được:", link)
    else:
        print("❌ Không lấy được m3u8")

    create_m3u(link)


if __name__ == "__main__":
    main()
