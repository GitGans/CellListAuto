import random
import re
import allure
from pages.cell_list_page import CellList
from faker import Faker

# Список возможных значений для типа контакта
contact_types = ["Family", "Friends", "Coworkers", "Businesses", "Contacts"]


@allure.story("Позитивные тесты")
@allure.feature('Создание контакта')
@allure.description('Тест создания нового контакта со всеми полями: '
                    'имя, фамилия, дата рождения и адрес - Случайные, тип контакта - Случайный выбор')
def test_create_contact_full(base_fixture):
    base = base_fixture  # Получаем объект base из фикстуры
    cell_list_page = CellList(base.driver)  # Инициализация класса CellList
    
    # Открываем страницу
    cell_list_page.open_page()
    
    # Создаем объект Faker для генерации случайных данных
    fake = Faker()
    
    # Генерация случайных данных: имя, фамилия и адрес
    first_name = fake.first_name()
    last_name = fake.last_name()
    address = fake.address()
    
    # Генерация случайной даты рождения в формате "Month DD, YYYY"
    birthday = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%B %d, %Y')
    
    # Выбор случайного типа контакта
    random_contact_type = random.choice(contact_types)
    
    # Вводим данные для нового контакта
    cell_list_page.input_in_field(cell_list_page.first_name_input, first_name)
    cell_list_page.input_in_field(cell_list_page.last_name_input, last_name)
    
    # Выбираем случайный тип контакта
    cell_list_page.select_option(cell_list_page.category_select, random_contact_type, by="text")
    
    # Вводим дату рождения
    cell_list_page.input_in_field(cell_list_page.birthday_input, birthday, press_enter=True)
    
    # Вводим адрес
    cell_list_page.input_in_field(cell_list_page.address_input, address)
    
    # Нажимаем на кнопку "Create Contact"
    cell_list_page.click_button(cell_list_page.create_contact_button)
    
    # Добавляем проверку количества контактов
    cell_list_page.flexible_assert_word(cell_list_page.contact_counter_text, "0 - 30 : 251")
    
    # Добавляем информацию о созданном контакте в отчёт Allure
    with allure.step(f"Создан контакт: {first_name} {last_name}, {birthday}, {address}, {random_contact_type}"):
        print(f"Создан контакт: {first_name} {last_name}, {birthday}, {address}, {random_contact_type}")
    
    # Скроллим до конца списка после создания контакта
    cell_list_page.scroll_to_bottom()
    
    # Добавляем проверку счетчика контактов после скролла
    cell_list_page.flexible_assert_word(cell_list_page.contact_counter_text, "0 - 251 : 251")
    
    # Склеиваем сгенерированные имя и фамилию
    expected_full_name = f"{first_name} {last_name}"
    
    # Сравниваем имя нового контакта с ожидаемым
    cell_list_page.flexible_assert_word(cell_list_page.new_contact_names, expected_full_name)
    
    # Форматируем адрес: убираем символы новой строки для корректного сравнения
    expected_address = address.replace('\n', ' ')
    
    # Сравниваем адрес нового контакта с ожидаемым
    cell_list_page.flexible_assert_word(cell_list_page.new_contact_address, expected_address)


@allure.story("Позитивные тесты")
@allure.feature('Создание контакта')
@allure.description('Тест создания нового контакта с минимальным набором полей: '
                    'дата рождения - Случайная, тип контакта - Случайный выбор')
def test_create_contact_min(base_fixture):
    base = base_fixture  # Получаем объект base из фикстуры
    cell_list_page = CellList(base.driver)  # Инициализация класса CellList
    
    # Открываем страницу
    cell_list_page.open_page()
    
    # Создаем объект Faker для генерации случайных данных
    fake = Faker()
    
    # Генерация случайной даты рождения в формате "Month DD, YYYY"
    birthday = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%B %d, %Y')
    
    # Выбор случайного типа контакта
    random_contact_type = random.choice(contact_types)
    
    # Выбираем случайный тип контакта
    cell_list_page.select_option(cell_list_page.category_select, random_contact_type, by="text")
    
    # Вводим дату рождения
    cell_list_page.input_in_field(cell_list_page.birthday_input, birthday, press_enter=True)
    
    # Нажимаем на кнопку "Create Contact"
    cell_list_page.click_button(cell_list_page.create_contact_button)
    
    # Добавляем проверку количества контактов
    cell_list_page.flexible_assert_word(cell_list_page.contact_counter_text, "0 - 30 : 251")
    
    # Добавляем информацию о созданном контакте в отчёт Allure
    with allure.step(f"Создан контакт: {birthday}, {random_contact_type}"):
        print(f"Создан контакт: {birthday}, {random_contact_type}")
    
    # Скроллим до конца списка после создания контакта
    cell_list_page.scroll_to_bottom()
    
    # Добавляем проверку счетчика контактов после скролла
    cell_list_page.flexible_assert_word(cell_list_page.contact_counter_text, "0 - 251 : 251")
    
    # Выбираем новый контакт из списка для проверки
    cell_list_page.click_button(cell_list_page.new_contact_card)
    
    # Удаляем ведущие нули перед одноцифровыми днями в дате
    formatted_birthday = re.sub(r'(?<=\s)0(\d,)', r'\1', birthday)
    
    # Сравниваем дату рождения нового контакта с ожидаемой
    cell_list_page.flexible_assert_word(cell_list_page.birthday_input, formatted_birthday)


@allure.story("Негативные тесты")
@allure.feature('Создание контакта')
@allure.description('Тест создания контакта без указания даты рождения: '
                    'имя, фамилия и адрес - Случайные, тип контакта - Случайный выбор')
def test_create_contact_neg(base_fixture):
    base = base_fixture  # Получаем объект base из фикстуры
    cell_list_page = CellList(base.driver)  # Инициализация класса CellList
    
    # Открываем страницу
    cell_list_page.open_page()
    
    # Создаем объект Faker для генерации случайных данных
    fake = Faker()
    
    # Генерация случайных данных: имя, фамилия и адрес
    first_name = fake.first_name()
    last_name = fake.last_name()
    address = fake.address()
    
    # Выбор случайного типа контакта
    random_contact_type = random.choice(contact_types)
    
    # Вводим данные для нового контакта
    cell_list_page.input_in_field(cell_list_page.first_name_input, first_name)
    cell_list_page.input_in_field(cell_list_page.last_name_input, last_name)
    
    # Выбираем случайный тип контакта
    cell_list_page.select_option(cell_list_page.category_select, random_contact_type, by="text")
    
    # Вводим адрес
    cell_list_page.input_in_field(cell_list_page.address_input, address)
    
    # Нажимаем на кнопку "Create Contact"
    cell_list_page.click_button(cell_list_page.create_contact_button)
    
    # Добавляем проверку количества контактов
    cell_list_page.flexible_assert_word(cell_list_page.contact_counter_text, "0 - 30 : 250")
    
    # Скроллим до конца списка после создания контакта
    cell_list_page.scroll_to_bottom()
    
    # Добавляем проверку счетчика контактов после скролла
    cell_list_page.flexible_assert_word(cell_list_page.contact_counter_text, "0 - 250 : 250")
    
    # Проверяем отсутствие нового контакта в списке
    with allure.step("New contact card is invisible"):
        cell_list_page.get_element(cell_list_page.new_contact_card, "invisibility")
        print("New contact not found")
        