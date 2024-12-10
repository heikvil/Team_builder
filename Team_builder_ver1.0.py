import json
import os
from datetime import datetime
import shutil

def read_roster_file(roster_file):
    roster = []
    try:
        with open(roster_file, "r", encoding="utf-8") as file:
            roster = json.load(file)
    except FileNotFoundError:
        create_roster_file()
    return roster

def create_roster_file():
    roster = []
    with open("roster.json", "w", encoding="utf-8") as file:
        json.dump(roster, file, ensure_ascii=False, indent=0)
        print("Empty roster.json file created")
    return roster

def read_teams_file(teams_file):
    team_a = []
    team_b = []
    try:
        with open(teams_file, "r", encoding="utf-8") as file:
            teams = json.load(file)
            for player in teams:
                if player["Team"] == "A":
                    team_a.append(player)
                elif player["Team"] == "B":
                    team_b.append(player)
    except FileNotFoundError:
        create_teams_file()
    return team_a, team_b

def create_teams_file():
    teams = []
    with open("teams.json", "w", encoding="utf-8") as file:
        json.dump(teams, file, ensure_ascii=False, indent=0)
        print("Empty teams.json file created")
    return teams

def select_roster(roster):
    roster_names = {}
    for player in roster:
        roster_names[player["Name"].lower()] = player
    print("Select roster to match.")
    print_roster(roster)
    selected = []
    selection = ""
    while True:
        for i, player in enumerate(selected):
                    print(f"{player['Name']} - {player['Position']}")
        selection = input("\nSelect player, (e) ends or (m) back to menu: ").lower()
        if selection == "m":
            return selection
        if selection == "e":
            break
        if selection in roster_names:
            player = roster_names[selection]
            if player not in selected:
                selected.append(player)
            else:
                print("Player is already selected.")
        else:
            print("Player is not in the list.")
            answer = input("Do you want to add the new player (y/n) or (m) back to menu: ").lower()
            if answer == "m":
                return answer
            elif answer == 'y':
                new_player = add_new_player()
                roster.append(new_player)
                roster_names[new_player['Name'].lower()] = new_player
                print(f"Player '{new_player['Name']}' has added to the list.")
                selected.append(new_player)
            elif answer == 'n':
                continue
            else:
                print("Incorrect input.")
    return selected

def add_new_player():
    while True:
        name = input("Enter the new player name: ")
        if name != '':
            break
        else:
            print("Name can't be empty. Try again.")
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
    return new_player

def divide_teams(selected):
    team_a = []
    team_b = []
    defenders, hybrids, forwards = sort_players(selected)
    for i in range(len(defenders)):
        if i % 2 == 0:
            team_a.append(defenders[i])
        else:
            team_b.append(defenders[i])
    for i in range(len(hybrids)):
        if i % 2 == 0:
            team_a.append(hybrids[i])
        else:
            team_b.append(hybrids[i])
    for player in forwards:
        if len(team_b) == len(team_a):
            team_a_rating = [player["Rating"] for player in team_a]
            team_b_rating = [player["Rating"] for player in team_b]
            if team_a_rating < team_b_rating:
                team_a.append(player)
            else:
                team_b.append(player)
        elif len(team_b) <= len(team_a):
            team_b.append(player)
        else:
            team_a.append(player)
    print_teams(team_a, team_b)
    return team_a, team_b

def sort_players(selected):
    defenders = [player for player in selected if player["Position"].lower() == "defender"]
    hybrids = [player for player in selected if player["Position"].lower() == "hybrid"]
    forwards = [player for player in selected if player["Position"].lower() == "forward"]
    defenders.sort(key=lambda x: int(x["Rating"]), reverse=True)
    hybrids.sort(key=lambda x: int(x["Rating"]), reverse=True)
    forwards.sort(key=lambda x: int(x["Rating"]), reverse=True)
    return defenders, hybrids, forwards

def print_teams(team_a, team_b):
    print(f"\nTeam A ({len(team_a)})")
    for i, player in enumerate(team_a, 1):
                    print(f"{player['Name']}")
    print(f"\nTeam B ({len(team_b)})")
    for i, player in enumerate(team_b, 1):
                    print(f"{player['Name']}")
    team_a_rating = [player["Rating"] for player in team_a]
    team_b_rating = [player["Rating"] for player in team_b]
    print(f"\nA taso: {sum(team_a_rating)}")
    print(f"B taso: {sum(team_b_rating)}")


def save_roster_file(roster, roster_file):
    for player in roster:
        player.pop("Team", None)
    
    with open(roster_file, "w", newline="", encoding="utf-8") as file:
        json.dump(roster, file, ensure_ascii=False, indent=0)
    print(f"roster has saved to file: {roster_file}")

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
        print(f"{player['Name']} - {player['Position']}")
    print()
    print(f"Team B: ({len(team_b)})")
    for i, player in enumerate(team_b, 1):
                    print(f"{player['Name']} - {player['Position']}")

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

