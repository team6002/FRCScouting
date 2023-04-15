import gspread
import statbotics
import json
import requests
import datetime

constants = open("./json-files/constants.json")
constant = json.load(constants)
constants.close()
team_number_column = constant["team_number_column"]
team_name_column = constant["team_name_column"]
team_state_column = constant["team_state_column"]
team_divison_column = constant["team_divison_column"]
team_epa_column = constant["team_epa_column"]
team_winrate_column = constant["team_winrate_column"]

auth_key = open("./json-files/X-TBA-Auth-Key.json")
key = json.load(auth_key)
auth_key.close()

stats = statbotics.Statbotics()
TBA_AUTH_KEY = key["key"]
TBA_BASE_ENDPOINT = "https://www.thebluealliance.com/api/v3"

gc = gspread.service_account(filename="json-files/credentials.json")

# Open a sheet from a spreadsheet in one go
sheet = gc.open("6002 ZooBOTix data sheet").sheet1

api_data_2d = [

]

api_data = [

]

team_names = [

]

team_names_2d = [

]

event_keys = [
    "2023arc",
    "2023cur",
    "2023dal",
    "2023gal",
    "2023hop",
    "2023joh",
    "2023mil",
    "2023new",
]

team_epa = [

]

team_epa_2d = [

]

team_winrate = [

]

team_winrate_2d = [

]

gc = gspread.service_account(filename="json-files/credentials.json")

sh = gc.open("6002 ZooBOTix data sheet")
worksheet = sh.sheet1

for event in event_keys:
    with open(f"./json-files/{event}.json") as jsonFile:
        data = json.load(jsonFile)
        for item in data:
            team = item["team_number"]
            api_data_2d.append([team])
            api_data.append(team)
    jsonFile.close()


def call_tba_api(url):
    r = requests.get(f"{TBA_BASE_ENDPOINT}/{url}", headers={"X-TBA-Auth-Key": TBA_AUTH_KEY})

    return r.json()


def update_event_json():
    for event in event_keys:
        with open(f"./json-files/{event}.json", "w+") as jsonFile:
            data = call_tba_api(f"/event/{event}/teams")
            print(json.dumps(data))
            jsonFile.write(json.dumps(data))


def update_team_list(update_sheet):
    update_event_json()
    for event in event_keys:
        with open(f"./json-files/{event}.json") as jsonFile:
            data = json.load(jsonFile)
            for item in data:
                api_data.append(item["team_number"])
                api_data_2d.append([item["team_number"]])
                print(item["team_number"])
    api_data.sort()
    api_data_2d.sort()
    print(api_data)
    print(api_data_2d)
    if update_sheet is True:
        sheet.batch_update([{
            "range": f"{team_number_column}2:{team_number_column}{len(api_data) + 1}",
            "values:": api_data_2d
        }])
    for team in api_data:
        for item in data:
            team_names.append(item["nickname"])
            team_names_2d.append([item["nickname"]])
            print(item["nickname"])
    if update_sheet is True:
        sheet.batch_update([{
            "range": f"{team_name_column}2:{team_name_column}{len(api_data) + 1}",
            "values": team_names_2d
        }])
    print(team_names)
    print(team_names_2d)


def update_epa():
    api_data.sort()
    api_data_2d.sort()
    for team in api_data:
        team_data = stats.get_team(team)
        epa = team_data["norm_epa"]
        rookie_year = team_data["rookie_year"]
        rookies = datetime.date.today().year == int(rookie_year)
        if epa is None:
            epa = "N/A"
        else:
            epa = round(epa / 28.1702899, 1)
        print(f"team: {team}, epa: {epa}, rookies?: {rookies}")
        team_epa.append(epa)
        team_epa_2d.append([epa])
    sheet.sort((1, "asc"), range=f"{team_number_column}2:{team_number_column}{len(api_data_2d) + 1}")
    sheet.batch_update([{"range": f"{team_epa_column}2:{team_epa_column}{len(team_epa_2d) + 1}", "values": team_epa_2d}])
    print(team_epa)
    print(team_epa_2d)


def update_winrate():
    for team in api_data:
        winrate = stats.get_team(team)["winrate"]
        team_winrate.append(f"{round(winrate * 100, 1)}%")
        team_winrate_rounded = f"{round(winrate * 100, 1)}%"
        team_winrate_2d.append([team_winrate_rounded])
        print(f"{round(winrate * 100, 2)}%")
    print(team_winrate)
    print(team_winrate_2d)
    sheet.batch_update([{
        "range": f"{team_winrate_column}2:{team_winrate_column}{len(api_data) + 1}",
        "values": team_winrate_2d
    }])


update_team_list(False)
