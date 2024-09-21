import json
import os
from datetime import datetime
import shutil

def read_players_from_file(players_file):
    players =[]
    with open(players_file, "r", encoding="utf-8") as f:
        players = json.load(f)
    return players

def read_teams_from_file(teams_file):
    team_a = []
    team_b = []
    with open(teams_file, "r", encoding="utf-8") as f:
        teams = json.load(f)
        for player in teams:
            if player["Teams"] == "A":
                team_a.append(player)
            elif player["Teams"] == "B":
                team_b.append(player)
    return team_a, team_b

def choose_players(players):
    players_names = {}
    for player in players:
        print(players)
        print(player) #debug
        player = players_names[player["Name"].lower()]

    print("Choose players to match:")
    columns = 5
    players_count = 0
    for player in players:
        players_count += 1
        if players_count % columns != 0:
            print(player["Name"], end=", ")
        else:
            print(player["Name"])
    
    selected = []
    selection = ""
    while True:
        selection = input("\nSelect players, (E) ends: ").lower()
        if selection == "e":
            break

        if selection in players_names:
            players = players_names[selection]
            if players not in selected:
                selected.append(players)
                for i, players in enumerate(selected, 1):
                    print(f"{players["Name"]} - {players["Position"]}")
            else:
                print("Player is already selected.")
        else:
            print("Player is not in list.")
            answer = input("Do you want to add new a player (y/n): ").lower()
            if answer == 'y':
                name = input("Enter the new players name: ")
                while True:
                    try:
                        rating = int(input("Enter the new player's rating: "))
                        break
                    except:
                        print("Ratingn has to be number. Try again.")
                        continue
                while True:    
                    position = input("Enter the new player's position (d) Defender, (h) Hybrid, (f) Forward: ")
                    print(position) #debug
                    if position.lower() != "d":
                        print("Wrong position input. Try Again.")
                        continue
                    else:
                        break
                
                new_player = {"Name": name, "Rating": rating, "Position": position}
                
                players.append(new_player) #Is this necessary?
                players_names[name.lower()] = new_player
                print(f"Player '{name}' has added to the players list.")
                selected.append(new_player)
                for i, players in enumerate(selected, 1):
                    print(f"{players["Name"]} - {players["Position"]}")
    return selected

def divide_players_to_teams(selected):
    team_a = []
    team_b = []
    rating_team_a = 0
    rating_team_b = 0

    defenders = [players for players in selected if players["Position"].lower() == "defender"]
    hybrid = [players for players in selected if players["Position"].lower() == "hybrid"]
    forwards = [players for players in selected if players["Position"].lower() != ("defender" or "hybrid")]

    defenders.sort(key=lambda x: int(x["Rating"]), reverse=True)

    defenders_count = len(defenders)
    for i in range(defenders_count):
        if i % 2 == 0:
            team_a.append(defenders[i])
            rating_team_a += defenders[i]["Rating"]
        else:
            team_b.append(defenders[i])
            rating_team_b += defenders[i]["Rating"]

    hybrid.sort(key=lambda x: int(x["Rating"]), reverse=True)
    hybrid_count = len(hybrid)
    for i in range(hybrid_count):
        if i % 2 == 0:
            team_a.append(hybrid[i])
            rating_team_a += hybrid[i]["Rating"]
        else:
            team_b.append(hybrid[i])
            rating_team_b += hybrid[i]["Rating"]

    forwards.sort(key=lambda x: int(x["Rating"]), reverse=True)
    for players in forwards:
        if len(team_b) == len(team_a):
            if rating_team_a < rating_team_b:
                team_a.append(players)
            else:
                team_b.append(players)
        elif len(team_b) <= len(team_a):
            team_b.append(players)
        else:
            team_a.append(players)
    print(f"\nTeam A ({len(team_a)})")
    for i, players in enumerate(team_a, 1):
                    print(f"{players["Name"]}")
    print(f"\nTeam B ({len(team_b)})")
    for i, players in enumerate(team_b, 1):
                    print(f"{players["Name"]}")
    rating_team_a = [players["Rating"] for players in team_a]
    print(f"\nTeam A rating: {sum(rating_team_a)}")
    rating_team_b = [players["Rating"] for players in team_b]
    print(f"Team B rating: {sum(rating_team_b)}")
    return team_a, team_b

def save_players_file(players, players_file):
    for players in players:
        players.pop("Teams", None)
    
    with open(players_file, "w", newline="", encoding="utf-8") as f:
        json.dump(players, f, ensure_ascii=False, indent=0)
    print(f"Players saved to file: {players_file}")

def save_teams_file(team_a, team_b, teams_file):
    teams = []
    for players in team_a:
        players["Teams"] = "A"
        teams.append(players)
    for players in team_b:
        players["Teams"] = "B"
        teams.append(players)
    with open(teams_file, "w", newline="", encoding="utf-8") as file:
        json.dump(teams, file, ensure_ascii=False, indent=0)

