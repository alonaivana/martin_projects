from api import get_data, get_token
from sql import add_data_MSSQL, create_list, get_last_update_date
from check_unique import get_visit_ids, create_list_id, get_duplicates
from datetime import date, timedelta
from settings import DAY_DELTA


def visits():
    try:
        # Получение токена для получения доступа к данным
        access_token = get_token()

        # Узнаём дату на три дня назад, чтобы выгрузить отчёт
        today = date.today()
        final_report_day = today - timedelta(days=DAY_DELTA)

        # Узнаём дату последнего обновления базы данных
        last_update_date = get_last_update_date()

        # Загрузка данных до final_report_day
        while last_update_date <= final_report_day:
            # Получение данных (суточного отчёта)
            data = get_data(access_token, last_update_date)

            # Получение листа ID визитов из базы данных
            visit_ids = get_visit_ids()

            # Получение листа новых ID визитов (из тех, которые хотим добавить)
            new_ids = create_list_id(data)

            # Получение кортежа повторяющихся ID визитов
            duplicates = get_duplicates(visit_ids, new_ids)

            # Преобразования словаря в кортеж для внесения в SQL-таблицу
            data_list = create_list(data, duplicates)

            # Загрузка данных в базу данных SQL Server
            add_data_MSSQL(data_list)

            last_update_date = last_update_date + timedelta(days=1)
    except BaseException:
        return None


if __name__ == "__main__":
    visits()
