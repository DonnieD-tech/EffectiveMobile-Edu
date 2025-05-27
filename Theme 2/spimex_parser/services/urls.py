from datetime import timedelta, datetime

import requests


def check_url_exists(url):
    try:
        resp = requests.head(url, timeout=5)
        return resp.status_code == 200
    except requests.RequestException:
        return False

def generate_spimex_urls(start_date, end_date):
    urls = []
    date = start_date
    while date <= end_date:
        filename = f"oil_xls_{date.strftime('%Y%m%d')}162000.xls"
        url = f"https://spimex.com/upload/reports/oil_xls/{filename}"
        urls.append(url)
        date += timedelta(days=1)
    return urls

def find_all_spimex_files():
    print('Start processing URLs.')
    start_date = datetime(2023, 1, 1)
    end_date = datetime.now()

    all_urls = generate_spimex_urls(start_date, end_date)
    existing_urls = []


    for url in all_urls:
        if check_url_exists(url):
            existing_urls.append(url)
            print(f'XLS found on: {url}')

    print(f"Total URLs: {len(existing_urls)}")
    return existing_urls