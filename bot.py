import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL = "https://khandaia2.me"

def get_m3u8():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(URL)
    time.sleep(5)

    # lấy toàn bộ HTML sau khi JS chạy
    html = driver.page_source

    driver.quit()

    # tìm m3u8
    match = re.search(r'https?://[^\s"\']+\.m3u8', html)
    if match:
        return match.group(0)

    return None


def create_m3u(link):
    content = "#EXTM3U\n"
    content += f'#EXTINF:-1 group-title="Khandaia",Live\n{link}\n'

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(content)


def main():
    print("🔍 Đang lấy m3u8...")

    link = get_m3u8()

    if link:
        print("✅ Lấy được:", link)
        create_m3u(link)
    else:
        print("❌ Không lấy được m3u8")


if __name__ == "__main__":
    main()
