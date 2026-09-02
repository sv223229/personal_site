from test import match_result

data = match_result(103004619)

if not data:
    print("Match not found.")
else:
    match_info = data['match_info']

    for player in match_info['players']:
        print(f"Player {player.get('hero_id')}:")
        for buff in player.get('power_up_buffs', []):
            print("  type:", buff.get('type'), "| is_permanent:", buff.get('is_permanent'), "| value:", buff.get('value'))