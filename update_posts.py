import urllib.request
import urllib.parse
import json
import re

PAGE_ID = "100057555523595"
RSS_URL = "https://fetchrss.com/feed/1x1JUGClSF2w1x1JTf5xPGeY.rss"
API_URL = f"https://api.rss2json.com/v1/api.json?rss_url={urllib.parse.quote(RSS_URL)}"

def clean_fb_url(url):
    """清理 FB 網址，去除 RSS 夾帶的追蹤參數（如 ?ref=... 或 &__tn__=...）"""
    if not url:
        return ""
    if 'permalink.php' in url:
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        story_fbid = params.get('story_fbid', [''])[0]
        page_id = params.get('id', [PAGE_ID])[0]
        if story_fbid:
            return f"https://www.facebook.com/permalink.php?story_fbid={story_fbid}&id={page_id}"
    
    # 一般網址去除問號後面的追蹤參數
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
                
                # 1. 擴充正則表達式：支援 pfbid, story_fbid, posts, videos, reel
                fbid_match = (
                    re.search(r'pfbid[a-zA-Z0-9]+', link) or 
                    re.search(r'story_fbid=([a-zA-Z0-9_]+)', link) or 
                    re.search(r'posts/([a-zA-Z0-9_]+)', link) or
                    re.search(r'videos/([0-9]+)', link) or
                    re.search(r'reel/([0-9]+)', link)
                )
                
                # 2. 統一轉換為標準 permalink 格式，強制 FB 渲染文字與貼文內容
                if fbid_match:
                    fbid = fbid_match.group(0) if 'pfbid' in fbid_match.group(0) else fbid_match.group(1)
                    target_url = f"https://www.facebook.com/permalink.php?story_fbid={fbid}&id={PAGE_ID}"
                else:
                    target_url = clean_fb_url(link)

                # 3. 確保 show_text=true 正確帶入且 href 經過乾淨編碼
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
    
    default_post_1 = "https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2Fpermalink.php%3Fstory_fbid%3Dpfbid0g415rmcwx6FwxnqWUrERRA91D9X4E7M4MDQGUrK5burFDQ5MEsFMu3yJxiT89rwl%26id%3D100057555523595&show_text=true&width=500"
    default_post_2 = "https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2Fpermalink.php%3Fstory_fbid%3Dpfbid06gfFHvUoW6P5iJw8tqpWaurEozeGdovCA8Rm26CjNTaZ6628e7ZFW81W6x8aP7wml%26id%3D100057555523595&show_text=true&width=500"

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
