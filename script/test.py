import requests
from flask import Flask, render_template
import os
from dotenv import load_dotenv
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'steam.env'))
load_dotenv(env_path)
steamid = os.getenv("STEAM_ID")
print("Loaded STEAM_ID:", os.getenv("STEAM_ID"))

region = "NAmerica"
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

def fetch_leaderboard(region):
    url = f'https://api.deadlock-api.com/v1/leaderboard/{region}'
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

def fetch_account(steamid):
    url = f'https://api.deadlock-api.com/v1/players/steam-search?search_query={steamid}'
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

@app.route('/leaderboard', methods=['GET'])
@app.route('/leaderboard.html', methods=['GET'])
def home():
    posts = fetch_leaderboard(region)
    if posts:
        return render_template('leaderboard.html', leader_board=posts['entries'])
    else:
        return 'Failed to fetch posts from API.'

@app.route('/index', methods=['GET'])
@app.route('/index.html', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/steam', methods=['GET'])
@app.route('/steam.html', methods=['GET'])
def account():
    # Assuming you want to fetch a specific account based on a query parameter or session
    steamid = os.getenv("STEAM_ID")  # You can replace this with a dynamic value if needed
    if not steamid:
        return 'Steam ID is required.'
    posts = fetch_account(steamid)
    # print("Fetched account data:", posts)
    if posts:
        return render_template('steam.html', accounts=posts)
    else:
        return 'Failed to fetch account from API.'

def fetch_match_history(steamid):
    url = f'https://api.deadlock-api.com/v1/players/{steamid}/match-history'
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

def format_duration(entry):
    minutes, seconds = divmod(entry['match_duration_s'], 60)
    entry['match_duration_min'] = minutes
    entry['match_duration_sec'] = seconds
    return entry

def calculate_net_worth_per_min(entry):
    total_minutes = entry['match_duration_s'] / 60
    entry['net_worth_per_min'] = round(entry['net_worth'] / total_minutes, 1) if total_minutes > 0 else 0
    return entry

def label_match_result(entry):
    entry['match_result'] = 'Win' if entry.get('match_result') == 1 else 'Defeat'
    return entry

@app.route('/test', methods=['GET'])
@app.route('/test.html', methods=['GET'])
def match_history():
    steamid = os.getenv("STEAM_ID")
    if not steamid:
        return 'Steam ID is required.'

    posts = fetch_match_history(steamid)
    if not posts:
        return 'Failed to fetch account from API.'

    

    for entry in posts:
        format_duration(entry)
        calculate_net_worth_per_min(entry)
        label_match_result(entry)

    return render_template('test.html', match_history=posts)


    
if __name__ == '__main__':
    app.run(debug=True)