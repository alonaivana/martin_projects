from sql_connection import get_connection_MSSQL
from datetime import date


# Преобразования словаря в кортеж для внесения в SQL-таблицу
# (с ограничением на уникальный ID визита)
def create_list(data, duplicates):
    data_list = []
    for visit_data in data:
        # Проверка на наличие ID среди дубликатов
        check = int(visit_data.get('visit_id'))
        if check not in duplicates:
            data_list.append((
                visit_data.get('contragent_name'),
                visit_data.get('visit_date'),
                visit_data.get('visit_id'),
                visit_data.get('code_tt'),
                visit_data.get('address_tt'),
                visit_data.get('branch_tt'),
                visit_data.get('city_tt'),
                visit_data.get('network_tt'),
                visit_data.get('latitude_tt'),
                visit_data.get('longitude_tt'),
                visit_data.get('visit_begin_date'),
                visit_data.get('visit_end_date'),
                visit_data.get('visit_plan_lead_time'),
                visit_data.get('visit_plan_travel_time_minutes'),
                visit_data.get('visit_plan_travel_time_minutes'),
                visit_data.get('visit_remote_finished'),
                visit_data.get('visit_end_distance'),
                visit_data.get('visit_has_fake_gps'),
                visit_data.get('visit_has_fake_photos'),
                visit_data.get('visit_last_time'),
                visit_data.get('visit_status'),
                visit_data.get('visit_unscheduled'),
                visit_data.get('visit_type'),
                visit_data.get('device_model'),
                visit_data.get('id_merch'),
                visit_data.get('visit_photos_url'),
                visit_data.get('visit_result_url'),
                visit_data.get('visit_work_time')
                ))
    return data_list


# Загрузка данных в базу данных SQL Server
def add_data_MSSQL(data_list):
    try:
        cnxn = get_connection_MSSQL()
        cursor = cnxn.cursor()
        request = """INSERT INTO [dbo].[visits]
           ([Контрагент],
           [Дата визита],
           [№ визита],
           [Код точки],
           [Адрес],
           [Филиал/Регион],
           [Город],
           [Сеть],
           [Широта],
           [Долгота],
           [Дата и время начала визита],
           [Дата и время окончания визита],
           [Время в точке/план],
           [Время на перемещение],
           [Время на перемещение / План],
           [Визит завершен вне ТТ],
           [Расстояние до ТТ в конце визита],
           [Использован Fake GPS],
           [Подменены фотографии],
           [Дата последнего изменения],
           [Статус визита],
           [Внеплановый],
           [Тип визита],
           [Устройство],
           [ID исполнителя],
           [Фотографии визита],
           [Результаты визита],
           [Время проведенное в точке])
           VALUES
           (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.executemany(request, data_list)
        cnxn.commit()
        cnxn.close()
    except BaseException:
        return None


# Узнаём дату последнего обновления базы данных
def get_last_update_date():
    try:
        request = ("""SELECT max([Дата визита])
        FROM [visits]""")
        cnxn = get_connection_MSSQL()
        cursor = cnxn.cursor()
        cursor.execute(request)
        response = cursor.fetchone()
        if not response[0]:
            today = date.today()
            today_year = today.year
            last_update_date = date(today_year, 1, 1)
        else:
            last_update_date = response[0].date()
        cnxn.close()
        return last_update_date
    except BaseException:
        return None


# Преобразования словаря в кортеж для внесения в SQL-таблицу
# (с ограничением на уникальный ID мерчандайзера)
def create_list_people(data, duplicates):
    data_list = []
    for people_data in data:
        # Проверка на наличие ID среди дубликатов
        check = int(people_data.get('id_merch'))
        if check not in duplicates:
            data_list.append((
                people_data.get('id_merch'),
                ))
    return data_list


# Загрузка данных в базу данных SQL Server
def add_data_MSSQL_people(data_list):
    try:
        cnxn = get_connection_MSSQL()
        cursor = cnxn.cursor()
        request = """INSERT INTO [dbo].[people]
           ([ID исполнителя])
           VALUES
           (%s)"""
        cursor.executemany(request, data_list)
        cnxn.commit()
        cnxn.close()
    except BaseException:
        return None
