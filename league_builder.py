import sys
import csv


# returns a list of dictionaries from the given file, one for each player
def get_players_from_file(filename):
    with open(filename, newline='') as playerfile:
        return list(csv.DictReader(playerfile, delimiter=','))


def average_team_height(team):
    fieldname = 'Height (inches)'
    height_total = 0

    for player in team:
        height_total += int(player[fieldname])

    try:
        avg = height_total / len(team)
    except ZeroDivisionError as zde:
        avg = 0

    return avg


def get_team(team_list, min_or_max):
    try:
        return_team = team_list[0]
    except IndexError:
        return None

    i = 1

    while i < len(team_list):
        if min_or_max == 'min':
            if average_team_height(
                    team_list[i]['players']) < average_team_height(
                    return_team['players']):
                return_team = team_list[i]
        elif min_or_max == 'max':
            if average_team_height(
                    team_list[i]['players']) >= average_team_height(
                    return_team['players']):
                return_team = team_list[i]
        i += 1

    return return_team


# returns the shortest player from any player list
def shortest_player(team):
    fieldname = 'Height (inches)'
    shortest = team[0]

    for player in team:
        if player[fieldname] < shortest[fieldname]:
            shortest = player

    return shortest


# returns the max difference in avg heights within a list of teams
def max_average_height_diff(team_list):
    diff = avg_height_diff(team_list[0], team_list[1])

    for i in range(1, len(team_list) - 2):

        for j in range(i + 1, len(team_list) - 1):

            comp_diff = avg_height_diff(team_list[i], team_list[j])

            if comp_diff > diff:
                diff = avg_height_diff

    return diff


# helper function to return the difference in average heights between 2 teams
def avg_height_diff(team1, team2):
    return abs(average_team_height(team1['players']) - average_team_height(
        team2['players']))


def create_player_round(player_list, team_list):
    player_round = []

    while len(player_round) < len(
            league):  # each round will have the same number of players as leagues

        # get shortest available player

        # NOTE: we're assuming that the players can be evenly distributed through all teams
        # this would normally be wrapped in a try/catch block to handle situations where the number of players is not a multiple of the number of teams
        player_to_add = shortest_player(player_list)

        player_list.remove(
            player_to_add)  # remove shortest player from available players

        player_round.append(player_to_add)  # add player to round

    return player_round


def distribute_players(player_list, team_list):
    while len(player_list) > 0:  # all players have same experience

        player_round = create_player_round(player_list,
                                           team_list)  # create list for the players to add in this round

        if max_average_height_diff(
                team_list) == 0:  # if all teams have equal avg heights, distribution logic is unnecessary

            for i, team in enumerate(team_list):
                team['players'].append(player_round[i])
        else:

            teams_after_round = []  # list to hold each team after a player has been added

            while len(
                    player_round) > 0:  # loop over players in the round from shortest to tallest

                player_to_add = shortest_player(
                    player_round)  # get the shortest player
                player_round.remove(player_to_add)

                team_to_add = get_team(team_list,
                                       'max')  # get and remove the tallest team
                team_list.remove(team_to_add)

                # add the shortest player to the tallest team, ensuring that the height averages are kept as close to one another as possible
                # this will work for mostly even height distribution among players
                team_to_add['players'].append(player_to_add)

                teams_after_round.append(
                    team_to_add)  # move team to the post-round list

            team_list.extend(
                teams_after_round)  # add all teams to teh original list


# opens a new file based on player name and writes letter to guardians
def write_letter(player, team):
    # variables for letter string formatting
    display_name = "_".join(player['Name'].lower().split())
    filename = display_name + ".txt"
    player_name = player['Name']
    team_name = team['name'].title()

    # contents of letter strings
    salutation = "Dear {},\n".format(player['Guardian Name(s)'])
    body = "We're very happy that {} has decided to play in the raddest soccer league ever \nthis year. Below you'll find some necessary information about teams and practice times. \nIf you have any, issues with our decisions...well, that just sucks for you...\n".format(
        player_name)
    decree = "SO SAYETH THE MIGHTY SOCCER OVERLORD!!!\n"
    name_display = "Player Name: {}".format(player_name)
    team_display = "Team: {}".format(team_name)

    # conditionally set practice date based on team
    practice_date = ""

    if team_name.lower() == 'dragons':
        practice_date = "March 17, 1pm"
    elif team_name.lower() == 'sharks':
        practice_date = "March 17, 3pm"
    elif team_name.lower() == 'raptors':
        practice_date = "March 18, 1pm"
    else:
        practice_date = "Your kid's not on a team..."

    practice_date += "\n"

    closing = "Sincerely,\n"
    my_name = "Your friendly neighborhood SOCCER OVERLORD\n"

    # create single string from list
    letter_list = [salutation, body, decree, name_display, team_display,
                   practice_date, closing, my_name]
    letter_string = "\n".join(letter_list)

    # write the letter
    with open(filename, 'w') as letter:
        letter.write(letter_string)


if __name__ == '__main__':

    # all teams will be dictionaries with a name and players keys
    dragons = {'name': 'dragons', 'players': []}
    sharks = {'name': 'sharks', 'players': []}
    raptors = {'name': 'raptors', 'players': []}
    league = []  # the league will simply be a list of teams

    available_players = get_players_from_file(sys.argv[1])  # create list of players from file specified in command line argument

    # split all players based on experience
    experienced = []
    inexperienced = []

    for player in available_players:
        if player['Soccer Experience'] == 'YES':
            experienced.append(player)
        else:
            inexperienced.append(player)

    league.extend([sharks, dragons, raptors])  # add all teams to the league

    # distribute all players
    distribute_players(experienced, league)
    distribute_players(inexperienced, league)

    # write letters for all players
    for team in league:
        for player in team['players']:
            write_letter(player, team)

