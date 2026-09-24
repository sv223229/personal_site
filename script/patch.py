import requests
import os
import re
import time

def fetch_patch():
    url = f'https://store.steampowered.com/events/ajaxgetadjacentpartnerevents/?appid=1422450'
    try:
            response = requests.get(url)
            if response.status_code == 200:
                print('Successfully fetched posts from API.')
    
                return response.json()
            else:
                print('Error: failed to fetch posts from API, response status code:', response.status_code)
                return None
    except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None

def parse_patch_notes(text):
    raw_segments = re.findall(r'\[p\](.*?)\[/p\]', text, re.DOTALL)

    sections = []
    current_bullets = None

    for raw in raw_segments:
        raw = raw.strip()
        if not raw:
            continue  # skip empty spacer paragraphs

        is_header = raw.startswith('[b]') and raw.endswith('[/b]')
        clean = raw.replace('[b]', '').replace('[/b]', '').replace('\\[', '[')

        if is_header:
            sections.append({'header': clean, 'bullets': []})
            current_bullets = sections[-1]['bullets']
        else:
            if clean.startswith('- '):
                clean = clean[2:]
            if current_bullets is None:
                sections.append({'header': None, 'bullets': []})
                current_bullets = sections[-1]['bullets']
            current_bullets.append(clean)

    return sections


def steam_to_html(text):
    text = text.replace("[p][/p]", "")
    text = text.replace("[p]", "<p>")
    text = text.replace("[/p]", "</p>")
    text = text.replace("[b]", "<strong>")
    text = text.replace("[/b]", "</strong>")
    text = text.replace("\\[", "[")
    return text

data = fetch_patch()
headline = data["events"][0]["announcement_body"]["headline"]

match = re.search(r'\d{2}-\d{2}-\d{4}', headline)

if match:
    date = match.group()
    print(date)