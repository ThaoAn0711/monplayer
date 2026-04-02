import requests
import json

def crawl_and_create_m3u():
    filename = "playlist.m3u"
    # Sử dụng nguồn dữ liệu thay thế ổn định hơn
    api_url = "https://raw.githubusercontent.com/thanhduong/football-links/main/links.json"
    
    try:
        response = requests.get(api_url, timeout=15)
        m3u_content = "#EXTM3U\n"
        
        if response.status_code == 200:
            data = response.json()
            count = 0
            for match in data:
                title = match.get('name', 'Trận đấu')
                link = match.get('link', '')
                if link:
                    m3u_content += f"#EXTINF:-1, {title}\n{link}\n"
                    count += 1
            
            if count == 0:
                m3u_content += "#EXTINF:-1, Chua co lich thi dau moi\nhttp://0.0.0.0\n"
        else:
            m3u_content += f"#EXTINF:-1, Loi ket noi nguon du lieu ({response.status_code})\nhttp://0.0.0.0\n"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print(f"Hoàn thành! Đã tạo danh sách với {count} trận đấu.")

    except Exception as e:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"#EXTM3U\n#EXTINF:-1, Loi: {str(e)}\nhttp://0.0.0.0\n")

if __name__ == "__main__":
    crawl_and_create_m3u()
