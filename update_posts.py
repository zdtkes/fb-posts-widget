import urllib.request
import urllib.parse
import json
import re

PAGE_ID = "100057555523595"
RSS_URL = "https://fetchrss.com/feed/1x1JUGClSF2w1x1JTf5xPGeY.rss"
API_URL = f"https://api.rss2json.com/v1/api.json?rss_url={urllib.parse.quote(RSS_URL)}"

def get_latest_posts():
    posts = []
    try:
        req = urllib.request.Request(API_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            for item in data.get('items', [])[:5]:
                link = item.get('link', '')
                
                # 尋找貼文 ID (pfbid 或 story_fbid)
                fbid_match = re.search(r'story_fbid=([a-zA-Z0-9_]+)', link) or re.search(r'posts/([a-zA-Z0-9_]+)', link) or re.search(r'pfbid[a-zA-Z0-9]+', link)
                
                if fbid_match:
                    fbid = fbid_match.group(0) if 'pfbid' in fbid_match.group(0) else fbid_match.group(1)
                    embed_url = f"https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2Fpermalink.php%3Fstory_fbid%3D{fbid}%26id%3D{PAGE_ID}&show_text=true&width=500"
                    if embed_url not in posts:
                        posts.append(embed_url)
                elif link:
                    encoded_link = urllib.parse.quote(link, safe='')
                    embed_url = f"https://www.facebook.com/plugins/post.php?href={encoded_link}&show_text=true&width=500"
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
