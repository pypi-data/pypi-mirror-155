import pkgutil
import requests


# Example function
def add_one(number):
    return number + 1


# Example using a dependancy
def get_google_response_status_code():
    return requests.get("https://www.google.com").status_code


# Example using a data file that comes with the package
def get_txt_data():
    data = pkgutil.get_data(__package__, "./data/data.txt")
    return data.decode("utf-8")