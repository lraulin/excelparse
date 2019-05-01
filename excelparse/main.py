import os
import pandas as pd
import requests
import urllib3

def save_to_xlsx(df):
    writer = pd.ExcelWriter('example.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})
    df.to_excel(writer, 'Sheet1')

def request_status(url):
    print(f'Checking {url}...')
    try: 
        r = requests.get(url, timeout=5)
        print(r.status_code)
        return r.status_code
    except requests.exceptions.ConnectionError:
        print("ConnectionError")
        return "FAIL"
    except urllib3.exceptions.ReadTimeoutError:
        print("Timed out")
        return "TIMEOUT"
    except:
        pass

def write_list(my_list):
    with open('your_file.txt', 'w') as f:
        for item in my_list:
            f.write("%s\n" % item)

def check_websites():
    file = "FOUO-USDOT-website list 20190413.xlsx"
    xl = pd.ExcelFile(file)
    df = xl.parse('Source-Live Websites w Owners')
    column = df.loc[:, 'Canonical URL']
    urls = [x for x in column]
    statuses = [request_status(x) for x in urls]
    live = ['Yes' if x == 200 else 'No' for x in statuses]
    write_list(live)
    return live

def main():
    statuses = check_websites()
    df.insert(4, 'Live', statuses)
    save_to_xlsx(df)

if __name__ == "__main__":
    main()