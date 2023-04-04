import smtplib
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from get_date_range import get_date_range_first, get_date_range_second
from get_date_range import month_name, month_name_rus
from settings import SMPT_SERVER, PORT, SENDER_EMAIL, EMAIL_PASSWORD
from settings import FIRST_DAY_OF_MONTH_TO_EMAIL_REPORT
from settings import SECOND_DAY_OF_MONTH_TO_EMAIL_REPORT


# Отправляем Excel-файл по электронной почте
def email_excel(recipient_email):
    # Ваши учетные данные для отправки
    sender_email = SENDER_EMAIL
    sender_password = EMAIL_PASSWORD

    # Получаем сегодняшнюю дату
    today = date.today()
    day = today.day

    # Получаем дату для названия файла, темы письма (3 число)
    if day == FIRST_DAY_OF_MONTH_TO_EMAIL_REPORT:

        # Получаем лист с 16 и последним числом прошлого месяца
        date_range = get_date_range_first()
        begin_date = date_range[0]
        month_numb = begin_date.month
        year = begin_date.year  # Год для имени письма
        m_name = month_name(month_numb)  # Название месяца для имени письма
        m_name_rus = month_name_rus(month_numb)  # Название месяца (рус.)
        filename = f"merchandisers_{m_name}2_{year}.xlsx"  # Имя файла

    # Получаем дату для названия файла, темы письма (18 число)
    if day == SECOND_DAY_OF_MONTH_TO_EMAIL_REPORT:
        # Получаем лист с датой начала и 15 числом текущего месяца
        date_range = get_date_range_second()
        begin_date = date_range[0]
        month_numb = begin_date.month
        year = begin_date.year  # Год для имени письма
        m_name = month_name(month_numb)  # Название месяца для имени письма
        m_name_rus = month_name_rus(month_numb)  # Название месяца (рус.)
        filename = f"merchandisers_{m_name}1_{year}.xlsx"  # Имя файла

    # Получатели, тема, текст письма
    if day == FIRST_DAY_OF_MONTH_TO_EMAIL_REPORT:
        subject = f"""Отчёт по мерчендайзерам,
        {m_name_rus} (вторая половина) {year}"""
        body = (f"Отчёт по мерчендайзерам за {m_name_rus}, "
                "вторая половина месяца (с 16 числа).")
    if day == SECOND_DAY_OF_MONTH_TO_EMAIL_REPORT:
        subject = f"""Отчёт по мерчендайзерам,
        {m_name_rus} (первая половина) {year}"""
        body = (f"Отчёт по мерчендайзерам за {m_name_rus}, "
                "первая половина месяца (1-15 число).")

    # Путь к файлу вложения
    attachment_file = filename

    # Создание сообщения
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Добавление текста письма
    msg.attach(MIMEText(body, "plain"))

    # Добавление вложения
    with open(attachment_file, "rb") as attachment:
        # Добавление файла в виде base64
        payload = MIMEBase("application", "octet-stream")
        payload.set_payload(attachment.read())
        encoders.encode_base64(payload)

        # Добавление заголовков для вложения
        payload.add_header("Content-Disposition",
                           f"attachment; filename={filename}")
        msg.attach(payload)

    # Отправка письма
    try:
        with smtplib.SMTP_SSL(SMPT_SERVER, PORT) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")


# Запускает функцию, если запускаем именно этот скрипт
if __name__ == "__main__":
    email_excel()
