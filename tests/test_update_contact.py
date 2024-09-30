import random
import allure
from pages.cell_list_page import CellList
from faker import Faker


@allure.story("Позитивные тесты")
@allure.feature('Редактирование контакта')
@allure.description('Тест редактирования существующего контакта: редактируем - Первый в списке, '
                    'имя, фамилия, дата рождения и адрес - Случайные, тип контакта - Случайный выбор')
def test_update_contact(base_fixture):
    base = base_fixture  # Получаем объект base из фикстуры
    cell_list_page = CellList(base.driver)  # Инициализация класса CellList
    
    # Открываем страницу CellList
    cell_list_page.open_page()
    
    # Выбираем первый контакт из списка для редактирования
    cell_list_page.click_button(cell_list_page.first_contact_card)
    
    # Создаем объект Faker для генерации случайных данных
    fake = Faker()
    
    # Генерация случайных данных: имя, фамилия и адрес
    first_name = fake.first_name()
    last_name = fake.last_name()
    address = fake.address()
    
    # Генерация случайной даты рождения в формате "Month DD, YYYY"
    birthday = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%B %d, %Y')
    
    # Извлекаем текущую выбранную категорию для контакта
    selected_category_element = cell_list_page.get_element(cell_list_page.category_select, "visible")['element']
    selected_category = selected_category_element.get_attribute('value')
    
    # Список всех возможных категорий
    contact_types = ["Family", "Friends", "Coworkers", "Businesses", "Contacts"]
    
    # Исключаем текущую категорию из списка
    available_contact_types = [contact_type for contact_type in contact_types if contact_type != selected_category]
    
    # Выбираем случайную новую категорию из оставшихся
    new_contact_type = random.choice(available_contact_types)
    
    # Редактируем имя контакта
    cell_list_page.backspace_all_and_input(cell_list_page.first_name_input, first_name)
    # Редактируем фамилию контакта
    cell_list_page.backspace_all_and_input(cell_list_page.last_name_input, last_name)
    
    # Меняем категорию контакта на случайно выбранную
    cell_list_page.select_option(cell_list_page.category_select, new_contact_type, by="text")
    
    # Редактируем дату рождения контакта
    cell_list_page.backspace_all_and_input(cell_list_page.birthday_input, birthday, press_enter=True)
    
    # Редактируем адрес контакта
    cell_list_page.backspace_all_and_input(cell_list_page.address_input, address)
    
    # Нажимаем на кнопку "Update Contact" для сохранения изменений
    cell_list_page.click_button(cell_list_page.update_contact_button)
    
    # Добавляем проверку, что количество контактов не изменилось
    cell_list_page.flexible_assert_word(cell_list_page.contact_counter_text, "0 - 30 : 250")
    
    # Добавляем информацию об обновленном контакте в отчёт Allure
    with allure.step(f"Обновленный контакт: {first_name} {last_name}, {birthday}, {address}, {new_contact_type}"):
        print(f"Обновленный контакт: {first_name} {last_name}, {birthday}, {address}, {new_contact_type}")
    
    # Склеиваем сгенерированные имя и фамилию
    expected_full_name = f"{first_name} {last_name}"
    
    # Сравниваем имя нового контакта с ожидаемым
    cell_list_page.flexible_assert_word(cell_list_page.first_contact_names, expected_full_name)
    
    # Форматируем адрес: убираем символы новой строки для корректного сравнения
    expected_address = address.replace('\n', ' ')
    
    # Сравниваем имя нового контакта с ожидаемым
    cell_list_page.flexible_assert_word(cell_list_page.first_contact_address, expected_address)
    