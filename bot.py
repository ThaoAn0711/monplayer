import cloudscraper
from bs4 import BeautifulSoup

def crawl_and_create_m3u():
    # URL chính xác từ ảnh của bạn
    target_url = "https://khandaia2.me/trang-chu?type=football" 
    filename = "playlist.m3u"
    scraper = cloudscraper.create_scraper()
    
    try:
        response = scraper.get(target_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = []

        # Tìm tất cả các thẻ chứa thông tin trận đấu
        # Dựa trên ảnh, các link thường nằm trong thẻ 'a' có chứa href dẫn đến trận đấu
        for a in soup.find_all('a', href=True):
            href = a['href']
            # Lọc các link dẫn đến chi tiết trận đấu
            if '/match/' in href or '/truc-tiep/' in href:
                # Lấy tên trận đấu từ các thẻ text bên trong (Team A vs Team B)
                title = a.get_text(separator=" ", strip=True)
                if not title: title = "Trận đấu bóng đá"
                
                link = href
                if link.startswith('/'):
                    link = "https://khandaia2.me" + link
                
                # Tránh trùng lặp link
                if not any(m['link'] == link for m in matches):
                    matches.append({"title": title, "link": link})

        # Tạo nội dung file M3U
        m3u_content = "#EXTM3U\n"
        if not matches:
            m3u_content += "#EXTINF:-1, Hiện chưa có trận đấu nào (Quét lúc 15:35)\nhttp://0.0.0.0\n"
        else:
            for match in matches:
                m3u_content += f"#EXTINF:-1, {match['title']}\n{match['link']}\n"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print(f"Thành công: Đã tìm thấy {len(matches)} trận đấu!")

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    crawl_and_create_m3u()
