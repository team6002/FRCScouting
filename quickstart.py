import gspread
import json
import requests
import time

auth_key = open("./json-files/X-TBA-Auth-Key.json")
key = json.load(auth_key)
auth_key.close()

TBA_AUTH_KEY = key["key"]
TBA_BASE_ENDPOINT = "https://www.thebluealliance.com/api/v3"

gc = gspread.service_account(filename="json-files/credentials.json")

# Open a sheet from a spreadsheet in one go
sheet = gc.open("6002 ZooBOTix data sheet").sheet1

api_data_2d = [

]

api_data = [

]

team_name_2d = [

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

parent_event_keys = [
    "archemides",
    "curie",
    "daly",
    "galileo",
    "hopper",
    "johnson",
    "milstein",
    "newton",
]

team_stateprov = [

]

gc = gspread.service_account(filename="json-files/credentials.json")

sh = gc.open("6002 ZooBOTix data sheet")
worksheet = sh.sheet1


def call_tba_api(url):
    r = requests.get(f"{TBA_BASE_ENDPOINT}/{url}", headers={"X-TBA-Auth-Key": TBA_AUTH_KEY})

    return r.json()


i = -1
division = None

for event in event_keys:
    i = i + 1
    division = parent_event_keys[i]
    with open(f"json-files/{event}.json") as jsonFile:
        data = json.load(jsonFile)
        for x in data:
            team_number = x["team_number"]
            api_data_2d.append([team_number])
            row = sheet.find(f"{team_number}", in_column=1).row
            print(f"{team_number} : {row} : {division}")
            sheet.update(f"D{row}", f"{division}")
            time.sleep(1)
        api_data_2d.sort()
        print(api_data_2d)

# TODO: fix confusing code below
    for team in api_data_2d:
        team_key = f"frc{team}"
        events = call_tba_api(f"team/{team_key}/events/2023")
        for event in events:
            if event["event type"] == 5 and not event["parent_event_key"] == "null":
                event_keys.append([event["parent_event_key"]])

        for event_key in event_keys:
            matches = call_tba_api(f"team/{team_key}/event/{event_key}/matches")
            for match in matches["alliances"]:
                for blue_alliance in matches:
                    for alliance_partner in blue_alliance["team_keys"]:
                        if alliance_partner == f"{team_key}":
                            alliance = "blue"
                        else:
                            alliance = "red"
