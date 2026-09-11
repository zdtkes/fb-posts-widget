import urllib.request
import urllib.parse
import json

PAGE_ID = "100057555523595"
RSS_URL = "https://fetchrss.com/feed/1x1JUGClSF2w1x1JTf5xPGeY.rss"
API_URL = f"https://api.rss2json.com/v1/api.json?rss_url={urllib.parse.quote(RSS_URL)}"

def clean_fb_url(url):
    """清理 FB 網址，切除 RSS 附帶的追蹤參數"""
    if not url:
        return ""
    return url.split('?')[0]

def get_latest_posts():
    posts = []
    try:
        req = urllib.request.Request(API_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            for item in data.get('items', []):
                link = item.get('link', '')
                if not link:
                    continue
                
                target_url = clean_fb_url(link)
                
                # 多重檢查：從網址、標題、描述與附件判斷是否為影片/Reel貼文
                title = str(item.get('title', '')).lower()
                desc = str(item.get('description', '')).lower()
                enclosure = str(item.get('enclosure', '')).lower()
                link_lower = target_url.lower()
                
                video_keywords = ['video', 'videos', 'reel', 'reels', 'watch', 'mp4', '影片', '播放']
                is_video = any(k in link_lower or k in title or k in desc or k in enclosure for k in video_keywords)
                
                encoded_href = urllib.parse.quote(target_url, safe='')
                embed_url = f"https://www.facebook.com/plugins/post.php?href={encoded_href}&show_text=true&width=500"

                post_data = {
                    'url': embed_url,
                    'is_video': is_video
                }

                if not any(p['url'] == embed_url for p in posts):
                    posts.append(post_data)

                if len(posts) >= 2:
                    break
    except Exception as e:
        print(f"抓取 RSS 失敗: {e}")
    
    return posts

def main():
    posts = get_latest_posts()
    
    default_1 = {
        'url': "https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2F100057555523595%2Fposts%2Fpfbid0g415rmcwx6FwxnqWUrERRA91D9X4E7M4MDQGUrK5burFDQ5MEsFMu3yJxiT89rwl&show_text=true&width=500",
        'is_video': False
    }
    default_2 = {
        'url': "https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2F100057555523595%2Fposts%2Fpfbid06gfFHvUoW6P5iJw8tqpWaurEozeGdovCA8Rm26CjNTaZ6628e7ZFW81W6x8aP7wml&show_text=true&width=500",
        'is_video': False
    }

    p1 = posts[0] if len(posts) > 0 else default_1
    p2 = posts[1] if len(posts) > 1 else default_2

    # 貼文高度設定：影片貼文手機版降至 340px（無空白），圖文貼文為 580px
    h1_desk = "500px" if p1['is_video'] else "650px"
    h1_mob  = "340px" if p1['is_video'] else "580px"
    
    h2_desk = "500px" if p2['is_video'] else "650px"
    h2_mob  = "340px" if p2['is_video'] else "580px"

    with open("template.html", "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace("__FB_POST_1__", p1['url'])
    content = content.replace("__FB_POST_1_HEIGHT_DESK__", h1_desk)
    content = content.replace("__FB_POST_1_HEIGHT_MOB__", h1_mob)
    
    content = content.replace("__FB_POST_2__", p2['url'])
    content = content.replace("__FB_POST_2_HEIGHT_DESK__", h2_desk)
    content = content.replace("__FB_POST_2_HEIGHT_MOB__", h2_mob)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("index.html 已成功更新！")

if __name__ == "__main__":
    main()
