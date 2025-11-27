import json
import re

try:
    with open('scripts/navarra_final_merged.json', 'r', encoding='utf-8') as f:
        json_content = json.load(f)
        data = json_content['data']

    comments_with_ref = 0
    comments_total = 0
    
    # Regex to find references at the end of string
    # Pattern: Book Abbrev + space + Chapter,Verse(-Chapter,Verse or -Verse)
    # e.g. Gn 1,1; Gn 1,3-5; Gn 1,1-2,4a
    ref_pattern = re.compile(r'([1-4]?\s?[A-Za-z]+)\s+(\d+),(\d+)(?:-(\d+)(?:,(\d+))?)?[a-z]?\s*$')

    for verse in data:
        if 'comment' in verse and verse['comment']:
            comments_total += 1
            text = verse['comment'].strip()
            # Check last 20 chars
            last_part = text[-30:]
            match = ref_pattern.search(last_part)
            if match:
                comments_with_ref += 1
            else:
                # Print some failures to see pattern
                if comments_total < 20:
                    print(f"No match: ...{last_part}")

    print(f"\nTotal comments: {comments_total}")
    print(f"Comments with parsable ref at end: {comments_with_ref}")
    print(f"Percentage: {comments_with_ref/comments_total*100:.2f}%")

except Exception as e:
    print(f"Error: {e}")
