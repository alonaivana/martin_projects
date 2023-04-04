import schedule
import time
from visits import visits
from run_excel import run_excel
from settings import TIME_TO_LOAD_SQL, TIME_TO_CREATE_EXCEL

scheduler1 = schedule.Scheduler()
scheduler2 = schedule.Scheduler()

# Запуск загрузки данных в базу SQL в 3 часа ночи ежедневно
scheduler1.every().day.at(TIME_TO_LOAD_SQL).do(visits)

# Запуск создания и отправки Excel-файла каждое 3 и 18 число месяца
scheduler2.every().day.at(TIME_TO_CREATE_EXCEL).do(run_excel)

# Ежесекундная проверка времени для запуска функции
while True:
    scheduler1.run_pending()
    scheduler2.run_pending()
    time.sleep(1)
