import requests
import os
import re
from flask import Flask, redirect, render_template
from flask import Flask, render_template, request, session
from dotenv import load_dotenv

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'steam.env'))
load_dotenv(env_path)
# steamid = os.getenv("STEAM_ID")
app.secret_key = os.getenv("SECRET_KEY")

region = "NAmerica"


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


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        raw_input = request.form.get('steamid')

        if not raw_input:
            return 'Please enter a Steam ID or profile URL.'

        numbers = re.findall(r'\d+', raw_input)

        if not numbers:
            return 'Please enter a valid numeric Steam ID.'

        steamid = numbers[0]  # take the first number sequence found

        session['steamid'] = steamid
        return redirect(('match-history'))  # send them to match history

    return render_template('form.html')

@app.route('/leaderboard', methods=['GET'])
def home():
    posts = fetch_leaderboard(region)
    if posts:
        return render_template('leaderboard.html', leader_board=posts['entries'])
    else:
        return 'Failed to fetch posts from API.'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/steam', methods=['GET'])

def account():
    steamid = session.get('steamid')
    if not steamid:
        return 'Steam ID is required.'
    posts = fetch_account(steamid)
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
            data = response.json()
            filtered_output = [item for item in data if item['match_mode'] == 4]
            return filtered_output
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

def calculate_win_loss_ratio(entry):
    wins = sum(1 for entry in entry if entry.get('player_match_outcome') == 'Win')
    losses = sum(1 for entry in entry if entry.get('player_match_outcome') == 'Loss')
    total_matches = wins + losses

    return {
        'wins': wins,
        'losses': losses,
        'win_loss_ratio': round((wins / total_matches)*100, 2) if total_matches > 0 else 0
    }


def label_match_result(entry):
    entry['player_match_outcome'] = 'Win' if entry.get('player_match_outcome') == 1 else 'Loss'
    return entry

def process_match_players(match_info):
    winning_team = match_info['winning_team']
    duration_s = match_info['duration_s']
    for player in match_info['players']:
        player['result'] = 'Win' if player['team'] == winning_team else 'Loss'
        player['match_duration_s'] = duration_s  # reuse your existing helper
        calculate_net_worth_per_min(player)
    return match_info['players']

@app.route('/match-history', methods=['GET'])
def match_history():
    steamid = session.get('steamid')
    if not steamid:
        return 'Steam ID is required.'

    print("Loaded STEAM_ID:", steamid)

    posts = fetch_match_history(steamid)
    if not posts:
        print(steamid)
        return 'Failed to fetch account from API.'

    for entry in posts:
        format_duration(entry)
        calculate_net_worth_per_min(entry)
        label_match_result(entry)

    record = calculate_win_loss_ratio(posts)

    return render_template('test.html', match_history=posts, record=record)

def match_result(match_id):
    url = f'https://api.deadlock-api.com/v1/matches/{match_id}/metadata'
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



@app.route('/match_history/<match_id>', methods=['GET'])
def match_detail(match_id):
    data = match_result(match_id)
    if not data:
        return 'Match not found.'

    match_info = data['match_info']
    players = process_match_players(match_info)
    minutes, seconds = divmod(match_info['duration_s'], 60)

    return render_template(
        'match_detail.html',
        match_id=match_info['match_id'],
        duration_min=minutes,
        duration_sec=seconds,
        winning_team=match_info['winning_team'],
        team0_players=[p for p in players if p['team'] == 0],
        team1_players=[p for p in players if p['team'] == 1]
    )

    
if __name__ == '__main__':
    app.run(debug=True)