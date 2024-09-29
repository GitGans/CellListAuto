import allure
from faker import Faker
from pages.cell_list_page import CellList


@allure.feature('Create Contact')
@allure.description('Test creating a new contact: '
                    'name, surname, date of birth and address - Random, contact type - Contacts')
def test_create_contact_type_contacts(base_fixture):
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
    # Генерация случайной даты рождения в формате "September 29, 2000"
    birthday = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%B %d, %Y')
    # Вводим имя в поле First Name
    cell_list_page.input_in_field(cell_list_page.first_name_input, first_name)
    # Вводим фамилию в поле Last Name
    cell_list_page.input_in_field(cell_list_page.last_name_input, last_name)
    # Выбираем тип контакта в выпадающем списке как "Contacts"
    cell_list_page.select_option(cell_list_page.category_select, "Contacts", by="text")
    # Вводим дату рождения в поле Birthday и нажимаем Enter
    cell_list_page.input_in_field(cell_list_page.birthday_input, birthday, press_enter=True)
    # Вводим адрес в поле Address
    cell_list_page.input_in_field(cell_list_page.address_input, address)
    # Нажимаем на кнопку "Create Contact"
    cell_list_page.click_button(cell_list_page.create_contact_button)
    # Добавляем проверку количества контактов
    cell_list_page.flexible_assert_word(cell_list_page.contact_counter_text, "0 - 30 : 251")
    # Добавляем информацию о созданном контакте в отчёт Allure
    with allure.step(f"Contact created: {first_name} {last_name}, {birthday}, {address}"):
        print(f"Contact created: {first_name} {last_name}, {birthday}, {address}")
    