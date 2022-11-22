
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
wait = WebDriverWait(driver, 2)


class OkBot():
    def __init__(self, login, password) -> None:
        self.__base_url = 'https://ok.ru/'
        self.__login = login
        self.__password = password
        self.__is_auth = False
        self.__auth()
    
    def __auth(self):
        """
        Метод авторизации
        """
        if self.__is_auth:
            if bool(input('Выйти из аккаунта? 1 - Да / 0 - Нет')):
                wait.until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '.toolbar_ucard'))).click()
                wait.until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, 'a.lp'))).click()
                driver.get(self.__base_url)
                return
            self.__is_auth = False

        driver.get(self.__base_url)
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="st.email"]'))).send_keys(self.__login)
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[name="st.password"]'))).send_keys(self.__password)
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input.button-pro'))).click()
        
        print(f'Вы авторизованы в аккаунт {self.__login}:{self.__password}')
        self.__is_auth = True
        
        
                
    def __scroll(self):
        """
        Метод для прокрутки страницы
        """
        i = 0
        while i < 5:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)
            driver.execute_script("window.scrollTo(0, 0);")
            sleep(1)
            i += 1


    def __create_post(self):
        """
        Метод создания поста
        """
        driver.get(self.__base_url + 'post')
        comment = str(input('Введите создаваемое сообщение: '))
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.posting_itx'))).send_keys(comment)
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.posting_submit'))).click()
        driver.get(self.__base_url)


    def __create_comment_in_user_profile(self):
        """
        Метод создания комментария подсты пользователя
        """
        if int(input('Загрузить ID из текстового документа? 1 - да / 0 - нет')) == 1:
            with open('ids.txt', encoding='utf-8') as file:
                ids = [line.rstrip() for line in file]
        else:
            ids = int(input('Введите ID: '))

        ids = [ids]

        for _id in ids:
            driver.get(self.__base_url + f'profile/{_id}')
            self.__scroll()

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


    def __like_users(self):
        """
        Метод лайка пользователей
        """
        if int(input('Загрузить ID из текстового документа? 1 - да / 0 - нет: ')) == 1:
            try:
                with open('ids.txt', encoding='utf-8') as file:
                    ids = [line.rstrip() for line in file]
            except Exception as _:
                print('Документ не найден.')
        else:
            ids = int(input('Введите ID: '))
            ids = [ids]


        for id in ids:
            driver.get(self.__base_url + f'profile/{id}')
            self.__scroll()

            like_button = driver.find_elements(
                By.CSS_SELECTOR,
                'span[class="widget_cnt controls-list_lk js-klass js-klass-action h-mod"]')
            for like in like_button:
                like.click()


    def __menu(self):
        """
        Метод отображения меню
        """
        print('''
            1 - Создать публикацию\n
            2 - Поставить лайки пользователю\n
            3 - Написать комментарии под посты\n
            -1 - Чтобы выйти\n
            ''')


    def start(self):
        """
        Метод выбора пункта меню
        """
        self.__menu()
        match int(input('>>> ')):
            case 1:
                self.__create_post()
                return True
            case 2:
                self.__like_users()
                return True
            case 3:
                self.__create_comment_in_user_profile()
                return True
            case -1:
                return False
            case _:
                print('Такого пункта нет...')
                return True
