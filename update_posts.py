import urllib.request
import urllib.parse
import json

PAGE_ID = "100057555523595"
RSS_URL = "https://fetchrss.com/feed/1x1JUGClSF2w1x1JTf5xPGeY.rss"
API_URL = f"https://api.rss2json.com/v1/api.json?rss_url={urllib.parse.quote(RSS_URL)}"

def clean_fb_url(url):
    """清理 FB 網址，切除 RSS 附帶的追蹤參數（如 ?ref=embed、&__tn__=...），保留最原始乾淨的貼文連結"""
    if not url:
        return ""
    # 取問號前的主網址，避免雜訊參數干擾 FB 外掛解析
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
                
                # 取得乾淨的 FB 原始連結
                target_url = clean_fb_url(link)

                # 將乾淨連結編碼後帶入 FB 官方 post.php 外掛
                encoded_href = urllib.parse.quote(target_url, safe='')
                embed_url = f"https://www.facebook.com/plugins/post.php?href={encoded_href}&show_text=true&width=500"

                if embed_url not in posts:
                    posts.append(embed_url)

                if len(posts) >= 2:
                    break
    except Exception as e:
        print(f"抓取 RSS 失敗: {e}")
    
    return posts

def main():
    posts = get_latest_posts()
    
    default_post_1 = "https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2F100057555523595%2Fposts%2Fpfbid0g415rmcwx6FwxnqWUrERRA91D9X4E7M4MDQGUrK5burFDQ5MEsFMu3yJxiT89rwl&show_text=true&width=500"
    default_post_2 = "https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2F100057555523595%2Fposts%2Fpfbid06gfFHvUoW6P5iJw8tqpWaurEozeGdovCA8Rm26CjNTaZ6628e7ZFW81W6x8aP7wml&show_text=true&width=500"

    post_1 = posts[0] if len(posts) > 0 else default_post_1
    post_2 = posts[1] if len(posts) > 1 else default_post_2

    with open("template.html", "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace("__FB_POST_1__", post_1)
    content = content.replace("__FB_POST_2__", post_2)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("index.html 已成功更新！")

if __name__ == "__main__":
    main()
