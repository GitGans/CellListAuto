import allure
from pages.cell_list_page import CellList


@allure.story("Позитивные тесты")
@allure.feature('Генерации контактов')
@allure.description('Тест генерации 50 новых контактов.')
def test_generate_contact(base_fixture):
    base = base_fixture  # Получаем объект base из фикстуры
    cell_list_page = CellList(base.driver)  # Инициализация класса CellList
    
    # Открываем страницу
    cell_list_page.open_page()
    
    # Нажимаем на кнопку "Generate 50 Contacts"
    cell_list_page.click_button(cell_list_page.generate_50_contacts_button)
    
    # Добавляем проверку количества контактов
    cell_list_page.flexible_assert_word(cell_list_page.contact_counter_text, "0 - 30 : 300")
        
    # Скроллим до конца списка после создания контакта
    cell_list_page.scroll_to_bottom()
    
    # Добавляем проверку счетчика контактов после скролла
    cell_list_page.flexible_assert_word(cell_list_page.contact_counter_text, "0 - 300 : 300")
    