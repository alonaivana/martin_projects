import pandas as pd
from datetime import date
from get_date_range import get_date_range, month_name
from sql_connection import get_connection_MSSQL


# Формируем запрос для базы данных SQL
def get_request(begin_date, end_date):
    request = (f"""select T1.*, isnull(time_on_tt/nullif(time_in_tt_plan , 0),
    (time_on_tt/(8*60)))*8 as fact_hours from
    (SELECT  visits.[Дата визита],visits.[ID исполнителя], people.Исполнитель,
    visits.[Филиал/Регион],SUM(isnull(visits.[Время проведенное в точке],0))
    AS time_on_tt, SUM(visits.[Время в точке/план]) as time_in_tt_plan
    FROM visits LEFT OUTER JOIN people
    ON visits.[ID исполнителя] = people.[ID исполнителя]
    where visits.[Дата визита] between '{begin_date}T00:00:00.000' and
    '{end_date}T23:59:59.999'
    GROUP BY visits.[ID исполнителя],people.Руководитель,
    people.Исполнитель,visits.[Филиал/Регион], visits.[Дата визита]) as T1
    where time_in_tt_plan <> 0
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
                                     'Филиал/Регион',
                                     'Фактическое время работы, мин.',
                                     'Планируемое время работы, мин.',
                                     'Фактическое время работы, час/день'])
        cnxn.close()
        return rows
    except BaseException:
        return None


def sql_to_excel():
    try:
        today = date.today()
        day = today.day

        # Запускаем создание файла только в 4-ый день месяца
        if day == 4:

            # Получаем лист с датами начала и окончания предыдущего месяца
            date_range = get_date_range()
            begin_date = date_range[0]
            end_date = date_range[1]
            month_numb = begin_date.month
            year = begin_date.year  # Год для имени файла
            m_name = month_name(month_numb)  # Название месяца для имени файла

            # Получаем данные для Excel-таблицы из базы данных SQL
            data = GetDataFromMSSQL(begin_date, end_date)

            # Меняем формат даты визита для Excel
            data['Дата визита'] = data['Дата визита'].dt.strftime('%d.%m.%Y')

            # Создаём Excel-файл
            writer = pd.ExcelWriter(f"мерчандайзеры_{m_name}_{year}.xlsx")
            data.to_excel(writer,
                          sheet_name=f"{m_name}_{year}",
                          index=False)

            # Корректируем ширину колонки в Excel
            for column in data:
                column_width = max(data[column].astype(str).map(len).max(),
                                   len(column))
                col_idx = data.columns.get_loc(column)
                writer.sheets[f"{m_name}_{year}"].set_column(col_idx,
                                                             col_idx,
                                                             column_width)
            writer.save()
    except BaseException:
        return None


if __name__ == "__main__":
    sql_to_excel()
