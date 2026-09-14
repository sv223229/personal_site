from test import match_result, get_hero_name, app, process_power_up_buffs

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

def calculate_total_buffs(player):
    """
    Sums stack_count * per_stack_amount for each buff, grouped by stat name.
    Returns e.g. {'fire_rate': 6.0, 'max_ammo': 15.0}
    """
    buffs = process_power_up_buffs(player)
    totals = {}

    for buff in buffs:
        if buff['per_stack_amount'] is None:
            continue  # unmatched type, e.g. gun_powerup_pickup — skip it

        total_for_this_buff = buff['stack_count'] * buff['per_stack_amount']
        totals[buff['display_name']] = totals.get(buff['display_name'], 0) + total_for_this_buff

    return totals
from test import app, match_result, process_power_up_buffs

with app.app_context():
    data = match_result(103363148)
    match_info = data['match_info']
    for player in match_info['players']:
        totals = calculate_total_buffs(player)
        print(player.get('hero_id'), totals)