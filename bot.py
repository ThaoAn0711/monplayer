import requests

def crawl_and_create_m3u():
    filename = "playlist.m3u"
    # Nguồn dự phòng ổn định
    api_url = "https://raw.githubusercontent.com/thanhduong/football-links/main/links.json"
    m3u_content = "#EXTM3U\n"
    count = 0  # Gán giá trị ngay từ đầu để tránh lỗi "referenced before assignment"

    try:
        response = requests.get(api_url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            for match in data:
                title = match.get('name', 'Trận đấu')
                link = match.get('link', '')
                if link:
                    m3u_content += f"#EXTINF:-1, {title}\n{link}\n"
                    count += 1
            
            if count == 0:
                m3u_content += "#EXTINF:-1, Hien tai chua co lich moi\nhttp://0.0.0.0\n"
        else:
            m3u_content += f"#EXTINF:-1, Loi ket noi nguon: {response.status_code}\nhttp://0.0.0.0\n"

    except Exception as e:
        m3u_content += f"#EXTINF:-1, Loi he thong: {str(e)}\nhttp://0.0.0.0\n"

    # Ghi file bất kể có lỗi hay không để MonPlayer không bị trống
    with open(filename, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print(f"Hoan thanh: Tim thay {count} tran.")

if __name__ == "__main__":
    crawl_and_create_m3u()
