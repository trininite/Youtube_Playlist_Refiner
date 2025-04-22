import yt_dlp
from datetime import datetime

# replace this with your playlist url
playlist_url = 'https://www.youtube.com/playlist?list=PLqj_PfKdlkzddIfmwd96IWl5UU5qTShZl'

# current date and time for filename
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
filename = f"{timestamp}.txt"

# yt_dlp options
ydl_opts = {
    'quiet': True,
    'extract_flat': True,
    'force_generic_extractor': True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(playlist_url, download=False)
    entries = info_dict.get('entries', [])

    titles = [entry.get('title', 'Untitled') for entry in entries]

# save to file
with open(filename, 'w', encoding='utf-8') as f:
    for title in titles:
        f.write(f"{title}\n")

print(f"Saved {len(titles)} titles to {filename}")
