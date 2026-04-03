import time
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://khandaia2.me"

def get_match_link(driver):
    driver.get(BASE_URL)
    time.sleep(5)

    links = driver.find_elements("tag name", "a")

    for link in links:
        href = link.get_attribute("href")
        if href and "truc-tiep" in href:
            return href

    return None


def get_m3u8(match_url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    print("🎯 Vào trận:", match_url)

    driver.get(match_url)
    time.sleep(15)

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
    print("🔍 Đang tìm trận...")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    match_url = get_match_link(driver)
    driver.quit()

    if not match_url:
        print("❌ Không tìm thấy trận")
        create_m3u(None)
        return

    link = get_m3u8(match_url)

    if link:
        print("✅ M3U8:", link)
    else:
        print("❌ Không lấy được m3u8")

    create_m3u(link)


if __name__ == "__main__":
    main()
