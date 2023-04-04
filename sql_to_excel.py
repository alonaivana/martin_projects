import pandas as pd
import os
from datetime import date
from get_date_range import get_date_range_first, get_date_range_second
from get_date_range import month_name, month_name_rus
from sql_connection import get_connection_MSSQL
from settings import FIRST_DAY_OF_MONTH_TO_EMAIL_REPORT
from settings import SECOND_DAY_OF_MONTH_TO_EMAIL_REPORT


# Формируем запрос для базы данных SQL
def get_request(begin_date, end_date):
    request = (f"""select T1.*, isnull(time_on_tt/nullif(time_in_tt_plan , 0)
        ,(time_on_tt/(8*60)))*8 as fact_hours from
    (SELECT  visits.[Дата визита],visits.[ID исполнителя],
    people.Исполнитель, people.[Телефон исполнителя],
    people.Руководитель, visits.[Филиал/Регион],
    SUM(visits.[Время в точке/план]) as time_in_tt_plan,
    SUM(isnull(visits.[Время проведенное в точке],0))
    AS time_on_tt
    FROM visits LEFT OUTER JOIN people
    ON visits.[ID исполнителя] = people.[ID исполнителя]
    where visits.[Дата визита] between '{begin_date}T00:00:00'
    and '{end_date}T23:59:59'
    GROUP BY visits.[ID исполнителя],people.Руководитель
    ,people.[Телефон исполнителя]
    ,people.Исполнитель,visits.[Филиал/Регион], visits.[Дата визита]) as T1
    order by [Исполнитель],[Дата визита]""")

    return request


# Получаем данные для Excel-таблицы из базы данных SQL
def GetDataFromMSSQL(begin_date, end_date):
    try:
        cnxn = get_connection_MSSQL()
        if not cnxn:
            exit()

        cursor = cnxn.cursor()

        request = get_request(begin_date, end_date)
        cursor.execute(request)
        rows = pd.DataFrame(cursor.fetchall(),
                            columns=['Дата визита',
                                     'ID исполнителя',
                                     'Исполнитель',
                                     'Телефон исполнителя',
                                     'Руководитель',
                                     'Филиал/Регион',
                                     'Время в точке (план), мин.',
                                     'Время в точке (факт), мин.',
                                     'Фактическое время работы, час/день'])
        cnxn.close()
        return rows
    except BaseException:
        return None


# Создаём Excel-файл за половину месяца
def sql_to_excel():
    try:
        today = date.today()
        day = today.day

        # Запускаем создание файла в 3-ий день месяца
        if day == FIRST_DAY_OF_MONTH_TO_EMAIL_REPORT:

            # Получаем лист с 16 и последним числом прошлого месяца
            date_range = get_date_range_first()
            begin_date = date_range[0]
            end_date = date_range[1]
            month_numb = begin_date.month
            year = begin_date.year  # Год для имени файла
            m_name = month_name(month_numb)  # Название месяца для имени файла
            m_name_rus = month_name_rus(month_numb)  # Название месяца (рус.)

            # Получаем данные для Excel-таблицы из базы данных SQL
            data = GetDataFromMSSQL(begin_date, end_date)

            # Меняем формат даты визита для Excel
            data['Дата визита'] = data['Дата визита'].dt.strftime('%d.%m.%Y')

            # Создаём Excel-файл
            filename = f"merchandisers_{m_name}2_{year}.xlsx"
            writer = pd.ExcelWriter(filename)
            data.to_excel(writer,
                          sheet_name=f"{m_name_rus}2_{year}",
                          index=False)

            # Корректируем ширину колонки в Excel
            for column in data:
                column_width = max(data[column].astype(str).map(len).max(),
                                   len(column))
                col_idx = data.columns.get_loc(column)
                writer.sheets[f"{m_name_rus}2_{year}"].set_column(col_idx,
                                                                  col_idx,
                                                                  column_width)
            writer.save()

        # Запускаем создание файла в 18-ый день месяца
        if day == SECOND_DAY_OF_MONTH_TO_EMAIL_REPORT:
            # Получаем лист с датой начала и 15 числом текущего месяца
            date_range = get_date_range_second()
            begin_date = date_range[0]
            end_date = date_range[1]
            month_numb = begin_date.month
            year = begin_date.year  # Год для имени файла
            m_name = month_name(month_numb)  # Название месяца для имени файла
            m_name_rus = month_name_rus(month_numb)  # Название месяца (рус.)

            # Получаем данные для Excel-таблицы из базы данных SQL
            data = GetDataFromMSSQL(begin_date, end_date)

            # Меняем формат даты визита для Excel
            data['Дата визита'] = data['Дата визита'].dt.strftime('%d.%m.%Y')

            # Создаём Excel-файл
            filename = f"merchandisers_{m_name}1_{year}.xlsx"
            writer = pd.ExcelWriter(filename)
            data.to_excel(writer,
                          sheet_name=f"{m_name_rus}1_{year}",
                          index=False)

            # Корректируем ширину колонки в Excel
            for column in data:
                column_width = max(data[column].astype(str).map(len).max(),
                                   len(column))
                col_idx = data.columns.get_loc(column)
                writer.sheets[f"{m_name_rus}1_{year}"].set_column(col_idx,
                                                                  col_idx,
                                                                  column_width)
            writer.save()
        return filename
    except BaseException:
        return None


# Удаляем файл
def remove_file(filename):
    os.remove(filename)


# Запускает функцию, если запускаем именно этот скрипт
if __name__ == "__main__":
    filename = sql_to_excel()
    remove_file(filename)
