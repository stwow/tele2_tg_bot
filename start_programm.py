# import asyncio
import os
import threading


def telebot():
    os.system('python tele2_bot.py')


def timer():
    os.system('python test_time.py')


th = threading.Thread(target=telebot)
ti = threading.Thread(target=timer)

th.start()
ti.start()

#
#
# async def telebot():
#     os.system('python tele2_bot.py')
#
#
# async def timer():
#     os.system('python test_time.py')
#
#
#
# loop = asyncio.get_event_loop()
#
# tasks = [
#     loop.create_task(timer()),
#     loop.create_task(telebot()),
#
# ]
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()