def update_roster(roster, team_a, team_b, team_a_goals, team_b_goals):
    goal_difference = team_a_goals - team_b_goals
    for player in roster:
        if player["Name"] in [name["Name"] for name in team_a]:
            player["Rating"] += 12 * goal_difference
        elif player["Name"] in [name["Name"] for name in team_b]:
            player["Rating"] -= 12 * goal_difference

def print_roster(roster):
    roster.sort(key=lambda x: int(x["Rating"]), reverse=True)
    print()
    for player in roster:
        print(player["Name"], player["Rating"])

def edit_roster(roster):
    print("1. Edit player")
    print("2. Remove player")
    print("(m) back to menu")
    answer = input("Select function: ")
    if answer.lower() == "m":
        return answer
    for player in roster:
        print(player["Name"], player["Rating"], player["Position"])
    if answer == "1":
        player_name = input("Select player to edit: ").lower()
        for i, player in enumerate(roster):
            if player["Name"].lower() == player_name.lower():
                index = i
        editing_player = next((player for player in roster if player["Name"].lower() == player_name), None)
        print(editing_player["Name"], editing_player["Rating"], editing_player["Position"])
        print("1. Edit name")
        print("2. Edit rating")
        print("3. Edit position")
        attribute = input("Select attribute to edit: ")
        if attribute == "1":
            edit_player_name(editing_player, roster, index)
        elif attribute == "2":
            edit_player_rating(editing_player, roster, index)
        elif attribute == "3":
            edit_player_position(editing_player, roster, index)
    elif answer == "2":
        player_name = input("Select player to remove: ").lower()
        for i, player in enumerate(roster):
            if player["Name"].lower() == player_name.lower():
                index = i
        removed_player = next((player for player in roster if player["Name"].lower() == player_name), None)
        print(removed_player["Name"], removed_player["Rating"], removed_player["Position"])
        del roster[index]
        print("Player removed")
    else:
        print("Incorrect input.")
    return roster

def edit_player_name(editing_player, roster, index):
    print(f"Current name is {editing_player['Name']}")
    new_name = input("Enter new name: ")
    roster[index]["Name"] = new_name
    print(f"New name is {roster[index]['Name']}")

def edit_player_rating(editing_player, roster, index):
    print(f"Current rating is {editing_player['Rating']}")
    new_rating = int(input("Enter new rating: "))
    roster[index]["Rating"] = new_rating
    print(f"New rating is {roster[index]['Rating']}")

def edit_player_position(editing_player, roster, index):
    print(f"Current position is {editing_player['Position']}")
    new_position = input("Enter new position (d) Defender, (h) Hybrid, (f) Forward: ")
    while True:
        if new_position.lower() == "d":
            new_position = "Defender"
            break
        elif new_position.lower() == "h":
            new_position = "Hybrid"
            break
        elif new_position.lower() == "f":
            new_position = "Forward"
            break
        else:
            print("Incorrect input. Try again.")
            continue  
    roster[index]["Position"] = new_position
    print(f"New position is {roster[index]['Position']}")

def backup_roster_file(roster_file):
    backup_kansio = "backups"
    if not os.path.exists(backup_kansio):
        os.makedirs(backup_kansio)
    filename = os.path.basename(roster_file)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_kansio, f"{timestamp}_{filename}")
    if os.path.exists(roster_file):
        shutil.copy2(roster_file, backup_file)
        print(f"Varmuuskopio luotu: {backup_file}")

def main():
    roster_file = "test_roster.json"
    teams_file = "teams.json"
    while True:
        roster = read_roster_file(roster_file)
        print("\nSelect function:")
        print("1. Divide new teams")
        print("2. Enter result and update roster ratings")
        print("3. Print roster sorted by rating")
        print("4. Edit roster")
        print("5. End programm")
        selection = input("Enter number: ")
        if selection == "1":
            selected = select_roster(roster)
            if selected == 'm':
                continue
            #backup_roster_file(roster_file)
            #Take backup to use removing comment
            save_roster_file(roster, roster_file)
            team_a, team_b = divide_teams(selected)
            save_teams_file(team_a, team_b, teams_file)
        elif selection == "2":
            team_a, team_b = read_teams_file(teams_file)
            team_a_goals, team_b_goals = result()
            update_roster(roster, team_a, team_b, team_a_goals, team_b_goals)
            #backup_roster_file(roster_file)
            #Take backup to use removing comment
            save_roster_file(roster, roster_file)
        elif selection == "3":
            print_roster(roster)
        elif selection == "4":
            roster = edit_roster(roster)
            if roster == "m":
                continue
            save_roster_file(roster, roster_file)
        elif selection == "5":
            break
        else:
            print("Incorret input. Try again")
            continue


if __name__ == "__main__":
    main()