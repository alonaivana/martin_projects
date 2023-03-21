import calendar
from datetime import date


# Получаем лист с датами начала и окончания предыдущего месяца
def get_date_range():
    today = date.today()
    today_year = today.year
    today_month = today.month

    if today_month == 1:
        download_month = 12
        download_year = today_year-1
    else:
        download_month = today_month-1
        download_year = today_year

    month_info = calendar.monthrange(download_year, download_month)
    last_day = month_info[1]
    begin_date = date(download_year, download_month, 1)
    end_date = date(download_year, download_month, last_day)

    date_range = [begin_date, end_date]

    return date_range


# Определяем название месяца
def month_name(month_numb):
    a = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль',
         'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
    month_name = a[month_numb-1]
    return month_name
