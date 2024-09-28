import pytest
from base.base_class import Base


@pytest.fixture
def base_fixture():
    # Инициализация драйвера через метод Base.get_driver()
    base = Base.get_driver()
    
    # Возвращаем экземпляр Base для использования в тестах
    yield base
    
    # Завершаем тест и закрываем драйвер
    base.test_finish()


# Хук для сохранения скриншота в случае провала теста
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Вызов теста и получение его результата
    outcome = yield
    report = outcome.get_result()
    
    # Получаем кортеж (base) через фикстуру
    base_fixture = item.funcargs.get('base_fixture', None)
    
    if base_fixture:
        base = base_fixture  # Извлекаем base
        
        # Если тест завершился с ошибкой и base доступен
        if report.when == "call" and report.failed and base:
            # Получаем имя теста
            test_name = item.nodeid.replace("::", "_").replace("/", "_")
            base.get_screenshot(test_name)  # Передаем имя теста в метод скриншота
