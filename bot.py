import requests
import re

def get_m3u8():
    html = requests.get("https://khandaia2.me").text
    match = re.search(r'https://[^"]+\.m3u8[^"]*', html)
    return match.group(0) if match else None

def main():
    link = get_m3u8() or "http://0.0.0.0"

    with open("playlist.m3u", "w") as f:
        f.write("#EXTM3U\n")
        f.write('#EXTINF:-1 group-title="Khandaia",Live\n')
        f.write(link)

if __name__ == "__main__":
    main()
