import cloudscraper
from bs4 import BeautifulSoup
import re

def crawl_and_create_m3u():
    target_url = "https://khandaia2.me/trang-chu?type=football"
    filename = "playlist.m3u"
    
    # Giả lập trình duyệt thật để vượt rào cản
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    try:
        response = scraper.get(target_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = []

        # Phương pháp 1: Tìm tất cả nút "Xem" (giống trong ảnh Screenshot 83)
        # Các nút này thường nằm trong thẻ 'a' chứa chữ 'Xem'
        for a in soup.find_all('a', href=True):
            text = a.get_text().strip()
            link = a['href']
            
            if 'Xem' in text or '/match/' in link or '/truc-tiep/' in link:
                # Tìm tên trận đấu ở các thẻ cha xung quanh nút Xem
                parent = a.find_parent('div')
                title = parent.get_text(" ", strip=True) if parent else "Trận đấu"
                
                # Làm sạch tên (xóa chữ Xem, Hot, Giờ thi đấu để gọn hơn)
                title = title.replace("Xem", "").strip()
                
                if link.startswith('/'):
                    link = "https://khandaia2.me" + link
                
                if link not in [m['link'] for m in matches] and "http" in link:
                    matches.append({"title": title, "link": link})

        # Ghi file M3U
        with open(filename, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            if not matches:
                # Nếu vẫn không thấy, ghi lại mã lỗi để kiểm tra
                f.write(f"#EXTINF:-1, Website chan Robot hoac chua co lich - Code: {response.status_code}\nhttp://0.0.0.0\n")
            else:
                for m in matches:
                    f.write(f"#EXTINF:-1, {m['title']}\n{m['link']}\n")
        
        print(f"Da tim thay {len(matches)} tran.")

    except Exception as e:
        print(f"Loi: {e}")

if __name__ == "__main__":
    crawl_and_create_m3u()
