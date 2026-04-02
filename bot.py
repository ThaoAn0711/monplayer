import requests
import re

def crawl_and_create_m3u():
    filename = "playlist.m3u"
    # Nguồn dữ liệu bóng đá thay thế từ vebo (thường ít chặn hơn)
    target_url = "https://api.vebo.xyz/api/match/featured"
    m3u_content = "#EXTM3U\n"
    count = 0

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(target_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # Duyệt qua danh sách trận đấu từ API
            matches = data.get('data', [])
            for match in matches:
                home = match.get('home', {}).get('name', 'Team A')
                away = match.get('away', {}).get('name', 'Team B')
                slug = match.get('slug', '')
                
                if slug:
                    title = f"{home} vs {away}"
                    # Tạo link xem (giả định cấu trúc link của vebo)
                    link = f"https://vebo.xyz/truc-tiep/{slug}"
                    m3u_content += f"#EXTINF:-1, {title}\n{link}\n"
                    count += 1
            
            if count == 0:
                m3u_content += "#EXTINF:-1, Chua co lich thi dau hom nay\nhttp://0.0.0.0\n"
        else:
            m3u_content += f"#EXTINF:-1, Nguon tam thoi bao tri (Code: {response.status_code})\nhttp://0.0.0.0\n"

    except Exception as e:
        m3u_content += f"#EXTINF:-1, Loi he thong: {str(e)}\nhttp://0.0.0.0\n"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print(f"Thành công: Đã cập nhật {count} trận đấu.")

if __name__ == "__main__":
    crawl_and_create_m3u()
