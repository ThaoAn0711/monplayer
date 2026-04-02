import cloudscraper
from bs4 import BeautifulSoup
import re

def crawl_and_create_m3u():
    target_url = "https://khandaia2.me/" 
    filename = "playlist.m3u"
    scraper = cloudscraper.create_scraper()
    
    try:
        print(f"Đang quét dữ liệu từ: {target_url}...")
        response = scraper.get(target_url)
        if response.status_code != 200:
            print("Không thể truy cập trang web.")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        matches = []
        for a in soup.find_all('a', href=True):
            if 'truc-tiep' in a['href'] or 'match' in a['href']:
                title = a.get_text(strip=True) or "Trận bóng đá"
                link = a['href']
                if link.startswith('/'):
                    link = "https://khandaia2.me" + link
                matches.append({"title": title, "link": link})

        m3u_content = "#EXTM3U\n"
        if not matches:
            m3u_content += "#EXTINF:-1, Hiện chưa có trận đấu nào\nhttp://0.0.0.0\n"
        else:
            for match in matches:
                m3u_content += f"#EXTINF:-1, {match['title']}\n{match['link']}\n"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("Cập nhật thành công!")

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    crawl_and_create_m3u()
