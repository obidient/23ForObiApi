import csv
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def generate_lga_objects():
    list_of_lgas = []
    with open(BASE_DIR + "/local_government_id.csv", "r") as csvfile:
        for row in csvfile:
            row = row.split(",")
            list_of_lgas.append(
                {
                    "sn": row[0],
                    "name": row[1],
                    "location_id": row[2].split("\n")[0],
                }
            )
    return list_of_lgas
