#!/usr/bin/python3

import csv
import argparse
from pathlib import Path
from decimal import Decimal
from math import radians, sin, cos, sqrt, atan2

class Planner:
    def __init__(self, city, state):
        self.city = city
        self.state = self.map_state_code(state) if len(state) > 2 else state
        self.base_dir = Path(__file__).resolve().parent
        self.resort_data = self.base_dir/"data"/"resorts.csv"
        self.city_data = self.base_dir/"data"/"us_cities.csv"

    def map_state_code(self, state):
        state_map = {'alabama':'AL','alaska':'AK','arizona':'AZ','arkansas':'AR','california':'CA','colordado':'CO','connecticut':'CT',
                     'delaware':'DE','florida':'FL','georgia':'GA','hawaii':'HI','idaho':'ID','illinois':'IL','indiana':'IN','iowa':'IA',
                     'kansas':'KS','kentucky':'KY','louisiana':'LA','maine':'ME','maryland':'MD','massachusetts':'MA','michigan':'MI',
                     'minnesota':'MN','mississippi':'MS','missouri':'MO','montana':'MT','nebraska':'NE','nevada':'NV','new Hampshire':'NH',
                     'new Jersey':'NJ','new Mexico':'NM','new York':'NY','north Carolina':'NC','north Dakota':'ND','ohio':'OH','oklahoma':'OK',
                     'oregon':'OR','pennsylvania':'PA','rhode Island':'RI','south Carolina':'SC','south Dakota':'SD','tennessee':'TN','texas':'TX',
                     'utah':'UT','vermont':'VT','virginia':'VA','washington':'WA','west Virginia':'WV','wisconsin':'WI','wyoming':'WY'}
        return state_map[state.lower()]

    def get_city_info(self):
        with open(self.city_data, 'r') as cities:
            reader = csv.reader(cities)
            next(reader)
            for row in reader:
                if row[3].lower() == self.city.lower() and row[1].lower() == self.state.lower():
                    return {row[3]: {'ID':row[0],'STATE_CODE':row[1],
                                     'STATE_NAME':row[2],'COUNTY':row[4],
                                     'LATITUDE':row[5],'LONGITUDE':row[6]}}
    
    def calculate_distance(self, res_long, city_long, res_lat, city_lat, range):
        earth_radius = 3958.8
        city_lat, city_long, res_lat, res_long = map(radians, [city_lat, city_long, res_lat, res_long])
        lat_distance = res_lat - city_lat
        long_distance = res_long - city_long
        haversine = sin(lat_distance/2)**2+cos(city_lat)*cos(res_lat)*sin(long_distance/2)**2
        cen_angle = 2*atan2(sqrt(haversine), sqrt(1-haversine))
        distance = earth_radius*cen_angle
        if Decimal(distance) <= Decimal(range):
            return True
        return False
    
    def get_resorts(self, city_info, range):
        resort_list = []
        city_long = Decimal(city_info[self.city]['LONGITUDE'])
        city_lat = Decimal(city_info[self.city]['LATITUDE'])
        with open(self.resort_data, 'r') as resorts:
            reader = csv.reader(resorts)
            next(reader)
            for row in reader:
                res_long = Decimal(row[3])
                res_lat = Decimal(row[2])
                if self.calculate_distance(res_long, city_long, res_lat, city_lat, range):
                    resort_list.append({'RESORT_NAME':row[0],'PARTNER':bool(row[1]),'LATITUDE':row[2],':LONGITUDE':row[3]})
        return resort_list

    def get_mountains(self, range):
        resorts = []
        city_info = self.get_city_info()
        resorts_in_range = self.get_resorts(city_info, range)
        for resort in resorts_in_range:
            resorts.append(resort['RESORT_NAME'])
        return resorts

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--city", required=True, help="Destination to begin looking")
    parser.add_argument("-s", "--state", required=True, help="State of city to begin looking")
    parser.add_argument("-r", "--range", required=False, help="Range in miles of mountains to look for", default="50")
    args = parser.parse_args()
    planner = Planner(args.city, args.state)
    mountains = planner.get_mountains(args.range)
    print(f"Mountains: {mountains}")