from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
wait = WebDriverWait(driver, 2)

BASE_URL = 'https://ok.ru/'
LOGIN = '79000778443'  # str(input('Введите логин: '))
PASSWORD = 'f4k3p4ssw0rd'  # str(input('Введите пароль: '))
IS_AUTH = False


def auth():
    """
    Функция авторизации
    """
    global IS_AUTH
    if IS_AUTH:
        if bool(input('Выйти из аккаунта? 1 - Да / 0 - Нет')):
            wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '.toolbar_ucard'))).click()
            wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'a.lp'))).click()
            driver.get(BASE_URL)
            return
        IS_AUTH = False

    driver.get(BASE_URL)
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'input[name="st.email"]'))).send_keys(LOGIN)
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'input[name="st.password"]'))).send_keys(PASSWORD)
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'input.button-pro'))).click()
    IS_AUTH = True


def scroll():
    """
    Функция для прокрутки страницы
    """
    i = 0
    while i < 5:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)
        driver.execute_script("window.scrollTo(0, 0);")
        sleep(1)
        i += 1


def create_post():
    """
    Функция создания поста
    """
    driver.get(BASE_URL + 'post')
    comment = str(input('Введите создаваемое сообщение: '))
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '.posting_itx'))).send_keys(comment)
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '.posting_submit'))).click()
    driver.get(BASE_URL)


def create_comment_in_user_profile():
    """
    Функция создания комментария подсты пользователя
    """
    if int(input('Загрузить ID из текстового документа? 1 - да / 0 - нет')) == 1:
        with open('ids.txt', encoding='utf-8') as file:
            ids = [line.rstrip() for line in file]
    else:
        ids = int(input('Введите ID: '))

    ids = [ids]

    for _id in ids:
        driver.get(BASE_URL + f'profile/{_id}')
        scroll()

        elements = driver.find_elements(
            By.CSS_SELECTOR,
            '.feed-list > div > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > ul:nth-child(2) > li:nth-child(1) > div:nth-child(1) > a:nth-child(1)'
            )
        urls = [element.get_attribute('href') for element in elements]
        comment = str(input('Комментарий: '))

        for url in urls:
            driver.get(url)
            try:
                wait.until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, '.gwt-inputButton'))).click()
            except Exception as _:
                pass
            wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '#ok-e-d'))).send_keys(comment)
            wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '#ok-e-d_button'))).click()


def like_users():
    """
    Функция лайка пользователей
    """
    if int(input('Загрузить ID из текстового документа? 1 - да / 0 - нет')) == 1:
        with open('ids.txt', encoding='utf-8') as file:
            ids = [line.rstrip() for line in file]
    else:
        ids = int(input('Введите ID: '))

    ids = [ids]

    for id in ids:
        driver.get(BASE_URL + f'profile/{id}')
        scroll()

        like_button = driver.find_elements(
            By.CSS_SELECTOR,
            'span[class="widget_cnt controls-list_lk js-klass js-klass-action h-mod"]')
        for like in like_button:
            like.click()


def menu():
    """
    Функция отображения меню
    """
    print('''
          1 - Создать публикацию\n
          2 - Поставить лайки пользователю\n
          3 - Написать комментарии под посты\n
          4 - Авториоваться в аккаунт\n
          ''')


def start():
    """
    Функция выбора пункта меню
    """
    menu()
    match int(input('>>> ')):
        case 1:
            create_post()
        case 2:
            like_users()
        case 3:
            create_comment_in_user_profile()
        case 4:
            auth()
        case _:
            pass


while True:
    start()
