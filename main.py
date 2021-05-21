import requests, requests_cache
from datetime import datetime, timedelta
import time
from tele import telegram_bot_sendtext

state_name = "Madhya Pradesh"
dist_name = "Morena"

requests_cache.install_cache('cowin_cache', expire_after=6000)

headers = {
    'Accept-Language':'en_US',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

response_states = None
response_districts = None

def get_list_of_state_codes():
    response_states = None

    if not response_states:
        response_states = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/states", headers = headers)
        print("State Code Req: Time: {0} / Used Cache: {1}".format(datetime.now(), response_states.from_cache))
        response_states = response_states.json()

    return response_states

def get_list_of_district_codes(state_id):
    if not state_id:
        return None

    dist_url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/" + str(state_id)
    
    response_districts = requests.get(dist_url, headers = headers)
    print("District Code Req: Time: {0} / Used Cache: {1}".format(datetime.now(), response_districts.from_cache))
    response_districts = response_districts.json()

    return response_districts

def get_state_id_from_name(state_name):

    state_id = None

    global response_states

    for state in response_states['states']:
        if(state["state_name"] == state_name):
            state_id = state["state_id"]
            # print(state["state_name"] + " : " + str(state["state_id"]))

    return state_id

def get_district_id_from_name(dist_name):

    district_id = None

    global response_district

    for district in response_district['districts']:
        if(district["district_name"] == dist_name):
            district_id = district["district_id"]
            # print(district["district_name"] + " : " + str(district["district_id"]))

    return district_id

def check_slots(state_name, dist_name):

    print("Checking slots for " + state_name + ": " + dist_name + "...")

    global response_states, response_district

    response_states = get_list_of_state_codes()
    state_id = get_state_id_from_name(state_name)
    response_district = get_list_of_district_codes(state_id)
    district_id = get_district_id_from_name(dist_name)
    today = datetime.today().strftime('%d-%m-%Y')

    parameters = {
        'district_id': district_id, 
        'date': today
    }

    flag = 0

    for i in range(0,4):
        today = (datetime.today() + timedelta(i*7)).strftime('%d-%m-%Y')

        parameters = {
            'district_id': district_id, 
            'date': today
        }

        with requests_cache.disabled():
            appointment = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict", headers = headers, params = parameters).json()


        # print(appointment)

        if "errors" in appointment:
            print("Error occurred. Retrying")
            continue

        for center in appointment["centers"]:
            for session in center["sessions"]:
                if(session["min_age_limit"] == 18 and session["available_capacity"] > 0):
                    flag = 1
                    print(telegram_bot_sendtext(center["name"] + ": " + session["date"] + ". Available Slots: " + str(session["available_capacity"]) + " Last Updated at: " + str(datetime.now())))

    if flag == 0:
        print("No slots found.")

# state_name = input("Enter State Name: ")
# dist_name = input("Enter District Name: ")

while(1):
    check_slots(state_name, dist_name)
    time.sleep(60)