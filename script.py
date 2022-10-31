import csv
import json

colors = {
    'ARI': "#97233F",
    'ATL': "#A71930",
    'BAL': '#241773',
    'BUF': "#00338D",
    'CAR': "#0085CA",
    'CHI': "#C83803",
    'CIN': "#FB4F14",
    'CLE': "#311D00",
    'DAL': '#003594',
    'DEN': "#FB4F14",
    'DET': "#0076B6",
    'GB': "#203731",
    'HOU': "#03202F",
    'IND': "#002C5F",
    'JAX': "#9F792C",
    'KC': "#E31837",
    'LA': "#003594",
    'LAC': "#0080C6",
    'LV': "#000000",
    'MIA': "#008E97",
    'MIN': "#4F2683",
    'NE': "#002244",
    'NO': "#D3BC8D",
    'NYG': "#0B2265",
    'NYJ': "#125740",
    'PHI': "#004C54",
    'PIT': "#FFB612",
    'SEA': "#69BE28",
    'SF': "#AA0000",
    'TB': '#D50A0A',
    'TEN': "#4B92DB",
    'WAS': "#5A1414",
    'football': '#CBB67C'
}


def construct_data_set(game_id: str, play_id: str):
    FRAME_ID = "frameId"
    TEAM = "team"
    DISPLAY_NAME = "displayName"
    X = "x"
    Y = "y"
    NFL_ID = "nflId"
    OFFICIAL_POSITION = "officialPosition"
    PFF_ROLE = "pff_role"
    PLAY_DESCRIPTION = "playDescription"
    QUARTER = "quarter"
    GAME_CLOCK = "gameClock"
    PLAY_ID = "playId"
    GAME_ID = "gameId"
    GAME_DATE = "gameDate"
    WEEK = "week"
    COLOR = "color"

    # get the game data from games.csv
    game_date, week = None, None
    with open("games.csv", "r") as f:
        for game in csv.DictReader(f):
            if game[GAME_ID] == game_id:
                game_date = game[GAME_DATE]
                week = game[WEEK]
                break
        else:
            raise KeyError(f"game with gameID - {game_id} - not found")

    # get play details from plays.csv
    play_description, quarter, game_clock = None, None, None
    with open("plays.csv", "r") as f:
        for play in csv.DictReader(f):
            if play[PLAY_ID] == play_id:
                play_description = play[PLAY_DESCRIPTION]
                quarter = play[QUARTER]
                game_clock = play[GAME_CLOCK]
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
    files = {
        "2021090900": ["97", "137", "187"],
        "2021091600": ["65", "187", "235"],
        "2021100700": ["95", "165", "227"]
    }
    for game, play_ids in files.items():
        for _id in play_ids:
            construct_data_set(game, _id)
