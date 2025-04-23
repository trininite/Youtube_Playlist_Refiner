import re
from rapidfuzz import fuzz

AUTO_ACCEPT = 95
REVIEW_MIN = 80


with open("./src/duplicate_check/logs_2025-04-21_17-54-11.txt", mode="w", encoding="utf-8"):
    pass

def clean_title(dirty_title:str):
    dirty_title= dirty_title.lower()
    dirty_title= re.sub(r'\(.*?\)|\[.*?]|official|video|lyrics|audio|hd|4k', '', dirty_title)
    dirty_title = re.sub(r'[^\w\s]', '', dirty_title, flags=re.UNICODE)
    dirty_title = re.sub(r'_', ' ', dirty_title)
    clean_title= re.sub(r'\s+', ' ', dirty_title).strip()
    return clean_title

def compare_titles(a, b):
    
    a_clean = clean_title(a)
    b_clean = clean_title(b)
    return fuzz.ratio(a_clean, b_clean)

with open("./src/duplicate_check/2025-04-21_17-54-11.txt", mode="r", encoding="utf-8") as titles_file:
    titles = titles_file.readlines()

#for i, dirty_title in dirty_titles:
    
skip_indicies = []
duplicate_groups = []
# start at the beginning of the list
for i, title_1 in enumerate(titles):
    # skip indicies already accounted for
    if i in skip_indicies:
        continue
    # stop if i title is the last title
    if i == len(titles)-1:
        break
    duplicates = []
    # compare the rest of the list to the i title
    for j, title_2 in enumerate(titles[i+1:]):
        # skip indicies already accounted for
        if i+j+1 in skip_indicies:
            continue
        # compare the current title to the j title
        ratio = compare_titles(title_1, title_2)

        # lower than all thresholds, not a duplicate
        if ratio < REVIEW_MIN:
            continue

        # if larger than manual review but lower than automatic
        if ratio < AUTO_ACCEPT:
            # if user says not a duplicate, restart the j loop
            print(f"{title_1}\n{title_2}\n{ratio}\n\n")
            if input("Is this a duplicate? (y/n): ").upper() == "N":
                continue
        
        # if were here its larger than automatic so its a duplicate
        if len(duplicates) == 0:
            duplicates.append(title_1)
            duplicates.append(title_2)
        # otherwise, only add the next title
        else:
            duplicates.append(title_2)
        # add the index of the 
        skip_indicies.append(i+j+1)

    # dont add the duplicates group if its empty, meaning know duplicates were found
    if duplicates != []:
        duplicate_groups.append(duplicates)


with open("./src/duplicate_check/duplicates.txt", mode="w", encoding="utf-8") as duplicates_file:
    for duplicate_group in duplicate_groups:
        for title in duplicate_group:
            duplicates_file.write(title)
        duplicates_file.write("\n")