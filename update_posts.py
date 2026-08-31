import urllib.request
import re

PAGE_ID = "100057555523595"
PLUGIN_URL = f"https://www.facebook.com/v18.0/plugins/page.php?href=https%3A%2F%2Fwww.facebook.com%2Fprofile.php%3Fid%3D{PAGE_ID}&tabs=timeline"

def get_fb_posts():
    req = urllib.request.Request(
        PLUGIN_URL, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    posts = []
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            fbids = re.findall(r'story_fbid=([a-zA-Z0-9_]+)', html)
            seen = set()
            for fbid in fbids:
                if fbid not in seen:
                    seen.add(fbid)
                    embed_url = f"https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2Fpermalink.php%3Fstory_fbid%3D{fbid}%26id%3D{PAGE_ID}&show_text=true&width=500"
                    posts.append(embed_url)
                if len(posts) >= 2:
                    break
    except Exception as e:
        print(f"抓取貼文失敗: {e}")
    
    return posts

def main():
    posts = get_fb_posts()
    
    # 預備預設連結（若抓取失敗時備用）
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
