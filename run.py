import schedule
import time
from visits import visits
from sql_to_excel import sql_to_excel
from settings import TIME_TO_LOAD

scheduler1 = schedule.Scheduler()
scheduler2 = schedule.Scheduler()

# Запуск загрузки данных в 3 часа ночи ежедневно
scheduler1.every().day.at(TIME_TO_LOAD).do(visits)
scheduler2.every().day.at(TIME_TO_LOAD).do(sql_to_excel)

# Ежесекундная проверка времени для запуска функции
while True:
    scheduler1.run_pending()
    scheduler2.run_pending()
    time.sleep(1)
