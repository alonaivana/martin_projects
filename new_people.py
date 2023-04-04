from sql_connection import get_connection_MSSQL


# Запрос на получение существующих ID мерчандайзеров из базы данных
def get_request_people():
    request = (
        """SELECT [ID исполнителя]
        FROM [people]""")
    return request


# Получение листа ID мерчандайзеров из базы данных
def get_people_ids():
    try:
        cnxn = get_connection_MSSQL()
        cursor = cnxn.cursor()

        request = get_request_people()
        cursor.execute(request)
        rows = cursor.fetchall()
        rows_list = []
        for t in rows:
            if t[0]:
                rows_list.append(t[0])

        cnxn.close()
        return rows_list
    except BaseException as e:
        print(str(e))


# Получение листа ID мерчандайзеров из ответа WODO
def create_list_people_id(data):
    data_list = []
    for person in data:
        data_list.append((
            int(person.get('id_merch'))
        ))
    return data_list


# Получение кортежа повторяющихся ID мерчандайзеров
def get_dup_people(list1, list2):
    list1.extend(list2)
    ids_unique = set()
    duplicates = []
    for x in list1:
        if x in ids_unique:
            duplicates.append(x)
        else:
            ids_unique.add(x)
    return duplicates
