import requests
from bs4 import BeautifulSoup
import re

# URL trang chủ
BASE_URL = "https://khandaia2.me"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_match_links():
    res = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/truc-tiep" in href or "/match" in href:
            if href.startswith("/"):
                href = BASE_URL + href
            links.append(href)

    return list(set(links))[:5]  # lấy 5 trận


def extract_m3u8(url):
    try:
        res = requests.get(url, headers=HEADERS)
        html = res.text

        # tìm iframe trước
        iframe = re.search(r'<iframe.*?src="(.*?)"', html)
        if iframe:
            iframe_url = iframe.group(1)
            if iframe_url.startswith("//"):
                iframe_url = "https:" + iframe_url

            res = requests.get(iframe_url, headers=HEADERS)
            html = res.text

        # tìm m3u8
        m3u8 = re.search(r'https?://[^\s"\']+\.m3u8', html)
        if m3u8:
            return m3u8.group(0)

    except Exception as e:
        print("Error:", e)

    return None


def create_m3u(channels):
    content = "#EXTM3U\n"

    for name, link in channels:
        content += f'#EXTINF:-1 group-title="Khandaia",{name}\n{link}\n'

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(content)


def main():
    print("🔍 Đang lấy danh sách trận...")

    matches = get_match_links()
    channels = []

    for i, link in enumerate(matches):
        print(f"🎯 Đang xử lý: {link}")

        m3u8 = extract_m3u8(link)
        if m3u8:
            channels.append((f"Match {i+1}", m3u8))
            print("✅ Lấy được m3u8")
        else:
            print("❌ Không có m3u8")

    if channels:
        create_m3u(channels)
        print("🔥 Đã tạo playlist.m3u")
    else:
        print("❌ Không lấy được link nào")


if __name__ == "__main__":
    main()
