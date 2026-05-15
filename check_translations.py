import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# remove scripts and styles
html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<title.*?>.*?</title>', '', html, flags=re.DOTALL)

# remove tags
text = re.sub(r'<[^>]+>', ' ', html)

lines = [line.strip() for line in text.split('\n')]
lines = [re.sub(r'\s+', ' ', line) for line in lines if line]

with open('translations.js', 'r', encoding='utf-8') as f:
    js_content = f.read()
    
match = re.search(r'const translations = (\{.*?\});', js_content, re.DOTALL)
translations = json.loads(match.group(1))

missing = set()
for line in lines:
    if len(line) > 1 and line not in ['EN', 'ES', 'English', 'Español'] and 'Which language' not in line:
        found = False
        for k in translations.keys():
            if k.lower() == line.lower():
                found = True
                break
        if not found:
            missing.add(line)

print("MISSING STRINGS:")
for m in sorted(list(missing)):
    print(m)

