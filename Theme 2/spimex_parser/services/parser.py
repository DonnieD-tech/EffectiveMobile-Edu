import requests
from datetime import datetime
import re
import xlrd
from models.spimex_trading_results_model import SpimexTradingResult
from models.database import SessionLocal

cnt = 1;

def normalize_header(name):
    if not name:
        return ""
    return name.replace("\n", " ").strip()


def extract_date_from_url(url):
    match = re.search(r"oil_xls_(\d{8})\d{6}", url)
    if match:
        try:
            return datetime.strptime(match.group(1), "%Y%m%d").date()
        except ValueError:
            pass
    return None


def parse_excel_file(file_url):
    parse_excel_file.cnt += 1
    print(f'Processing [XLS #{parse_excel_file.cnt}]: {file_url}')
    resp = requests.get(file_url)
    wb = xlrd.open_workbook(file_contents=resp.content)

    session = SessionLocal()

    sheet_names = wb.sheet_names()
    for sheet_name in sheet_names:
        ws = wb.sheet_by_name(sheet_name)

        rows = [ws.row_values(i) for i in range(ws.nrows)]

        found_table = False
        headers = []
        header_row_index = None

        for i, row in enumerate(rows):
            row_str = " ".join(str(cell) if cell else "" for cell in row)
            if not found_table and "Единица измерения: Метрическая тонна" in row_str:
                found_table = True
                continue

            if found_table and any(cell for cell in row):
                headers = [normalize_header(str(cell)) for cell in row]
                header_row_index = i

                header_map = {key: idx for idx, key in enumerate(headers)}
                required_columns = [
                    "Код Инструмента",
                    "Наименование Инструмента",
                    "Базис поставки",
                    "Объем Договоров в единицах измерения",
                    "Обьем Договоров, руб.",
                    "Количество Договоров, шт."
                ]
                missing_cols = [col for col in required_columns if col not in header_map]
                if missing_cols:
                    headers = []
                    break
                break

        if not headers:
            continue

        for row in rows[header_row_index + 1:]:
            count_cell = row[header_map["Количество Договоров, шт."]]
            if not count_cell or count_cell in ("-", "", 0):
                continue

            exchange_product_id = str(row[header_map["Код Инструмента"]]).strip()
            obj = SpimexTradingResult(
                exchange_product_id=exchange_product_id,
                exchange_product_name=row[header_map["Наименование Инструмента"]],
                oil_id=exchange_product_id[:4],
                delivery_basis_id=exchange_product_id[4:7],
                delivery_type_id=exchange_product_id[-1],
                delivery_basis_name=row[header_map["Базис поставки"]],
                volume=float(row[header_map["Объем Договоров в единицах измерения"]]) if row[header_map["Объем Договоров в единицах измерения"]] not in ("-", "") else 0.0,
                total=float(row[header_map["Обьем Договоров, руб."]]) if row[header_map["Обьем Договоров, руб."]] not in ("-", "") else 0.0,
                count=int(count_cell),
                date=extract_date_from_url(file_url),
            )
            session.add(obj)


    session.commit()
    session.close()

    print(f"Processing done.")



