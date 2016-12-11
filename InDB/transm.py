import sqlite3
import os
import json
import datetime as d


def read_folder():
    """return json names"""
    json_files = os.listdir("JSON")
    return json_files


def read_one(f):
    """reades one file and saves it"""
    with open("JSON/" + f) as bike_json:
        b_dict = json.load(bike_json)  # b_dict ist das dokument als dict
        return b_dict


def filter(j_dict, date):
    """ Filters Latitude, Longitude and Bike ID from JSON file"""

    date = str(date).split("date")[0]
    markers = j_dict["marker"]
    data_tuples = []
    for marker in markers:
        latitude = float(marker["lat"])
        longitude = float(marker["lng"])
        bikelist = marker["hal2option"]["bikelist"]
        street = marker["hal2option"]["tooltip"]
        street = ((street.replace("&nbsp", "")).replace(";", "")).\
            replace("'", "")
        streets = str(street.split("/"))
        for bike in bikelist:
            data_tuples.append((int(bike["Number"]), streets, latitude,
                                longitude, date))
    return data_tuples


def makedate(city_ts):
    """ Filters date from file name"""
    splitted_city_ts = city_ts.split("-")
    # city = splitted_city_ts[0]  not necessary
    year = int(splitted_city_ts[1])
    month = int(splitted_city_ts[2])
    day = int(splitted_city_ts[3].split("T")[0])
    '''Building timestamp out of year, month and day'''
    date = d.date(year, month, day)
    return date


class DBClass():

    def __init__(self):
        self.bikedb = sqlite3.connect('infovisdb.db')
        self.cursor = self.bikedb.cursor()

    def insert(self, data_tuples):
        """ Inserts tuples into db"""
        for t in data_tuples:
            command = "INSERT INTO Bike VALUES " + str(t)
            print(command)
            self.cursor.execute(command)
            self.bikedb.commit()

    def close(self):
        self.cursor.close()


if __name__ == '__main__':
    mydb = DBClass()
    json_files = read_folder()
    for f in json_files:
        city_ts = f
        j_dict = read_one(f)
        date = makedate(city_ts)
        data_tuples = filter(j_dict, date)
        mydb.insert(data_tuples)
        print("-------------------------------------Commit done---------------"
              "--------------------")