from sql_connection import get_connection_MSSQL


# Формирование запроса на получение существующих номеров визита из базы данных
def get_request():
    request = (
        """SELECT [№ визита]
        FROM [merchtest].[dbo].[visits]""")
    return request


# Получение листа ID визитов из базы данных
def get_visit_ids():
    try:
        cnxn = get_connection_MSSQL()
        cursor = cnxn.cursor()

        request = get_request()
        cursor.execute(request)
        rows = cursor.fetchall()
        rows_list = [int(item) for t in rows for item in t]
        cnxn.close()
        return rows_list
    except BaseException:
        return None


# Получение листа новых ID визитов (из тех, которые хотим добавить)
def create_list_id(data):
    data_list = []
    for visit_data in data:
        data_list.append((
            int(visit_data.get('visit_id'))
            ))
    return data_list


# Получение кортежа повторяющихся ID визитов
def get_duplicates(list1, list2):
    list1.extend(list2)
    ids_unique = set()
    duplicates = []
    for x in list1:
        if x in ids_unique:
            duplicates.append(x)
        else:
            ids_unique.add(x)
    return duplicates
