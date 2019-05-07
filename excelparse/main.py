import os
import pandas as pd
import requests
import urllib3
from shutil import copyfile
import sys
import requests
from openpyxl import Workbook, load_workbook
import json

TIMEOUT = 15
FILE_NAME = "FOUO-USDOT-website list 20190413.xlsx"
SHEET_NAME = "Source-Live Websites w Owners"
OUTPUT_FILE = "your_file.txt"

def save_to_xlsx():
    wb = load_workbook(FILE_NAME)
    sheet = wb[SHEET_NAME]

def check_for_redirects(url):
    print(f"Checking {url}...")
    result = {
        "url": url,
        "status_code": None,
        "message": None,
        "r_url": None
    }
    try:
        r = requests.get(url, allow_redirects=False, timeout=TIMEOUT)
        result["status_code"] = r.status_code
        print(f"Status Code: {r.status_code}")
        if 300 <= r.status_code < 400:
            result["r_url"] = r.headers['location']
            print(f"Location: {r.headers['location']}")
        else:
            result["message"] = '[no redirect]'
            print('No Redirect')
    except requests.exceptions.Timeout:
        print("Timeout")
        result["message"] = f'[timeout after {TIMEOUT} s]'
    except requests.exceptions.ConnectionError:
        print("Connection Error")
        result["message"] = '[connection error]'
    finally:
        return result


def write_list(my_list):
    with open('your_file.txt', 'w') as f:
        for item in my_list:
            f.write("%s\n" % item)

def check_websites(column_header):
    xl_file = pd.ExcelFile(FILE_NAME)
    data_frame = xl_file.parse('Source-Live Websites w Owners')
    column = data_frame.loc[:, column_header]
    urls = [x for x in column]
    statuses = [check_for_redirects(x) for x in urls]
    return statuses

def modify_xlsx():
    lines = [line.rstrip('\n') for line in open(OUTPUT_FILE)]
    xl_file = pd.ExcelFile(FILE_NAME)
    data_frame = xl_file.parse(SHEET_NAME)
    data_frame.insert(4, 'Live', lines)
    writer = pd.ExcelWriter(FILE_NAME, engine='xlsxwriter', options={'strings_to_urls': False})
    data_frame.to_excel(writer, SHEET_NAME)

def main():
    statuses = check_websites('Canonical URL')
    with open('url_responses.json', 'w') as f:
        json.dump(statuses, f)
    # save_to_xlsx()

if __name__ == "__main__":
    main()