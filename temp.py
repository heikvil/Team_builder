import json

with open('test_roster.json', 'r') as f:
    roster = json.load(f)

print(roster)

if 'John X' in [player['Name'] for player in roster]:
    print('Toimii')
else:
    print('Ei toimi')

print([player['Name'] for player in roster])