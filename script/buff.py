from test import match_result, get_hero_name, app

def print_power_up_buffs(match_id):
    data = match_result(match_id)

    if not data:
        print("Match not found.")
        return

    match_info = data['match_info']

    for player in match_info['players']:
        player['hero_name'] = get_hero_name(player['hero_id'])
        print(f"Player {player.get('hero_name')}")
        for buff in player.get('power_up_buffs', []):
            print("  type:", buff.get('type'), "| is_permanent:", buff.get('is_permanent'), "| value:", buff.get('value'))


with app.app_context():
    print_power_up_buffs(102774303)