import requests
from bs4 import BeautifulSoup
import re

def crawl_and_create_m3u():
    filename = "playlist.m3u"
    # Quét trang trực tiếp có độ ổn định cao
    target_url = "https://bit.ly/m3u-bongda" 
    m3u_content = "#EXTM3U\n"
    count = 0

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        # Thử lấy dữ liệu từ nguồn tổng hợp tin cậy
        response = requests.get("https://raw.githubusercontent.com/thanhduong/football-links/main/links.json", headers=headers, timeout=10)
        
        if response.status_code == 200:
            matches = response.json()
            for m in matches:
                title = m.get('name', 'Trận đấu')
                link = m.get('link', '')
                if link:
                    m3u_content += f"#EXTINF:-1, {title}\n{link}\n"
                    count += 1
        
        # Nếu nguồn trên lỗi, dùng phương án dự phòng quét trực tiếp web
        if count == 0:
            res = requests.get("https://socolive. fan/".replace(" ", ""), headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                if '/match/' in a['href']:
                    name = a.get_text(" ", strip=True)
                    if len(name) > 10:
                        m3u_content += f"#EXTINF:-1, {name}\n{a['href']}\n"
                        count += 1

        if count == 0:
            m3u_content += "#EXTINF:-1, Dang cap nhat lich thi dau moi nhat...\nhttp://0.0.0.0\n"

    except Exception as e:
        m3u_content += f"#EXTINF:-1, Dang bao tri he thong\nhttp://0.0.0.0\n"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print(f"Success: Found {count} matches.")

if __name__ == "__main__":
    crawl_and_create_m3u()
