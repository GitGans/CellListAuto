import allure
from base.base_class import Base


class CellList(Base):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.url = 'https://samples.gwtproject.org/samples/Showcase/Showcase.html#!CwCellList'

    # Locators
    first_name_input = {
        "xpath": "(//input[@class='gwt-TextBox'])[1]",
        "name": 'First Name fild'
    }
    last_name_input = {
        "xpath": "(//input[@class='gwt-TextBox'])[2]",
        "name": 'Last Name fild'
    }
    category_select = {
        "xpath": "//select[@class='gwt-ListBox']",
        "name": 'Category dropdown'
    }
    birthday_input = {
        "xpath": "//input[@class='gwt-DateBox']",
        "name": 'Birthday fild'
    }
    address_input = {
        "xpath": "//textarea[@class='gwt-TextArea']",
        "name": 'Address fild'
    }
    update_contact_button = {
        "xpath": "//button[@class='gwt-Button' and text()='Update Contact']",
        "name": 'Update Contact button'
    }
    create_contact_button = {
        "xpath": "//button[@class='gwt-Button' and text()='Create Contact']",
        "name": 'Create Contact button'
    }
    generate_50_contacts_button = {
        "xpath": "//button[@class='gwt-Button' and text()='Generate 50 Contacts']",
        "name": 'Generate 50 Contacts button'
    }
    contact_counter_text = {
        "xpath": "(//div[@class='gwt-HTML'])[2]",
        "name": 'Contact counter text'
    }
    
    # Methods
    """Open page"""
    def open_page(self):
        """
        Открывает страницу CellList.
        """
        with allure.step("Open CellList page"):
            self.driver.get(self.url)
            print("Opening CellList page: " + self.url)
    
    