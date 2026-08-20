# import requests
# import os
# import re
# from test import fetch_match_history
# from flask import Flask, redirect, render_template
# from flask import Flask, render_template, request, session
# from dotenv import load_dotenv

# template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
# static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
# app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
# env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'steam.env'))
# load_dotenv(env_path)
# # steamid = os.getenv("STEAM_ID")
# app.secret_key = os.getenv("SECRET_KEY")

# region = "NAmerica"

# match_history = fetch_match_history(os.getenv("STEAM_ID"))  # Fetch match history for the specified region and Steam ID

# match_id = [entry['match_id'] for entry in match_history]  # Extract match IDs from the match history

# # print(match_id)  # Print the list of match IDs to the console
# def match_result(match_id):
#     url = f'https://api.deadlock-api.com/v1/matches/{match_id}/metadata'
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             print('Successfully fetched posts from API.')
#             return response.json()
#         else:
#             print('Error: failed to fetch posts from API, response status code:', response.status_code)
#             return None
#     except requests.exceptions.RequestException as e:
#         print('Error:', e)
#         return None

# @app.route('/match_history/<match_id>', methods=['GET'])
# def match_detail(match_id):
#     match = match_result(match_id)
#     if not match:
#         return 'Match not found.'
#     print("Match metadata:", match)  # check terminal to see the real shape
#     return render_template('match_detail.html', match=match)

# if __name__ == '__main__':
#     app.run(debug=True)
