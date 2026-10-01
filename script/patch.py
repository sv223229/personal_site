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

def clean_bbcode(text):
    # Images: drop entirely — banner graphics aren't useful as plain text
    text = re.sub(r'\[img\].*?\[/img\]', '', text, flags=re.DOTALL)

    # [url=href]label[/url] -> "label (href)", collapsing to just the URL
    
    def _url_repl(m):
        href, label = m.group(1), m.group(2).strip()
        if not label or label == href:
            return href
        return f'{label} ({href})'
    text = re.sub(r'\[url=([^\]]+)\](.*?)\[/url\]', _url_repl, text, flags=re.DOTALL)
    text = re.sub(r'\[url\](.*?)\[/url\]', r'\1', text, flags=re.DOTALL)  # bare [url]href[/url]

    # Inline formatting — keep the text, drop the markup
    for tag in ['b', 'i', 'u', 'strike']:
        text = text.replace(f'[{tag}]', '').replace(f'[/{tag}]', '')

    # Escaped literal brackets, e.g. \[ General ]
    text = text.replace('\\[', '[').replace('\\]', ']')

    return text.strip()


def parse_patch_notes(text):
    # Some posts wrap paragraphs in [p]...[/p] (patch notes);
    if '[p]' in text:
        raw_segments = re.findall(r'\[p\](.*?)\[/p\]', text, re.DOTALL)
    else:
        raw_segments = re.split(r'\n\s*\n+', text.strip())

    sections = []
    current_bullets = None

    for raw in raw_segments:
        raw = raw.strip()
        if not raw:
            continue  # skip empty/spacer paragraphs

        is_header = raw.startswith('[b]') and raw.endswith('[/b]')
        clean = clean_bbcode(raw)

        if not clean:
            continue  # nothing left after stripping tags (e.g. a lone image)

        if clean.startswith('- '):
            clean = clean[2:]

        if is_header:
            sections.append({'header': clean, 'bullets': []})
            current_bullets = sections[-1]['bullets']
        else:
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

body = data["events"][0]["announcement_body"]["body"]
sections = parse_patch_notes(body)
# print(sections)

headline = data["events"][0]["announcement_body"]["headline"]

match = re.search(r'\d{2}-\d{2}-\d{4}', headline)

if match:
    date = match.group()
    print(date)
else:
    print("No date found in headline:", headline)