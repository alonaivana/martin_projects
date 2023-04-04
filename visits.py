from api import get_data, get_token
from sql import add_data_MSSQL, create_list, get_last_update_date
from sql import create_list_people, add_data_MSSQL_people
from check_unique import get_visit_ids, create_list_id, get_duplicates
from new_people import get_people_ids, create_list_people_id
from new_people import get_dup_people
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

            # Получение листа ID мерчандайзеров из базы данных
            people_ids = get_people_ids()

            # Получение листа ID мерчандайзеров из ответа WODO
            new_people_ids = create_list_people_id(data)

            # Получение кортежа повторяющихся ID мерчандайзеров
            duplicates_people = get_dup_people(people_ids, new_people_ids)

            # Преобразования словаря в кортеж для внесения в SQL-таблицу
            # (с ограничением на уникальный ID мерчандайзера)
            data_people_list = create_list_people(data, duplicates_people)

            # Загрузка данных в базу данных SQL Server
            add_data_MSSQL_people(data_people_list)

            # Получение листа ID визитов из базы данных
            visit_ids = get_visit_ids()

            # Получение листа ID визитов из ответа WODO
            new_visit_ids = create_list_id(data)

            # Получение кортежа повторяющихся ID визитов
            duplicates_visits = get_duplicates(visit_ids, new_visit_ids)

            # Преобразования словаря в кортеж для внесения в SQL-таблицу
            data_list = create_list(data, duplicates_visits)

            # Загрузка данных в базу данных SQL Server
            add_data_MSSQL(data_list)

            last_update_date = last_update_date + timedelta(days=1)
    except BaseException as e:
        print(str(e))
        return None


# Запускает функцию, если запускаем именно этот скрипт
if __name__ == "__main__":
    visits()
