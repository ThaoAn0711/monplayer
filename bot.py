import requests
import re

def get_m3u8():
    url = "https://khandaia2.me"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    html = requests.get(url, headers=headers).text

    # tìm link m3u8 trực tiếp
    match = re.search(r'https://[^"]+\.m3u8[^"]*', html)

    if match:
        return match.group(0)

    return None


def save(link):
    if not link:
        link = "http://0.0.0.0"

    with open("playlist.m3u", "w") as f:
        f.write("#EXTM3U\n")
        f.write('#EXTINF:-1 group-title="Khandaia",Live\n')
        f.write(link)


def main():
    print("🔍 Đang lấy m3u8...")

    link = get_m3u8()

    if link:
        print("✅ FOUND:", link)
    else:
        print("❌ NOT FOUND")

    save(link)


if __name__ == "__main__":
    main()
