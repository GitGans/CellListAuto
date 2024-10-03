import allure
from pages.cell_list_page import CellList


@allure.story("Позитивные тесты")
@allure.feature('Скролл списка')
@allure.description('Тест скролла: скроллим до конца списка, затем возвращаемся к началу списка.')
def test_scroll_list(base_fixture):
    base = base_fixture  # Получаем объект base из фикстуры
    cell_list_page = CellList(base.driver)  # Инициализация класса CellList
    
    # Открываем страницу
    cell_list_page.open_page()
    
    # Проверяем количество контактов в начале
    cell_list_page.flexible_assert_word(cell_list_page.contact_counter_text, "0 - 30 : 250")
    
    # Скроллим до конца списка
    cell_list_page.scroll_to_bottom()
    
    # Проверяем количество контактов после скролла вниз
    cell_list_page.flexible_assert_word(cell_list_page.contact_counter_text, "0 - 250 : 250")
    
    # Скроллим до начала списка
    cell_list_page.scroll_to_top()
    
    # Проверяем видимость первого контакта в списке
    with allure.step("First contact card is visible"):
        cell_list_page.get_element(cell_list_page.first_contact_card, "visible")
        print("First contact card is visible")
    