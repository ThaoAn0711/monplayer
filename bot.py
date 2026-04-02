import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

URL = "https://khandaia2.me"

def get_m3u8():
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service('/usr/bin/chromedriver'),
        options=options
    )

    driver.get(URL)
    time.sleep(20)

    html = driver.page_source
    driver.quit()

    match = re.search(r'https?://[^\s"\']+\.m3u8', html)
    if match:
        return match.group(0)

    return None


def create_m3u(link):
    if not link:
        link = "http://0.0.0.0"

    content = "#EXTM3U\n"
    content += f'#EXTINF:-1 group-title="Khandaia",Live\n{link}\n'

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(content)


def main():
    print("🔍 Đang lấy m3u8...")

    link = get_m3u8()

    if link:
        print("✅ Lấy được:", link)
    else:
        print("❌ Không lấy được")

    create_m3u(link)


if __name__ == "__main__":
    main()
