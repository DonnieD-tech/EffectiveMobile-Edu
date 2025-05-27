from models.database import create_db
from services.parser import parse_excel_file
from services.urls import find_all_spimex_files

create_db()

if __name__ == '__main__':
    urls = find_all_spimex_files()
    parse_excel_file.cnt = 0
    for url in urls:
        parse_excel_file(url)
    print('Processing complete.')

