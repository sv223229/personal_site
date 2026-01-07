import requests
region = "Europe"
def get_region(region):
    url = f'https://api.deadlock-api.com/v1/leaderboard/{region}'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            print('Successfully fetched posts from API.')
            posts = response.json()
            
            return posts
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

def main():
    posts = get_region(region)

    if posts:
        for entry in posts['entries']:
         print(entry['account_name'])
        
    else:
        print('Failed to fetch posts from API.')

if __name__ == '__main__':
    main()