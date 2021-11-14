import schedule
import time
from datetime import datetime
import os


def job():
    now = str(datetime.now())[:16]
    with open('client.txt', mode='r') as f:
        text = f.read().split('\n')
        try:
            for i in text:
                data = i.split(';')
                client_date = data[0]
                client_id = data[1]
        except IndexError:
            pass
    if now == client_date:
        print('понеслась')
        os.system(f'python cancel_ph.py')
    else:
        print(client_date)
        print(now)

schedule.every().minute.do(job)
#schedule.every().day.at("12:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
    #print('working...')