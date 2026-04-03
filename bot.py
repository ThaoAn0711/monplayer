import requests
import re

BASE = "https://khandaia2.me"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_match():
    html = requests.get(BASE, headers=headers).text

    matches = re.findall(r'href="(https://khandaia2.me/[^"]+truc-tiep[^"]+)"', html)

    if matches:
        return matches[0]
    return None


def get_m3u8(url):
    html = requests.get(url, headers=headers).text

    # tìm iframe
    iframe = re.search(r'<iframe.*?src="([^"]+)"', html)
    if iframe:
        iframe_url = iframe.group(1)

        print("👉 iframe:", iframe_url)

        iframe_html = requests.get(iframe_url, headers=headers).text

        m3u8 = re.search(r'https://[^"]+\.m3u8[^"]*', iframe_html)
        if m3u8:
            return m3u8.group(0)

    # fallback tìm trực tiếp
    m3u8 = re.search(r'https://[^"]+\.m3u8[^"]*', html)
    if m3u8:
        return m3u8.group(0)

    return None


def save(link):
    if not link:
        link = "http://0.0.0.0"

    with open("playlist.m3u", "w") as f:
        f.write("#EXTM3U\n")
        f.write('#EXTINF:-1 group-title="Khandaia",Live\n')
        f.write(link)


def main():
    print("🔍 Tìm trận...")

    match = get_match()

    if not match:
        print("❌ Không có trận")
        save(None)
        return

    print("🎯 Trận:", match)

    link = get_m3u8(match)

    if link:
        print("✅ M3U8:", link)
    else:
        print("❌ Không có m3u8")

    save(link)


if __name__ == "__main__":
    main()
