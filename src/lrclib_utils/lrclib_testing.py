from lrcup import LRCLib

lrclib = LRCLib()

# Fetch synced lyrics via search
results = lrclib.search(
    track = "Subways of your mind",
    artist = "FEX"
)


with open("lyrics.txt", "w") as f:
    for result in results:
        f.write(result)