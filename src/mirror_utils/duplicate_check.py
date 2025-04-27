import re
from rapidfuzz import fuzz

AUTO_ACCEPT = 95
REVIEW_MIN = 80

def clean_title(dirty_title:str):
    dirty_title= dirty_title.lower()
    dirty_title= re.sub(r'\(.*?\)|\[.*?]|official|video|lyrics|audio|hd|4k', '', dirty_title)
    dirty_title = re.sub(r'[^\w\s]', '', dirty_title, flags=re.UNICODE)
    dirty_title = re.sub(r'_', ' ', dirty_title)
    clean_title= re.sub(r'\s+', ' ', dirty_title).strip()
    return clean_title


def run_duplicate_check(song_list: list[dict]) -> list[dict]:
    processed_indices: set[int] = set()

    for i, video_i in enumerate(song_list):
        if i in processed_indices:
            continue

        duplicates = []
        duplicate_indices = []

        video_i_title = clean_title(video_i["title"])

        for j, video_j in enumerate(song_list):
            if i == j or j in processed_indices:
                continue

            video_j_title = clean_title(video_j["title"])
            ratio = fuzz.ratio(video_i_title, video_j_title)

            if ratio < REVIEW_MIN:
                continue

            if ratio < AUTO_ACCEPT:
                print(f"\nPossible duplicate:\n  {video_i_title}\n  {video_j_title}\n  Similarity: {ratio}%\n")
                if input("Is this a duplicate? (y/n): ").strip().lower() != "y":
                    continue

            # found a duplicate
            if not duplicates:
                duplicates.append(video_i["title"])
                duplicate_indices.append(i)

            duplicates.append(video_j["title"])
            duplicate_indices.append(j)

        if duplicates:
            print("\nSelect the number of the title you want to KEEP:")
            for idx, title in enumerate(duplicates):
                print(f"{idx}: {title}")
            while True:
                try:
                    picked = int(input("> ").strip())
                    if 0 <= picked < len(duplicates):
                        break
                    else:
                        print("Invalid number. Try again.")
                except ValueError:
                    print("Invalid input. Enter a number.")

            for idx, song_idx in enumerate(duplicate_indices):
                if idx == picked:
                    continue
                song_list[song_idx]["duplicate"] = True
                processed_indices.add(song_idx)

        else:
            processed_indices.add(i)

    return song_list