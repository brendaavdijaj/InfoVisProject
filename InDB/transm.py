import sqlite3
import os
import json
import datetime as d
import time
import uuid


def gen_name():
    return uuid.uuid4()

def read_folder(name):
    """return json names"""
    json_folders = os.listdir(name)
    return json_folders


def read_one(f, filename):
    """reades one file and saves it"""
    with open("JSON/" + filename + "/" + f) as bike_json:
        b_dict = json.load(bike_json)  # b_dict ist das dokument als dict
        return b_dict


def filter(j_dict, ts):
    """ Filters Latitude, Longitude and Bike ID from JSON file"""

    ts = int(ts)
    markers = j_dict["marker"]
    data_tuples = []
    for marker in markers:
        latitude = float(marker["lat"])
        longitude = float(marker["lng"])
        bikelist = marker["hal2option"]["bikelist"]
        street = marker["hal2option"]["tooltip"]
        street = ((street.replace("&nbsp", "")).replace(";", "")).replace("'",
                                                                          "")
        streets = str(street.split("/"))
        for bike in bikelist:
            u_id = str(bike["Number"]) + "_" + str(ts)
            data_tuples.append((int(bike["Number"]), streets, latitude,
                                longitude, ts, u_id))
    return data_tuples


def makedate(city_ts):
    """ Filters date from file name"""
    splitted_city_ts = city_ts.split("-")
    # city = splitted_city_ts[0]  not necessary
    year = splitted_city_ts[1]
    month = splitted_city_ts[2]
    day = splitted_city_ts[3].split("T")[0]
    '''Building timestamp out of year, month and day'''
    time_part = splitted_city_ts[-1].split("T")[1].split("+")[0]
    time_part = time_part.split("_")
    hours = time_part[0]
    minutes = time_part[1]
    seconds = time_part[2]

    t_d_str = year + "-" + month + "-" + day + " " + hours + ":" + minutes +\
              ":" + seconds
    date_time = d.datetime.strptime(t_d_str, '%Y-%m-%d %H:%M:%S')
    ts = time.mktime(date_time.timetuple())

    return ts


def write_to_json(data_tuples, foldername):
    # number , streets, lat, long, ts, u_id

    name = str(gen_name()) + ".json"
    data_dict = {}

    for t in data_tuples:
        dict = {"Number": t[0], "Streets": t[1],
                "Latitude": t[2], "Longitude": t[3], "Timestamp": t[4]}
        # "UniqueId": t[4]}
        data_dict[t[5]] = dict

    with open("results/" + foldername + "/" + name, 'w') as bike_j:
        json.dump(data_dict, bike_j, indent=4,
                  sort_keys=True)
    bike_j.close()


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
    # mydb = DBClass()

    json_folders = read_folder('JSON')
    for f in json_folders:
        json_files = read_folder('JSON/' + f)
        foldername = str(gen_name())
        os.makedirs("results/" + foldername)
        for e in json_files:
            city_ts = e
            j_dict = read_one(e, f)
            ts = makedate(city_ts)
            data_tuples = filter(j_dict, ts)

            write_to_json(data_tuples, foldername)
            # mydb.insert(data_tuples)

    print("finished")