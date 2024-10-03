import datetime
import time
import re
import os
import allure

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from typing import Dict, Type, Optional

# Путь к драйверу
WINDOWS_DRIVER_PATH = os.path.join('resource', 'windows', 'chromedriver.exe')


class Base:
    """
    Базовый класс, содержащий методы для взаимодействия с веб-драйвером.
    """
    driver: WebDriver
    
    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует экземпляр класса с драйвером.

        Parameters
        ----------
        driver : WebDriver
            Драйвер для управления браузером.
        """
        self.driver = driver
    
    """ Get driver """
    
    @classmethod
    def get_driver(cls: Type['Base']) -> 'Base':
        """
        Создает и возвращает экземпляр драйвера и класса.

        Returns
        -------
        Base
            Экземпляр класса Base с инициализированным веб-драйвером.
        """
        options = webdriver.ChromeOptions()
        
        # Настройки для Windows
        chrome_driver_path = WINDOWS_DRIVER_PATH
        options.add_argument('--window-size=1920x1080')
        
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(options=options, service=service)
        
        with allure.step("Start test"):
            print("Start test")
        
        return cls(driver)
    
    """ Test finish """
    
    def test_finish(self) -> None:
        """
        Завершает тест и закрывает браузер.
        """
        with allure.step("Test finish"):
            print("Test finish")
            self.driver.quit()
    
    """ Get element with choosing a method for obtaining an element """
    
    def get_element(self, element_info: Dict[str, str], wait_type: str = 'clickable') \
            -> Dict[str, Optional[WebElement]]:
        """
        Ожидает элемент в зависимости от выбранного типа ожидания и возвращает элемент.

        Parameters
        ----------
        element_info : dict
            Информация о локаторе элемента.
        wait_type : str, optional
            Тип ожидания: 'clickable', 'visible', 'located', 'find', или 'invisibility'. По умолчанию 'clickable'.

        Returns
        -------
        dict
            Словарь с информацией о найденном элементе или None, если элемент не найден.
        """
        try:
            if wait_type == 'clickable':
                element = WebDriverWait(self.driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, element_info['xpath'])))
            elif wait_type == 'visible':
                element = WebDriverWait(self.driver, 15).until(
                    EC.visibility_of_element_located((By.XPATH, element_info['xpath'])))
            elif wait_type == 'located':
                element = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, element_info['xpath'])))
            elif wait_type == 'find':
                element = self.driver.find_element(By.XPATH, element_info['xpath'])
            elif wait_type == 'invisibility':
                WebDriverWait(self.driver, 60).until(
                    EC.invisibility_of_element_located((By.XPATH, element_info['xpath'])))
                element = None
            else:
                raise ValueError(f"Unsupported wait type: {wait_type}")
            
            return {'name': element_info['name'], 'element': element}
        
        except TimeoutException:
            message = f"Element '{element_info['name']}' is not {wait_type}"
            with allure.step(message):
                print(message)
            if wait_type == 'visible':
                return {'name': element_info['name'], 'element': None}
            raise TimeoutException(message)
    
    """ Get timestamp with dot """
    
    @staticmethod
    def get_timestamp_dot() -> str:
        """
        Возвращает текущее время в формате UTC с точками в качестве разделителей.

        Returns
        -------
        str
            Текущее время в формате "ГГГГ.ММ.ДД.ЧЧ.ММ.СС".
        """
        return datetime.datetime.utcnow().strftime("%Y.%m.%d.%H.%M.%S")
    
    """ Assert word input reference """
    
    def flexible_assert_word(self, element_dict: Dict[str, str], reference_value: str,
                             wait_type: str = 'clickable') -> None:
        """
        Проверяет, что текст элемента или значение его атрибута 'value' соответствует заданному значению.

        Parameters
        ----------
        element_dict : dict
            Словарь с информацией о локаторе элемента.
        reference_value : str
            Ожидаемый текст или значение для проверки соответствия тексту элемента или его атрибуту 'value'.
        wait_type : str, optional
            Тип ожидания элемента ('clickable', 'visible', 'located', 'find'). По умолчанию 'clickable'.

        Raises
        ------
        AssertionError
            Если текст элемента или его атрибут 'value' не соответствует ожидаемому значению.
        """
        element = self.get_element(element_dict, wait_type=wait_type)['element']
        time.sleep(0.1)
        actual_text = element.text or element.get_attribute('value')
        with allure.step(f"Assert \"{actual_text}\" == \"{reference_value}\""):
            assert re.fullmatch(reference_value,
                                actual_text), f"Expected '{reference_value}', but found '{actual_text}'."
            print(f"Assert \"{actual_text}\" == \"{reference_value}\"")
    
    """ Get screenshot """
    
    def get_screenshot(self, test_name: str = None) -> None:
        """
        Сохраняет скриншот текущего состояния браузера в базовую папку.
        Если тест запускается с Allure, прикрепляет скриншот к отчету Allure.

        Parameters
        ----------
        test_name : str, optional
            Имя теста, используется для именования скриншота. Если не указано, используется только таймштамп.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        screenshot_dir = os.path.join(base_dir, '..', 'screens')
        
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        print(f"Saving screenshot to default directory: {screenshot_dir}")
        
        timestamp = self.get_timestamp_dot()
        name_screenshot = f'{test_name}_{timestamp}.png' if test_name else f'{timestamp}.png'
        screenshot_path = os.path.join(screenshot_dir, name_screenshot)
        
        self.driver.save_screenshot(screenshot_path)
        
        with allure.step(f"Screen taken: {name_screenshot}"):
            print(f"Screenshot saved successfully at: {screenshot_path}")
            allure.attach.file(screenshot_path, name="Screenshot", attachment_type=allure.attachment_type.PNG)
    
    """ Click button """
    
    def click_button(self, element_dict: Dict[str, str], wait_type: str = 'clickable') -> None:
        """
        Кликает по кнопке с заданным типом ожидания.

        Parameters
        ----------
        element_dict : dict
            Словарь с информацией о кнопке для клика.
        wait_type : str, optional
            Тип ожидания элемента перед кликом ('clickable', 'visible', 'located', 'find'). По умолчанию 'clickable'.
        """
        with allure.step(f"Click on {element_dict['name']}"):
            button_dict = self.get_element(element_dict, wait_type)
            button_dict['element'].click()
            print(f"Click on {button_dict['name']}")
    
    """ Input in field with optional click and enter """
    
    def input_in_field(self, element_dict: Dict[str, str], value: str, click_first: bool = False,
                       press_enter: bool = False, wait_type: str = 'clickable') -> None:
        """
        Универсальный метод для ввода текста в поле с опциональным кликом перед вводом и нажатием Enter после.

        Parameters
        ----------
        element_dict : dict
            Словарь с информацией о поле ввода.
        value : str
            Значение для ввода.
        click_first : bool, optional
            Если True, сначала кликает по полю перед вводом текста. По умолчанию False.
        press_enter : bool, optional
            Если True, нажимает Enter после ввода текста. По умолчанию False.
        wait_type : str, optional
            Тип ожидания элемента ('clickable', 'visible', 'located', 'find'). По умолчанию 'clickable'.
        """
        with allure.step(f"{'Click and ' if click_first else ''}Input in {element_dict['name']}: {value}"):
            field_dict = self.get_element(element_dict, wait_type)
            if click_first:
                field_dict['element'].click()
            field_dict['element'].send_keys(value)
            if press_enter:
                field_dict['element'].send_keys(Keys.ENTER)
            print(f"{'Click and ' if click_first else ''}Input in {element_dict['name']}: {value}")
    
    """ Select option in dropdown by text, value or index """
    
    def select_option(self, element_dict: Dict[str, str], option: str, by: str = 'text',
                      wait_type: str = 'clickable') -> None:
        """
        Выбирает опцию в выпадающем списке <select> с опциональным типом ожидания.

        Parameters
        ----------
        element_dict : dict
            Словарь с информацией о <select> элементе.
        option : str
            Опция для выбора. Это может быть текст, значение или индекс.
        by : str, optional
            Критерий выбора опции ('text', 'value', 'index'). По умолчанию 'text'.
        wait_type : str, optional
            Тип ожидания элемента перед выбором ('clickable', 'visible', 'located', 'find'). По умолчанию 'clickable'.
        """
        step_title = f"Selected option '{option}' from dropdown '{element_dict['name']}' by {by}"
        
        with allure.step(step_title):
            select_element = self.get_element(element_dict, wait_type)['element']
            select = Select(select_element)
            
            if by == 'text':
                select.select_by_visible_text(option)
            elif by == 'value':
                select.select_by_value(option)
            elif by == 'index':
                select.select_by_index(int(option))
            else:
                raise ValueError(f"Недопустимый критерий выбора опции: выберите 'text', 'value' или 'index'.")
            
            print(f"Selected option '{option}' from dropdown '{element_dict['name']}' by {by}")
    
    """ Backspace all and input with optional click, enter, and wait type """
    
    def backspace_all_and_input(self, element_dict: Dict[str, str], value: str,
                                click_first: bool = False, press_enter: bool = False,
                                wait_type: str = 'clickable') -> None:
        """
        Очищает поле ввода путем нажатий клавиши Backspace для каждого символа в поле, затем вводит новое значение.

        Parameters
        ----------
        element_dict : dict
            Словарь с информацией о поле ввода.
        value : str
            Значение для ввода.
        click_first : bool, optional
            Если True, сначала кликает по полю перед вводом текста. По умолчанию False.
        press_enter : bool, optional
            Если True, нажимает Enter после ввода значения. По умолчанию False.
        wait_type : str, optional
            Тип ожидания элемента. По умолчанию 'clickable'.
            Доступные варианты: 'clickable', 'visible', 'located', 'find', 'invisibility'.
        """
        with allure.step(
                f"{'Click and ' if click_first else ''}Backspace and input in {element_dict['name']}: {value}"):
            field_dict = self.get_element(element_dict, wait_type=wait_type)
            if click_first:
                field_dict['element'].click()
            current_value = field_dict['element'].get_attribute('value')
            for _ in range(len(current_value)):
                field_dict['element'].send_keys(Keys.BACKSPACE)
            field_dict['element'].send_keys(value)
            if press_enter:
                field_dict['element'].send_keys(Keys.ENTER)
            print(f"{'Click and ' if click_first else ''}Backspaced and input in {element_dict['name']}: {value}")