def print_teams(team_a, team_b):
    print(f"Team A: ({len(team_a)})")
    for i, players in enumerate(team_a, 1):
        print(f"{players["Name"]} - {players["Position"]}")
    print(f"\nTeam B: ({len(team_b)})")
    for i, players in enumerate(team_b, 1):
                    print(f"{players["Name"]} - {players["Position"]}")

def result():
    while True:
        try:
            team_a_goals = int(input("Enter Team A goals: "))
            team_b_goals = int(input("Enter Team B golas: "))
            break
        except ValueError:
            print("Error: The inputs are not valid numbers.")
            continue
    return team_a_goals, team_b_goals

def update_players(players, team_a, team_b, team_a_goals, team_b_goals):
    goal_difference = team_a_goals - team_b_goals
    for players in players:
        if players["Name"] in [name["Name"] for name in team_a]:
            players["Rating"] += 12 * goal_difference
        elif players["Name"] in [name["Name"] for name in team_b]:
            players["Rating"] -= 12 * goal_difference

def print_players(players):
    players.sort(key=lambda x: int(x["Rating"]), reverse=True)
    for players in players:
        print(players["Name"], players["Rating"])

def edit_players(players):
    print("1. Edit player")
    print("2. Remove players")
    answer = input("Enter the function: ")
    for players in players:
        print(players["Name"], players["Rating"], players["Position"])
    if answer == "1":
        players_name = input("Valitse muokattava players: ").lower()
        for i, players in enumerate(players):
            if players["Name"].lower() == players_name.lower():
                index = i
        edit_player = next((players for players in players if players["Name"].lower() == players_name), None)
        print(edit_player["Name"], edit_player["Rating"], edit_player["Position"])
        print("1. Edit name")
        print("2. Edit rating")
        print("3. Edit position")
        attribute = input("Choose wich attribute you want to edit.")
        if attribute == "1":
            print(f"The current name is {edit_player['name']}")
            new_name = input("Enter the new name: ")
            players[index]["Name"] = new_name
            print(f"The name has updated, yhe new name is {players[index]["Name"]}")
        elif attribute == "2":
            print(f"The curren rating is {edit_player['rating']}")
            new_rating = int(input("Enter the new rating: "))
            players[index]["Rating"] = new_rating
            print(f"The rating has uptated, the new rating is {players[index]["Rating"]}")
        elif attribute == "3":
            print(f"The current position is {edit_player["Position"]}")
            new_position = input("Enter the new position (Defender / Hybrid / Forward): ")
            players[index]["Position"] = new_position
            print(f"The position has updateds, the new postion is {players[index]["Position"]}")
    if answer == "2":
        players_name = input("Choose hte palyer to be removed: ").lower()
        for i, players in enumerate(players):
            if players["Name"].lower() == players_name.lower():
                index = i
        removed_player = next((player for player in players if player["Name"].lower() == players_name), None)
        print(removed_player["Name"], removed_player["Rating"], removed_player["Position"])
        del players[index]
        print(f"{players_name} removed.")
    else:
        print("Not supported input.")
    return players

def backup_players_file(file):
    backup_folder = "backups"
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    filename = os.path.basename(file)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_folder, f"{timestamp}_{filename}")
    
    if os.path.exists(file):
        shutil.copy2(file, backup_file)
        print(f"Backup created: {backup_file}")

def main():
    if not os.path.isfile("players.json"):
        players = [
            {
                "Name": "Test A",
                "Rating": 1000,
                "Position": "Forward"
            }
        ]
        with open("players.json", "w", encoding="utf-8") as f:
            json.dump(players, f, ensure_ascii=False, indent=0)
            print("players.json file has created")
    players_file = "players.json"
    if not os.path.isfile("teams.json"):
        teams = [
            {
                "Name": "Test A",
                "Rating": 1000,
                "Position": "Forward",
                "Team": "A"
            }
            ]
        with open("teams.json", "w", encoding="utf-8") as file:
            json.dump(teams, file, ensure_ascii=False, indent=0)
            print("teams.json file has created")
    teams_file = "teams.json"
    while True:
        players = (players_file)

        print("\nSelect function:")
        print("1. Divide the new teams")
        print("2. Enter the result and update players ratingts")
        print("3. Print the players, sorted by ratingns")
        print("4. Edit players")
        answer = input("\nEnter function: ")

        if answer == "1":
            selected= choose_players(players)
            #backup_players_file(players_file)
            save_players_file(players, players_file)
            team_a, team_b = divide_players_to_teams(selected)
            save_teams_file(team_a, team_b, teams_file)

        elif answer == "2":
            team_a, team_b = read_players_from_file(teams_file)
            team_a_goals, team_b_goals = result()
            update_players(players, team_a, team_b, team_a_goals, team_b_goals)
            #backup_players_file(players_file)
            #Ota varmuuskopiointi käyttöön poistamalla risuaita
            save_players_file(players, players_file)
        
        elif answer == "3":
            print_players(players)

        elif answer == "4":
            edit_players(players)
            save_players_file(players, players_file)

        else:
            print("Not suported funtion. Try again")
            continue
        
        repeat = input("Do you wan to run the program again (y/n)?").lower()
        if repeat != "y":
            print("End of programm.")
            break

main()