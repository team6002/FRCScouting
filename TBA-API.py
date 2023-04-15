import gspread
import statbotics
import json
import requests
import datetime

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

gc = gspread.service_account(filename="json-files/credentials.json")

sh = gc.open("6002 ZooBOTix data sheet")
worksheet = sh.sheet1


def call_tba_api(url):
    r = requests.get(f"{TBA_BASE_ENDPOINT}/{url}", headers={"X-TBA-Auth-Key": TBA_AUTH_KEY})

    return r.json()


for event in event_keys:
    with open(f"./json-files/{event}.json") as jsonFile:
        data = json.load(jsonFile)
        for item in data:
            team = item["team_number"]
            api_data_2d.append([team])
            api_data.append(team)


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
    sheet.sort((1, "asc"), range=f"A2:A{len(api_data_2d) + 1}")
    sheet.batch_update([{"range": f"E2:E{len(team_epa_2d) + 1}", "values": team_epa_2d}])
    print(team_epa)
    print(team_epa_2d)
