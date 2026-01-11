import requests
from flask import Flask, render_template
import os

region = "NAmerica"
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))

app = Flask(__name__, template_folder=template_dir)

def fetch_leaderboard(region):
    url = f'https://api.deadlock-api.com/v1/leaderboard/{region}'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            print('Successfully fetched posts from API.')
            posts = response.json()
            return posts
        else:
            print('Error: failed to fetch posts from API, response status code:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None


@app.route('/', methods=['GET'])
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

if __name__ == '__main__':
    app.run(debug=True)