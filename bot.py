import requests

def crawl_and_create_m3u():
    filename = "playlist.m3u"
    # Nguồn API cộng đồng ổn định hơn
    target_url = "https://raw.githubusercontent.com/biem9x/m3u/main/sport.json"
    m3u_content = "#EXTM3U\n"
    count = 0

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
        response = requests.get(target_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # Cấu trúc nguồn này thường là danh sách các kênh/trận đấu
            for item in data:
                title = item.get('name') or item.get('title')
                link = item.get('url') or item.get('link')
                
                if title and link:
                    m3u_content += f"#EXTINF:-1, {title}\n{link}\n"
                    count += 1
            
            if count == 0:
                m3u_content += "#EXTINF:-1, Dang cap nhat lich thi dau...\nhttp://0.0.0.0\n"
        else:
            # Nếu nguồn này lỗi, thử nguồn dự phòng 2
            m3u_content += f"#EXTINF:-1, Nguồn đang bảo trì ({response.status_code})\nhttp://0.0.0.0\n"

    except Exception as e:
        m3u_content += f"#EXTINF:-1, Loi he thong: {str(e)}\nhttp://0.0.0.0\n"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print(f"Hoan thanh: Lay duoc {count} kenh/tran dau.")

if __name__ == "__main__":
    crawl_and_create_m3u()
