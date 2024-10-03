import time
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
        "name": 'First Name field'
    }
    last_name_input = {
        "xpath": "(//input[@class='gwt-TextBox'])[2]",
        "name": 'Last Name field'
    }
    category_select = {
        "xpath": "//select[@class='gwt-ListBox']",
        "name": 'Category dropdown'
    }
    birthday_input = {
        "xpath": "//input[@class='gwt-DateBox']",
        "name": 'Birthday field'
    }
    address_input = {
        "xpath": "//textarea[@class='gwt-TextArea']",
        "name": 'Address field'
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
    contact_list = {
        "xpath": "//div[contains(@class, 'CMWVMEC-p-b')]",
        "name": 'Contact list'
    }
    first_contact_card = {
        "xpath": "//div[@__idx='0']",
        "name": 'First contact card'
    }
    first_contact_names = {
        "xpath": "(//td[@style='font-size:95%;'])[1]",
        "name": 'First contact names'
    }
    first_contact_address = {
        "xpath": "(//td[@style='font-size:95%;']/ancestor::tr/following-sibling::tr/td)[1]",
        "name": 'First contact address'
    }
    new_contact_card = {
        "xpath": "//div[@__idx='250']",
        "name": 'New contact card'
    }
    new_contact_names = {
        "xpath": "(//td[@style='font-size:95%;'])[251]",
        "name": 'New contact names'
    }
    new_contact_address = {
        "xpath": "(//td[@style='font-size:95%;']/ancestor::tr/following-sibling::tr/td)[251]",
        "name": 'New contact address'
    }
    
    # Methods
    """ Open page """
    
    def open_page(self) -> None:
        """
        Открывает страницу CellList.
        """
        with allure.step("Open CellList page"):
            self.driver.maximize_window()
            self.driver.get(self.url)
            print(f"Opening CellList page: {self.url}")
    
    """ Scroll to bottom """
    
    def scroll_to_bottom(self) -> None:
        """
        Скроллит список контактов до самого низа, пока не будет достигнут конец списка.
        """
        with allure.step("Scroll to the bottom of the contact list"):
            print("Scroll to the bottom of the contact list")
            contact_list_element = self.get_element(self.contact_list, wait_type="visible")['element']
            last_height = self.driver.execute_script("return arguments[0].scrollHeight", contact_list_element)
            
            while True:
                self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", contact_list_element)
                time.sleep(0.1)
                new_height = self.driver.execute_script("return arguments[0].scrollHeight", contact_list_element)
                
                if new_height == last_height:
                    print("Reached the bottom of the contact list.")
                    with allure.step("Reached the bottom of the contact list"):
                        pass
                    break
                
                else:
                    last_height = new_height
    
    """ Scroll to top """
    
    def scroll_to_top(self) -> None:
        """
        Скроллит список контактов до самого верха, пока не будет достигнут верх списка.
        """
        with allure.step("Scroll to the bottom of the contact list"):
            print("Scroll to the bottom of the contact list")
            contact_list_element = self.get_element(self.contact_list, wait_type="visible")['element']
            scroll_position = self.driver.execute_script("return arguments[0].scrollTop", contact_list_element)
            
            while scroll_position > 0:
                self.driver.execute_script("arguments[0].scrollTo(0, 0);", contact_list_element)
                time.sleep(0.1)
                scroll_position = self.driver.execute_script("return arguments[0].scrollTop", contact_list_element)
                
                if scroll_position == 0:
                    print("Reached the top of the contact list.")
                    with allure.step("Reached the top of the contact list"):
                        pass
                    break
