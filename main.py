from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import logging
logging.basicConfig(filename='sample.log', level=logging.INFO)
import time
import sys
import os
import threading
from random import randint
count = 2            #int(input('Введите количество потоков: '))
semaphore = threading.Semaphore(value = count)
path_to_driver = "geckodriver.exe"


def start_p(tel, pas, ch_tel, ip, port):
    with semaphore:
        try:
            options = webdriver.FirefoxOptions()
            try:
                options.set_preference('network.proxy.type', 1)
                options.set_preference('network.proxy.http', ip)
                options.set_preference('network.proxy.http_port', port)
                options.set_preference('network.proxy.https', ip)
                options.set_preference('network.proxy.https_port', port)
                options.set_preference('network.proxy.ssl', ip)
                options.set_preference('network.proxy.ssl_port', port)
            except Exception:
                pass
            options.set_preference("general.useragent.override",
                                   "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0")
            options.set_preference("dom.webdriver.enabled", False)
            options.headless = False
            driver = webdriver.Firefox(
                executable_path=path_to_driver,
                service_log_path=os.path.devnull,
                options=options
            )
            try:
                driver.get('https://msk.tele2.ru/business/login-new-lk?pageParams=askForRegion%3Dtrue')
                driver.implicitly_wait(10)
                time.sleep(randint(1, 3))
                driver.find_element_by_xpath('//a[@class="gtm-old-navigation-login"]').click()
                driver.implicitly_wait(10)
                time.sleep(randint(1, 3))
                login = driver.find_element_by_xpath('//div[@class="info-modal violet-style"]')
                driver.implicitly_wait(10)
                time.sleep(randint(1,3))
                tel_login = login.find_element_by_xpath('//input[@id="keycloakAuth.phone"]').click()
                driver.implicitly_wait(10)
                time.sleep(randint(1, 3))
                inp = driver.find_element_by_xpath('//input[@class="text-field"]')
                driver.implicitly_wait(10)
                time.sleep(randint(1, 3))
                inp.send_keys(tel + Keys.ENTER)
                driver.implicitly_wait(10)
                time.sleep(randint(1, 3))
                driver.find_element_by_xpath('//button[@class="keycloak-login-form__button underscored-button"]').click()
                pasw_inp = driver.find_element_by_xpath('//input[@id="keycloakAuth.password"]')
                pasw_inp.send_keys(pas)
                driver.find_element_by_xpath('//button[@class="keycloak-login-form__button btn btn-black"]').click()
                driver.implicitly_wait(10)
                time.sleep(randint(1, 3))
                try:
                    if driver.find_element_by_xpath('//p[@class="static-error-text"]'):
                        e = driver.find_element_by_xpath('//p[@class="static-error-text"]').text
                        log = log + f'Ошибка для номера {tel}: {e}' + '\n'
                        print(f'Ошибка для номера {tel}: ', e)
                        driver.close()
                        start_p(tel, pas, ch_tel, ip, port)
                    logging.info(f'Авторизация {tel} прошла успешно'  + '\n')
                except Exception:
                    pass
                print(f'Авторизация {tel} прошла успешно')
            except Exception:
                print(f'Авторизация {tel} не удалась, возможно проблема с соединением в том числе с прокси')
                logging.info(f'Авторизация {tel} не удалась, возможно проблема с соединением в том числе с прокси'  + '\n')

            try:
                balanse = driver.find_element_by_xpath('//span[@class="number"]').text
                logging.info(f'Баланс {tel} состовляет {balanse}'  + '\n')
                print(f'Баланс {tel} состовляет {balanse}')
                menu = driver.find_elements_by_xpath('//li[@class="header-navbar-hot-line-navigation-item header-navbar-hot-line-navigation-item_none"]')
                menu[-2].click()
                driver.implicitly_wait(10)
                time.sleep(randint(1, 3))
                driver.find_element_by_xpath('//div[@data-cartridge-type="CallForwardingCard"]').click()
                driver.implicitly_wait(10)
                print(f'В меню переадресации {tel} зашёл успешно')
                logging.info(f'В меню переадресации {tel} зашёл успешно' + '\n')
            except Exception:
                logging.info(f'В меню переадресации {tel} не смог зайти' + '\n')
                print(f'В меню переадресации {tel} не смог зайти')

            #если уже есть переадресация
            try:
                try:
                    rev_tel = driver.find_element_by_xpath('//div[@class="text-field-holder phone-field text-active call-forwarding-board__phone-number "]')
                except Exception:
                    rev_tel = driver.find_element_by_xpath(
                        '//div[@class="text-field-holder phone-field call-forwarding-board__phone-number "]')
                change_tel = rev_tel.find_element_by_tag_name('input')
                driver.implicitly_wait(10)

                #перетаскиевание бегунка "всегда переадресовывать вызовы"
                s = driver.find_element_by_xpath('//input[@id="checkBoxField_нет ответа 10 секунд"]')
                if s.get_attribute('disabled'):
                    logging.info(f'Для {tel} включена функция "Всегда переадресовывать вызовы"' + '\n')
                    print(f'Для {tel} включена функция "Всегда переадресовывать вызовы"')
                else:
                    # перетащить бегунок "всегда переадресовывать вызовы"
                    driver.find_element_by_xpath('//label[@class="switch"]').click()
                    driver.implicitly_wait(10)
                    logging.info(f'Для {tel} включена функция "Всегда переадресовывать вызовы"' + '\n')
                    print(f'Для {tel} включена функция "Всегда переадресовывать вызовы"')

                for i in range(11):
                    change_tel.send_keys(Keys.BACKSPACE)
                change_tel.send_keys(ch_tel)
                driver.find_element_by_xpath('//button[@class="btn btn-black call-forwarding-board-buttons__button"]').click()
                if driver.find_elements_by_xpath('//p[@class="error-message call-forwarding-board__error-text"]'): #если ошибка - то повторяем
                    driver.refresh()
                    try:
                        rev_tel = driver.find_element_by_xpath(
                            '//div[@class="text-field-holder phone-field text-active call-forwarding-board__phone-number "]')
                    except Exception:
                        rev_tel = driver.find_element_by_xpath(
                            '//div[@class="text-field-holder phone-field call-forwarding-board__phone-number "]')
                    change_tel = rev_tel.find_element_by_tag_name('input')
                    for i in range(11):
                        change_tel.send_keys(Keys.BACKSPACE)
                    change_tel.send_keys(ch_tel)
                    driver.find_element_by_xpath(
                        '//button[@class="btn btn-black call-forwarding-board-buttons__button"]').click()
                logging.info(f'Для {tel} процедура переадресации на {ch_tel} прошла успешно' + '\n')
                print(f'Для {tel} процедура переадресации на {ch_tel} прошла успешно')

            except Exception:
                logging.info(f'Для {tel} процедура переадресации не прошла успешно' + '\n')
                print(f'Для {tel} процедура переадресации не прошла успешно')
            time.sleep(randint(4,7))
        except Exception:
            pass
        finally:
            driver.close()
#кнопка - отключить переадресацию
#                    driver.find_element_by_xpath('//button[@class="btn call-forwarding-board-buttons__button"]').click()

if __name__ == '__main__':
    print('началось')
    ch_tel = sys.argv[1]
    threads = list()
    # list_files = os.listdir()
    # for i in list_files:
    #     if i[-4:] == '.txt':
    #         file = i
    with open('phones.txt', mode='r') as f:
        text = f.read().split('\n')
        try:
            for i in text:
                data = i.split(';')
                tel = ''.join(c for c in data[0] if c.isdigit())
                if tel[0] == '7':
                    tel = tel[1:]
                pas = data[1]
                try:
                    proxy = data[2].split(':')
                    ip = proxy[0]
                    port = int(proxy[1])
                    print(ip, port)
                except Exception:
                    ip = ''
                    port = ''
                thread = threading.Thread(target=start_p, args=(tel, pas, ch_tel, ip, port,))
                threads.append(thread)
                print(tel, pas, ch_tel, ip, port)
        except IndexError:
            pass
    for i in threads:
        i.start()