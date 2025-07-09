from datetime import timedelta, datetime


def generate_spimex_urls(start_date, end_date):
    urls = []
    date = start_date
    while date <= end_date:
        filename = f"oil_xls_{date.strftime('%Y%m%d')}162000.xls"
        url = f"https://spimex.com/upload/reports/oil_xls/{filename}"
        urls.append(url)
        date += timedelta(days=1)
    return urls


async def find_all_spimex_files():
    print('Start processing URLs.')
    start_date = datetime(2023, 1, 1)
    end_date = datetime.now()
    all_urls = generate_spimex_urls(start_date, end_date)
    print(f"Сгенерировано {len(all_urls)} URLs.")
    return all_urls