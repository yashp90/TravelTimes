import requests
import re
import os
import datetime
import schedule
import json
import googlemaps
from pprint import pprint


KEY = open("gdir.key").read()
master = {}


def get_duration(origin, destination, departure_time="now"):
    today_year = str(datetime.datetime.now().year)
    today_month = str(datetime.datetime.now().month)
    today_day = str(datetime.datetime.now().day)

    options = {"origin": re.sub(" ", "+", origin), "destination": re.sub(" ", "+", destination),
               "departure_time": departure_time, "key": KEY}

    r = requests.get("https://maps.googleapis.com/maps/api/directions/json", params=options)
    print datetime.datetime.now().time(), r.url
    r_json = r.json()
    try:
        duration_in_traffic = str(r_json["routes"][0]["legs"][0]["duration_in_traffic"]["text"])
    except Exception as e:
        print e
        duration_in_traffic = ""

    if master.setdefault(today_year) is None:
        master[today_year] = {}
    if master[today_year].setdefault(today_month) is None:
        master[today_year][today_month] = {}
    if master[today_year][today_month].setdefault(today_day) is None:
        master[today_year][today_month][today_day] = {}

    now_time = datetime.datetime.now().strftime("%H:%M")
    print "At {}, it will take {} to go from {} to {}".format(
        now_time, duration_in_traffic, origin, destination)
    master[today_year][today_month][today_day].setdefault(now_time, duration_in_traffic)

    with open("times.json", "w") as times_file:
        pprint(master, stream=times_file)
        times_file.close()
    return


def main():
    with open("params.json") as f:
        params = json.load(f)
    home = params["home"]
    office = params["office "]
    morning_times = []
    evening_times = []

    for i in range(24):
        for j in range(0, 60, 5):
            evening_times.append(datetime.time(i, j).strftime("%H:%M"))
    if os.path.isfile("times.json"):
        now_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
        os.rename("times.json", "times_{}.json".format(now_time))

    for time_to_run in morning_times:
        schedule.every().day.at(time_to_run).do(get_duration, home, office)
    for time_to_run in evening_times:
        schedule.every().day.at(time_to_run).do(get_duration, office, home)

    while True:
        schedule.run_pending()


def test():
    get_duration(HOME, OFFICE)
    get_duration(OFFICE, HOME)
    print "-"
    current_time = datetime.datetime.now().time()
    current_min = current_time.minute
    print "current_time", current_time
    time_to_run = current_time.replace(minute=current_min+2).strftime("%H:%M")
    print time_to_run
    schedule.every().day.at(time_to_run).do(get_duration, "morning")

    current_time = datetime.datetime.now().time()
    current_min = current_time.minute
    print "current_time", current_time
    time_to_run = current_time.replace(minute=current_min+4).strftime("%H:%M")
    print time_to_run
    schedule.every().day.at(time_to_run).do(get_duration, "evening")
    print schedule.jobs

    while True:
        schedule.run_pending()


def test2():
    gmaps = googlemaps.Client(key=KEY)
    directions_result = gmaps.directions("Hittell Place San Jose",
                                         "905 11th Avenue Sunnyvale",
                                         departure_time="now")
    # pprint(directions_result)
    print directions_result[0]["legs"][0]["duration"]["text"]


if __name__ == "__main__":
    # test()
    test2()
    # main()
