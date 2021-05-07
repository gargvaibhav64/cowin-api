import requests
from datetime import datetime, timedelta
import smtplib, ssl

state_name = "Maharashtra"
dist_name = "Mumbai"

headers = {
    'Accept-Language':'en_US',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

response_states = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/states", headers = headers).json()

state_id = 0 

for state in response_states['states']:
    if(state["state_name"] == state_name):
        state_id = state["state_id"]
        print(state["state_name"] + " : " + str(state["state_id"]))


dist_url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/" + str(state_id)

response_district = requests.get(dist_url, headers = headers).json()

# print(response_district['districts'])

district_id = 0

for district in response_district['districts']:
    if(district["district_name"] == dist_name):
        district_id = district["district_id"]
        print(district["district_name"] + " : " + str(district["district_id"]))

# print(response_states.json())
# print(response.url)
# jprint(response.json())

today = datetime.today().strftime('%d-%m-%Y')

parameters = {
    'district_id': district_id, 
    'date': today
}

for i in range(0,4):
    today = (datetime.today() + timedelta(i*7)).strftime('%d-%m-%Y')

    parameters = {
        'district_id': district_id, 
        'date': today
    }

    appointment = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict", headers = headers, params = parameters).json()

    for center in appointment["centers"]:
        for session in center["sessions"]:
            if(session["min_age_limit"] == 18 and session["available_capacity"] > 0):
                print(center["name"] + " " + session["date"])

# today = (datetime.today() + timedelta(7)).strftime('%d-%m-%Y')




# print(today)

# print(appointment)