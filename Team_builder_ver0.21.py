import json
import os
from datetime import datetime
import shutil

def read_players_file(players_file):
    players = []
    with open(players_file, "r", encoding="utf-8") as file:
        players = json.load(file)
    return players

def read_teams_file(teams_file):
    team_a = []
    team_b = []
    with open(teams_file, "r", encoding="utf-8") as file:
        teams = json.load(file)
        for player in teams:
            if player["Team"] == "A":
                team_a.append(player)
            elif player["Team"] == "B":
                team_b.append(player)
    return team_a, team_b

def select_players(players):
    players_name = {}
    for player in players:
        players_name[player["Name"].lower()] = player

    print("Select players to match.")
    columns = 5
    palyer_count = 0
    for player in players:
        palyer_count += 1
        if palyer_count % columns != 0:
            print(player["Name"], end=", ")
        else:
            print(player["Name"])
    
    selected = []
    selection = ""
    while True:
        selection = input("\nSelect player, (E) ends: ").lower()
        if selection == "e":
            break

        if selection in players_name:
            player = players_name[selection]
            if player not in selected:
                selected.append(player)
                for i, player in enumerate(selected, 1):
                    print(f"{player["Name"]} - {player["Position"]}")
            else:
                print("Player is already selected.")
        else:
            print("Player is not in the list.")
            answer = input("Do you want to add the new player (y/n): ").lower()
            if answer == 'y':
                name = input("Enter the new player name: ")
                while True:
                    try:
                        rating = int(input("Enter the new player rating: "))
                        break
                    except:
                        print("Ratingn has to be number. Try again.")
                        continue
                while True:
                    position = input("Enter the new player position (d) Defender, (h) Hybrid, (f) Forward: ")
                    if position.lower() == "d":
                        position = "Defender"
                        break
                    elif position.lower() == "h":
                        position = "Hybrid"
                        break
                    elif position.lower() == "f":
                        position = "Forward"
                        break
                    else:
                        print("Incorrect input. Try again.")
                        continue          
                new_player = {"Name": name, "Rating": rating, "Position": position}
                
                players.append(new_player)
                players_name[name.lower()] = new_player
                print(f"Player '{name}' has added to the list.")
                selected.append(new_player)
                for i, player in enumerate(selected, 1):
                    print(f"{player["Name"]} - {player["Position"]}")

            else:
                print("Incorrect input.")

    return selected

def divide_teams(selected):
    team_a = []
    team_b = []

    defenders = [player for player in selected if player["Position"].lower() == "defender"]
    hybrids = [player for player in selected if player["Position"].lower() == "hybrid"]
    forwards = [player for player in selected if player["Position"].lower() != ("defender" or "hybrid")]

    defenders.sort(key=lambda x: int(x["Rating"]), reverse=True)

    defender_count = len(defenders)
    for i in range(defender_count):
        if i % 2 == 0:
            team_a.append(defenders[i])
        else:
            team_b.append(defenders[i])

    hybrids.sort(key=lambda x: int(x["Rating"]), reverse=True)
    hybrid_count = len(hybrids)
    for i in range(hybrid_count):
        if i % 2 == 0:
            team_a.append(hybrids[i])
        else:
            team_b.append(hybrids[i])

    forwards.sort(key=lambda x: int(x["Rating"]), reverse=True)
    for player in forwards:
        if len(team_b) == len(team_a):
            if team_a_rating < team_b_rating:
                team_a.append(player)
            else:
                team_b.append(player)
        elif len(team_b) <= len(team_a):
            team_b.append(player)
        else:
            team_a.append(player)
    print(f"\nTeam A ({len(team_a)})")
    for i, player in enumerate(team_a, 1):
                    print(f"{player["Name"]}")
    print(f"\nTeam B ({len(team_b)})")
    for i, player in enumerate(team_b, 1):
                    print(f"{player["Name"]}")
    team_a_rating = [player["Rating"] for player in team_a]
    print(f"\nA taso: {sum(team_a_rating)}")
    team_b_rating = [player["Rating"] for player in team_b]
    print(f"B taso: {sum(team_b_rating)}")
    return team_a, team_b

def save_players_file(players, players_file):
    for player in players:
        player.pop("Team", None)
    
    with open(players_file, "w", newline="", encoding="utf-8") as file:
        json.dump(players, file, ensure_ascii=False, indent=0)
    print(f"Players has saved to file: {players_file}")

def save_teams_file(team_a, team_b, teams_file):
    teams = []
    for player in team_a:
        player["Team"] = "A"
        teams.append(player)
    for player in team_b:
        player["Team"] = "B"
        teams.append(player)
    with open(teams_file, "w", newline="", encoding="utf-8") as file:
        json.dump(teams, file, ensure_ascii=False, indent=0)

