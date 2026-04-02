import cloudscraper
from bs4 import BeautifulSoup
import re

def crawl_and_create_m3u():
    target_url = "https://khandaia2.me/trang-chu?type=football"
    filename = "playlist.m3u"
    scraper = cloudscraper.create_scraper()
    
    try:
        response = scraper.get(target_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = []

        # Tìm tất cả các thẻ 'a' (đường dẫn) trên trang
        for a in soup.find_all('a', href=True):
            link = a['href']
            
            # Chỉ lấy các link có cấu trúc trận đấu (match, truc-tiep, hoặc xem-tran)
            if any(keyword in link for keyword in ['/match/', '/truc-tiep/', 'xem-tran']):
                # Lấy tên trận đấu từ thẻ chứa nó
                title = a.get_text(" ", strip=True)
                
                # Nếu không có chữ, thử tìm trong thẻ lân cận
                if len(title) < 5:
                    parent = a.find_parent()
                    title = parent.get_text(" ", strip=True) if parent else "Trận đấu bóng đá"

                # Chuẩn hóa link
                if link.startswith('/'):
                    link = "https://khandaia2.me" + link
                
                # Xóa các khoảng trắng thừa và ký tự lạ
                title = re.sub(r'\s+', ' ', title).strip()
                
                if link not in [m['link'] for m in matches]:
                    matches.append({"title": title, "link": link})

        # Ghi file M3U
        with open(filename, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            if not matches:
                # Nếu vẫn không thấy, ghi log để kiểm tra
                f.write(f"#EXTINF:-1, Khong tim thay tran nao luc {response.status_code}\nhttp://0.0.0.0\n")
            else:
                for m in matches:
                    f.write(f"#EXTINF:-1, {m['title']}\n{m['link']}\n")
        
        print(f"Da tim thay {len(matches)} tran dau.")

    except Exception as e:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"#EXTM3U\n#EXTINF:-1, Loi script: {str(e)}\nhttp://0.0.0.0\n")

if __name__ == "__main__":
    crawl_and_create_m3u()
