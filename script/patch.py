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

# print(fetch_patch())


def steam_to_html(text):
    text = text.replace("[p][/p]", "")
    text = text.replace("[p]", "<p>")
    text = text.replace("[/p]", "</p>")
    text = text.replace("[b]", "<strong>")
    text = text.replace("[/b]", "</strong>")

    return text