import cloudscraper
from bs4 import BeautifulSoup
import re

def crawl_and_create_m3u():
    # Cấu hình nguồn quét (Thay đổi link nếu trang web đổi domain)
    target_url = "https://khandaia2.me/" 
    filename = "playlist.m3u"
    
    # Khởi tạo scraper để vượt Cloudflare
    scraper = cloudscraper.create_scraper()
    
    try:
        print(f"Đang quét dữ liệu từ: {target_url}...")
        response = scraper.get(target_url)
        if response.status_code != 200:
            print("Không thể truy cập trang web.")
            return

        # Dùng BeautifulSoup để đọc nội dung HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Bước 1: Tìm các link trận đấu (Ví dụ: tìm các thẻ <a> có chứa từ 'truc-tiep')
        # Lưu ý: Mỗi trang có cấu trúc khác nhau, bạn có thể cần chỉnh sửa đoạn này
        matches = []
        for a in soup.find_all('a', href=True):
            if 'truc-tiep' in a['href'] or 'match' in a['href']:
                title = a.get_text(strip=True) or "Trận bóng đá"
                link = a['href']
                # Nếu link là link tương đối, hãy nối thêm domain
                if link.startswith('/'):
                    link = "https://khandaia2.me" + link
                matches.append({"title": title, "link": link})

        # Bước 2: Tạo nội dung file M3U
        # Định dạng chuẩn: #EXTM3U -> #EXTINF -> Link
        m3u_content = "#EXTM3U\n"
        
        if not matches:
            print("Không tìm thấy trận đấu nào.")
            # Tạo một kênh thông báo để biết script vẫn chạy nhưng web trống
            m3u_content += "#EXTINF:-1, Hiện chưa có trận đấu nào đang diễn ra\nhttp://0.0.0.0\n"
        else:
            for match in matches:
                # Bạn có thể thêm logo hoặc group-title nếu muốn
                m3u_content += f"#EXTINF:-1 group-title=\"Bóng Đá Trực Tiếp\", {match['title']}\n"
                m3u_content += f"{match['link']}\n"

        # Ghi nội dung ra file playlist.m3u
        with open(filename, "w", encoding="utf-8") as f:
            f.write(m3u_content)
            
        print(f"Đã cập nhật thành công {len(matches)} trận đấu vào {filename}")

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    crawl_and_create_m3u()
