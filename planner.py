import os
import csv
import argparse

class Planner:
    def __init__(self, city):
        self.city = city
        self.resort_data = "data/resorts.csv"
        self.city_data = "data/us_cities.csv"

    def get_city_info(self):
        with open(self.city_data, 'r') as cities:
            reader = csv.reader(cities)
            for row in reader:
                print(row)
        return
    
    def get_resorts(self):
        return

    def get_mountains(self, range):
        long, lat = self.get_city_info()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--city", required=True, help="Destination to begin looking")
    parser.add_argument("-r", "--range", required=False, help="Range in miles of mountains to look for", default="50")
    args = parser.parse_args()
    planner = Planner(args.city)
    mountains = planner.get_mountains(args.range)
    print(f"Mountains: {mountains}")