import json

try:
    with open('scripts/navarra_final_merged.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Find John
    john = next((b for b in data if b['book'] == 'JHN' or b['book'] == 'Juan'), None)
    
    if john:
        print(f"Found book: {john['book']}")
        # Check first chapter
        ch1 = john['chapters'][0]
        print(f"Chapter 1 verses: {len(ch1['verses'])}")
        
        # Check comments in verses 19-25
        for v in ch1['verses']:
            if 19 <= v['verse'] <= 25:
                print(f"Verse {v['verse']} comment: {v.get('comment', '')[:50]}...")
    else:
        print("John not found in JSON")
        
except Exception as e:
    print(f"Error: {e}")
