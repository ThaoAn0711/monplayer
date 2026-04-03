import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://khandaia2.me"

def get_m3u8():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # bật log network
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(URL)
    time.sleep(15)

    logs = driver.get_log("performance")

    driver.quit()

    for log in logs:
        message = json.loads(log["message"])["message"]

        if message["method"] == "Network.responseReceived":
            url = message["params"]["response"]["url"]

            if ".m3u8" in url:
                return url

    return None


def create_m3u(link):
    if not link:
        link = "http://0.0.0.0"

    content = "#EXTM3U\n"
    content += f'#EXTINF:-1 group-title="Khandaia",Live\n{link}\n'

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(content)


def main():
    print("🔍 Bắt m3u8 từ network...")

    link = get_m3u8()

    if link:
        print("✅ Lấy được m3u8:", link)
    else:
        print("❌ Không lấy được")

    create_m3u(link)


if __name__ == "__main__":
    main()
