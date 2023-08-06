import os
import requests

# Example function
def add_one(number):
    return number + 1


# Example using a dependancy
def get_google_response_status_code():
    return requests.get("https://www.google.com").status_code


# Example using a data file that comes with the package
def get_txt_data():
    this_dir, this_file = os.path.split(__file__)
    txt_file_path = os.path.join(this_dir, "data", "data.txt")

    with open(txt_file_path, "r") as txt_file:
        return txt_file.read()