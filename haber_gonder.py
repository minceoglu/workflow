import feedparser
import pywhatkit
import time
import os

RSS_URL = 'https://bianet.org/rss/bianet'
SEEN_POSTS_FILE = 'gonderilen_haberler.txt'
WHATSAPP_GROUP_NAME = 'bianet'  # WhatsApp Web'de göründüğü şekliyle yaz

if os.path.exists(SEEN_POSTS_FILE):
    with open(SEEN_POSTS_FILE, 'r', encoding='utf-8') as file:
        seen_posts = set(file.read().splitlines())
else:
    seen_posts = set()

feed = feedparser.parse(RSS_URL)
new_posts = [entry for entry in feed.entries if entry.link not in seen_posts]

if new_posts:
    print(f"{len(new_posts)} yeni haber bulundu.")
    for post in reversed(new_posts):
        mesaj = f"{post.title}\n{post.link}"
        simdi = time.localtime()
        saat = simdi.tm_hour
        dakika = simdi.tm_min + 1
        if dakika >= 60:
            dakika -= 60
            saat = (saat + 1) % 24

        try:
            pywhatkit.sendwhatmsg_to_group(
                WHATSAPP_GROUP_NAME, mesaj, saat, dakika, wait_time=15, tab_close=True
            )
            print(f"Gönderildi: {post.title}")
            time.sleep(60)
        except Exception as e:
            print(f"Hata: {e}")

        seen_posts.add(post.link)

    with open(SEEN_POSTS_FILE, 'w', encoding='utf-8') as file:
        file.write("\n".join(seen_posts))
else:
    print("Yeni haber yok.")
