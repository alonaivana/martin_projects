from datetime import date
from sql_to_excel import sql_to_excel, remove_file
from email_excel import email_excel
from settings import FIRST_DAY_OF_MONTH_TO_EMAIL_REPORT as FIRST
from settings import SECOND_DAY_OF_MONTH_TO_EMAIL_REPORT as SECOND
from settings import RECEIVER_EMAIL, RECEIVER_EMAIL_CONTROL


# Создаёмб отправляемб удаляем Excel-файл
def run_excel():

    today = date.today()
    day = today.day

    # Запускаем создание файла в 3-ий день месяца
    if day == FIRST or day == SECOND:
        # Создаём Excel-файл за половину месяца
        filename = sql_to_excel()

        # Отправляем Excel-файл в отдел мерчендайзинга
        email_excel(RECEIVER_EMAIL)

        # Отправляем Excel-файл в отдел IT
        email_excel(RECEIVER_EMAIL_CONTROL)

        # Удаляем Excel-файл
        remove_file(filename)


# Запускает функцию, если запускаем именно этот скрипт
if __name__ == "__main__":
    run_excel()
