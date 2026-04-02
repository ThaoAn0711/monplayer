import cloudscraper
from bs4 import BeautifulSoup
import random

def crawl_and_create_m3u():
    # Sử dụng URL cơ bản để tránh bị soi
    target_url = "https://khandaia2.me/" 
    filename = "playlist.m3u"
    
    # Danh sách các User-Agent để giả lập các trình duyệt khác nhau
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    ]

    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    try:
        # Gửi kèm Headers giống người dùng thật
        headers = {'User-Agent': random.choice(user_agents)}
        response = scraper.get(target_url, headers=headers, timeout=20)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = []

        # Quét tất cả link có khả năng là trận đấu
        for a in soup.find_all('a', href=True):
            link = a['href']
            # Kiểm tra nếu link chứa các từ khóa trận đấu
            if any(k in link for k in ['/match/', '/truc-tiep/', '/xem-tran/']):
                title = a.get_text(" ", strip=True)
                
                # Nếu text trong thẻ a quá ngắn, lấy text của thẻ cha
                if len(title) < 10:
                    parent = a.find_parent('div')
                    title = parent.get_text(" ", strip=True) if parent else "Trận đấu bóng đá"
                
                # Xử lý link tuyệt đối
                if link.startswith('/'):
                    link = "https://khandaia2.me" + link
                
                # Loại bỏ các ký tự rác trong title
                title = title.replace("HOT", "").replace("Xem", "").strip()
                
                if link not in [m['link'] for m in matches]:
                    matches.append({"title": title, "link": link})

        # Ghi file M3U
        with open(filename, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            if not matches:
                f.write(f"#EXTINF:-1, Web van chan (Code: {response.status_code}) - Thu lai sau\nhttp://0.0.0.0\n")
            else:
                for m in matches:
                    f.write(f"#EXTINF:-1, {m['title']}\n{m['link']}\n")
        
        print(f"Thành công! Tìm thấy {len(matches)} trận.")

    except Exception as e:
        print(f"Lỗi hệ thống: {e}")

if __name__ == "__main__":
    crawl_and_create_m3u()
