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

def calculate_buffs(match_id):
    data = match_result(match_id)

    if not data:
        print("Match not found.")
        return

    match_info = data['match_info']

    buffs_summary = {}

    for player in match_info['players']:
        for buff in player.get('power_up_buffs', []):
            buff_type = buff.get('type')
            if buff_type not in buffs_summary:
                buffs_summary[buff_type] = {
                    'count': 0,
                    'total_value': 0,
                    'permanent_count': 0
                }
            buffs_summary[buff_type]['count'] += 1
            buffs_summary[buff_type]['total_value'] += buff.get('value', 0)
            if buff.get('is_permanent'):
                buffs_summary[buff_type]['permanent_count'] += 1

    print(f"Buffs Summary for Match {match_id}:")
    for buff_type, summary in buffs_summary.items():
        print(f"Buff Type: {buff_type}, Count: {summary['count']}, Total Value: {summary['total_value']}, Permanent Count: {summary['permanent_count']}")

with app.app_context():
    print_power_up_buffs(102774303)