import datetime
import time
import re
import allure
import os
from selenium.webdriver.support.ui import Select
from typing import Any, Dict, Type, NoReturn, Optional
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# Путь к драйверу
WINDOWS_DRIVER_PATH = os.path.join('resource', 'windows', 'chromedriver.exe')


class Base:
    """
    Базовый класс содержащий методы для взаимодействия с веб-драйвером.
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
    
    """ Get driver"""
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
        # options.add_argument('--headless')  # Режим без графического интерфейса, можно активировать при необходимости
        
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(options=options, service=service)
        
        with allure.step(title="Start test"):
            print("Start test")
        
        return cls(driver)
    
    """Test finish"""
    def test_finish(self) -> None:
        """
        Завершает тест и закрывает браузер.
        """
        with allure.step(title="Test finish"):
            print("Test finish")
            self.driver.quit()
    
    """ Get current url"""
    def get_current_url(self) -> None:
        """
        Получает и выводит текущий URL адрес в консоль.
        """
        get_url = self.driver.current_url
        with allure.step(title="Current url: " + get_url):
            print("Current url: " + get_url)
    
    """ Get element with choosing a method for obtaining an element"""
    def get_element(self, element_info: Dict[str, str], wait_type: str = 'clickable') -> Dict[str, Any]:
        """
        Ожидает элемент в зависимости от выбранного типа ожидания и возвращает его.

        Parameters
        ----------
        element_info : dict
            Информация о локаторе элемента.
        wait_type : str, optional
            Тип ожидания: 'clickable', 'visible', 'located', 'find', или 'invisibility'.

        Returns
        -------
        dict
            Словарь с информацией о найденном элементе.
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
            message = ""
            if wait_type == 'clickable':
                message = f"Element '{element_info['name']}' is not clickable"
            elif wait_type == 'visible':
                message = f"Element '{element_info['name']}' is not visible"
                with allure.step(message):
                    print(message)
                # Возвращаем None, чтобы тест продолжился
                return {'name': element_info['name'], 'element': None}
            elif wait_type == 'located':
                message = f"Element '{element_info['name']}' is not located"
            elif wait_type == 'find':
                message = f"Element '{element_info['name']}' is not found"
            elif wait_type == 'invisibility':
                message = f"Element '{element_info['name']}' is not invisible"
            
            with allure.step(message):
                print(message)
            raise TimeoutException(message)

    """ Get timestamp with dot"""
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
    
    """ Assert word fix reference"""
    def assert_word(self, element_dict: Dict[str, str], wait_type: str = 'clickable') -> NoReturn:
        """
        Проверяет, что текст элемента соответствует заданному значению. Если предоставлен 'reference_xpath',
        использует его для точного определения элемента для проверки текста.

        Parameters
        ----------
        element_dict : dict
            Словарь с информацией о локаторе элемента и ожидаемым текстом.
            Может включать 'reference_xpath' для спецификации элемента, текст которого следует проверять.
        wait_type : str, optional
            Тип ожидания элемента ('clickable', 'visible', 'located', 'find').

        Raises
        ------
        AssertionError
            Если текст элемента не соответствует ожидаемому значению.
        """
        if 'reference_xpath' in element_dict:
            reference_element = self.get_element(
                {'name': 'Reference element', 'xpath': element_dict['reference_xpath']}, wait_type='located')['element']
            time.sleep(0.1)  # Фиксированная задержка
            value_word = reference_element.text
        else:
            element = self.get_element(element_dict, wait_type=wait_type)['element']
            time.sleep(0.1)  # Фиксированная задержка
            value_word = element.text
        
        with allure.step(title=f"Assert \"{value_word}\" == \"{element_dict['reference']}\""):
            assert re.fullmatch(element_dict['reference'],
                                value_word), f"Expected '{element_dict['reference']}', but found '{value_word}'."
            print(f"Assert \"{value_word}\" == \"{element_dict['reference']}\"")
            
        """ Assert word input reference"""
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
            Тип ожидания элемента ('clickable', 'visible', 'located', 'find').

        Raises
        ------
        AssertionError
            Если текст элемента или его атрибут 'value' не соответствует ожидаемому значению.
        """
        element = self.get_element(element_dict, wait_type=wait_type)['element']
        time.sleep(0.1)  # Фиксированная задержка
        actual_text = element.text or element.get_attribute('value')  # Получаем текст или значение атрибута 'value'
        with allure.step(title=f"Assert \"{actual_text}\" == \"{reference_value}\""):
            assert re.fullmatch(reference_value,
                                actual_text), f"Expected '{reference_value}', but found '{actual_text}'."
            print(f"Assert \"{actual_text}\" == \"{reference_value}\"")
    
    """ Get screenshot"""
    def get_screenshot(self, test_name: str = None) -> NoReturn:
        """
        Сохраняет скриншот текущего состояния браузера в базовую папку.
        Если тест запускается с Allure, прикрепляет скриншот к отчету Allure.
        """
        # Всегда сохраняем скриншот в базовую папку
        screenshot_dir = 'C:\\Users\\Gans\\PycharmProjects\\CellListAuto\\screens'
        print(f"Saving screenshot to default directory: {screenshot_dir}")
        
        # Создаем имя файла скриншота с таймштампом и названием теста (если указано)
        timestamp = self.get_timestamp_dot()
        if test_name:
            name_screenshot = f'{test_name}_{timestamp}.png'
        else:
            name_screenshot = f'{timestamp}.png'
        
        # Полный путь для сохранения скриншота
        screenshot_path = os.path.join(screenshot_dir, name_screenshot)
        
        # Проверяем, существует ли папка, и создаем ее, если не существует
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        # Сохраняем скриншот
        self.driver.save_screenshot(screenshot_path)
        
        # Шаг в отчете Allure, если тест запускается с Allure, прикрепляем скриншот
        with allure.step(title="Screen taken: " + name_screenshot):
            print(f"Screenshot saved successfully at: {screenshot_path}")
            
            # Прикрепляем файл скриншота только если используется Allure
            if hasattr(self, 'allure_dir') and self.allure_dir:
                allure.attach.file(screenshot_path, name="Screenshot", attachment_type=allure.attachment_type.PNG)
    
    """ Click button"""
    def click_button(self, element_dict: Dict[str, str], index: int = 1, do_assert: Optional[bool] = False,
                     wait_type: str = 'clickable') -> NoReturn:
        """
        Кликает по кнопке с заданным типом ожидания и опционально по индексу элемента.
        Может выполнять дополнительную проверку текста элемента после клика (ассерт).

        Parameters
        ----------
        element_dict : dict
            Словарь с информацией о кнопке для клика.
        index : int, optional
            Индекс элемента в списке однотипных элементов. По умолчанию 1 (первый элемент).
        do_assert : bool, optional
            Если True, выполнит дополнительную проверку текста элемента после клика.
        wait_type : str, optional
            Тип ожидания элемента перед кликом ('clickable', 'visible', 'located', 'find'), по умолчанию 'clickable'.

        """
        element_name = f"{element_dict['name']} index {index}" if index > 1 else element_dict['name']
        locator = f"({element_dict['xpath']})[{index}]" if index > 1 else element_dict['xpath']
        updated_element_dict = {"name": element_name, "xpath": locator}
        
        with allure.step(title=f"Click on {element_name}"):
            button_dict = self.get_element(updated_element_dict, wait_type)
            button_dict['element'].click()
            print(f"Click on {button_dict['name']}")
        
        if do_assert:
            self.assert_word(element_dict)
    
    """ Input in field with optional click, enter, index """
    def input_in_field(self, element_dict: Dict[str, str], value: str, click_first: bool = False,
                       press_enter: bool = False, safe: bool = False,
                       wait_type: str = 'clickable', index: int = 1) -> None:
        """
        Универсальный метод для ввода текста в поле с опциональным кликом перед вводом и нажатием Enter после.
        Поддерживает дополнительные параметры для управления взаимодействием, включая индекс элемента
        и выбор типа ожидания доступности элемента.

        Parameters
        ----------
        element_dict : dict
            Словарь с информацией о поле ввода.
        value : str
            Значение для ввода.
        click_first : bool, optional
            Если True, сначала кликает по полю перед вводом текста.
        press_enter : bool, optional
            Если True, нажимает Enter после ввода текста.
        safe : bool, optional
            Если True, заменяет введенное значение на символы "***" в логах.
        wait_type : str, optional
            Тип ожидания элемента ('clickable', 'visible', 'located', 'find'), по умолчанию 'clickable'.
        index : int, optional
            Индекс элемента в списке однотипных элементов. По умолчанию 1 (первый элемент).

        """
        log_value = "***" if safe else value
        element_name = f"{element_dict['name']} index {index}" if index > 1 else element_dict['name']
        locator = f"({element_dict['xpath']})[{index}]" if index > 1 else element_dict['xpath']
        updated_element_dict = {"name": element_name, "xpath": locator}
        
        with allure.step(title=f"{('Click and ' if click_first else '')}Input in {element_name}: " + log_value):
            field_dict = self.get_element(updated_element_dict, wait_type)
            if click_first:
                field_dict['element'].click()
            field_dict['element'].send_keys(value)
            if press_enter:
                field_dict['element'].send_keys(Keys.ENTER)
            print(f"{('Click and ' if click_first else '')}Input in {field_dict['name']}: " + log_value)
    
    """Select option in dropdown by text, value or index """
    
    def select_option(self, element_dict: Dict[str, str], option: str, by: str = 'text',
                      wait_type: str = 'clickable') -> None:
        """
        Выбирает опцию в выпадающем списке <select> с опциональным типом ожидания и шагами Allure.

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
        # Формируем шаг Allure с названием выпадающего списка
        step_title = f"Select '{option}' from dropdown '{element_dict['name']}'"
        
        with allure.step(step_title):
            # Получаем элемент <select> с заданным типом ожидания
            select_element = self.get_element(element_dict, wait_type)['element']
            select = Select(select_element)
            
            # Выбор опции в зависимости от критерия
            if by == 'text':
                select.select_by_visible_text(option)
            elif by == 'value':
                select.select_by_value(option)
            elif by == 'index':
                select.select_by_index(int(option))
            else:
                raise ValueError(f"Недопустимый критерий выбора опции: выберите 'text', 'value' или 'index'.")
            
            # Вывод в консоль с именем выпадающего списка
            print(f"Selected option '{option}' from dropdown '{element_dict['name']}' by {by}")
