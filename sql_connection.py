import pymssql
from settings import SERVER, DB_USER, DB_PASSWORD, DATABASE

# Получение доступа к SQL Server


def get_connection_MSSQL():
    try:
        cnxn = pymssql.connect(server=SERVER,
                               user=DB_USER,
                               password=DB_PASSWORD,
                               database=DATABASE
                               )
        return cnxn
    except BaseException:
        return None
