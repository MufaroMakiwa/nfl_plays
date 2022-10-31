import csv
import json


def construct_data_set(game_id: str, play_id: str):
    FRAME_ID = "frameId"
    TEAM = "team"
    DISPLAY_NAME = "displayName"
    X = "x"
    Y = "y"
    NFL_ID = "nflId"
    OFFICIAL_POSITION = "officialPosition"
    PFF_ROLE = "pff_role"
    PLAY_ID = "playId"
    GAME_ID = "gameId"
    WEEK = "week"

    # get the game data from games.csv
    week = None
    with open("games.csv", "r") as f:
        for game in csv.DictReader(f):
            if game[GAME_ID] == game_id:
                week = game[WEEK]
                break
        else:
            raise KeyError(f"game with gameID - {game_id} - not found")

    # get play details from plays.csv
    with open("plays.csv", "r") as f:
        for play in csv.DictReader(f):
            if play[PLAY_ID] == play_id:
                break
        else:
            raise KeyError(f"play with playID - {play_id} - not found")

    # get pffScoutingData for given play
    with open("pffScoutingData.csv", "r") as f:
        scouting_data = {
            row[NFL_ID]: row[PFF_ROLE] for row in csv.DictReader(f) if row[PLAY_ID] == play_id
        }

    # get the players details for the teams playing
    with open("players.csv", "r") as f:
        players = {
            player[NFL_ID]: {
                OFFICIAL_POSITION: player[OFFICIAL_POSITION],
                DISPLAY_NAME: player[DISPLAY_NAME]
            } for player in csv.DictReader(f)
        }

    # read data from the game week
    with open(f"week{week}.csv", "r") as f:
        data = [
            {
                FRAME_ID: int(event[FRAME_ID]),
                TEAM: event[TEAM],
                X: float(event[X]),
                Y: float(event[Y]),
                NFL_ID: int(event[NFL_ID]) if event[TEAM] != "football" else "",
                DISPLAY_NAME: players[event[NFL_ID]][DISPLAY_NAME] if event[TEAM] != "football" else "football",
                OFFICIAL_POSITION: players[event[NFL_ID]][OFFICIAL_POSITION] if event[TEAM] != "football" else "",
                PFF_ROLE: scouting_data[event[NFL_ID]] if event[TEAM] != "football" else ""
            }
            for event in csv.DictReader(f) if event[PLAY_ID] == play_id
        ]

    # save data to json
    with open(f"{game_id}_{play_id}.json", "w") as f:
        json.dump(data, f)


if __name__ == '__main__':
    plays = {
        "2021090900": ["97", "137", "187"],
        "2021091600": ["65", "187", "235"],
        "2021100700": ["95", "165", "227"]
    }
    for game_, play_ids in plays.items():
        for _id in play_ids:
            construct_data_set(game_, _id)