def print_teams(team_a, team_b):
    print(f"Team A: ({len(team_a)})")
    for i, player in enumerate(team_a, 1):
        print(f"{player["Name"]} - {player["Position"]}")
    print()
    print(f"Team B: ({len(team_b)})")
    for i, player in enumerate(team_b, 1):
                    print(f"{player["Name"]} - {player["Position"]}")

def result():
    while True:
        try:
            team_a_goals = int(input("Enter team A score: "))
            team_b_goals = int(input("Enter team b score: "))
            break
        except ValueError:
            print("Incorrect input. Inputs has to be numbers.")
            continue
    return team_a_goals, team_b_goals

def update_players(players, team_a, team_b, team_a_goals, team_b_goals):
    goal_difference = team_a_goals - team_b_goals
    for player in players:
        if player["Name"] in [name["Name"] for name in team_a]:
            player["Rating"] += 12 * goal_difference
        elif player["Name"] in [name["Name"] for name in team_b]:
            player["Rating"] -= 12 * goal_difference

def print_players(players):
    players.sort(key=lambda x: int(x["Rating"]), reverse=True)
    for player in players:
        print(player["Name"], player["Rating"])

def edit_players(players):
    print("1. Edit player")
    print("2. Remove player")
    answer = input("Select function: ")
    for player in players:
        print(player["Name"], player["Rating"], player["Position"])
    if answer == "1":
        player_name = input("Select player to edit: ").lower()
        for i, player in enumerate(players):
            if player["Name"].lower() == player_name.lower():
                index = i
        editing_player = next((player for player in players if player["Name"].lower() == player_name), None)
        print(editing_player["Name"], editing_player["Rating"], editing_player["Position"])
        print("1. Edit name")
        print("2. Edit rating")
        print("3. Edit pelipaikkaa")
        attribute = input("Select attribute to edit.")
        if attribute == "1":
            print(f"Current name is {editing_player["Name"]}")
            new_name = input("Enter new name: ")
            players[index]["Name"] = new_name
            print(f"New name is {players[index]["Name"]}")
        elif attribute == "2":
            print(f"Current rating is {editing_player["Rating"]}")
            new_rating = int(input("Enter new rating: "))
            players[index]["Rating"] = new_rating
            print(f"New rating is {players[index]["Rating"]}")
        elif attribute == "3":
            print(f"Current position is {editing_player["Position"]}")
            new_position = input("Enter new position (Defender / Hybrid / Forward): ")
            players[index]["Position"] = new_position
            print(f"New position is {players[index]["Position"]}")
    if answer == "2":
        player_name = input("Select player to remove: ").lower()
        for i, player in enumerate(players):
            if player["Name"].lower() == player_name.lower():
                index = i
        removed_player = next((player for player in players if player["Name"].lower() == player_name), None)
        print(removed_player["Name"], removed_player["Rating"], removed_player["Position"])
        del players[index]
        print("Player removed")
    else:
        print("Incorrect input.")
    return players

def backup_players_file(players_file):
    backup_kansio = "backups"
    if not os.path.exists(backup_kansio):
        os.makedirs(backup_kansio)

    filename = os.path.basename(players_file)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_kansio, f"{timestamp}_{filename}")
    
    if os.path.exists(players_file):
        shutil.copy2(players_file, backup_file)
        print(f"Varmuuskopio luotu: {backup_file}")

def main():
    if not os.path.isfile("players.json"):
        players = []
        with open("players.json", "w", encoding="utf-8") as file:
            json.dump(players, file, ensure_ascii=False, indent=0)
            print("players.json file created")
    players_file = "players.json"
    if not os.path.isfile("teams.json"):
        teams = []
        with open("teams.json", "w", encoding="utf-8") as file:
            json.dump(teams, file, ensure_ascii=False, indent=0)
            print("teams.json file created")
    teams_file = "teams.json"
    while True:
        players = read_players_file(players_file)

        print("\nSelect function:")
        print("1. Divide new teams")
        print("2. Enter result and update players ratings")
        print("3. Print players sorted by rating")
        print("4. Edit players")
        selection = input("Enter number: ")

        if selection == "1":
            selected = select_players(players)
            #backup_players_file(players_file)
            #Ota varmuuskopiointi käyttöön poistamalla risuaita
            save_players_file(players, players_file)
            team_a, team_b = divide_teams(selected)
            save_teams_file(team_a, team_b, teams_file)

        elif selection == "2":
            team_a, team_b = read_teams_file(teams_file)
            team_a_goals, team_b_goals = result()
            update_players(players, team_a, team_b, team_a_goals, team_b_goals)
            #backup_players_file(players_file)
            #Ota varmuuskopiointi käyttöön poistamalla risuaita
            save_players_file(players, players_file)
        
        elif selection == "3":
            print_players(players)

        elif selection == "4":
            edit_players(players)
            save_players_file(players, players_file)

        else:
            print("Incorret input. Try again")
            continue
        
        answer = input("Do you want to restar the program (y/n)?").lower()
        if answer != "y":
            print("Program ends.")
            break

main()