import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from curls import Curls
from data import PersonalData
from locators.login_page_locator import LoginPageLocator
from locators.main_page_locator import MainPageLocator
from pages.base_page import BasePage

@pytest.fixture(params=['chrome', 'firefox'])
def driver(request):
    driver = None
    browser_name = request.param
    
    try:
        if browser_name == 'chrome':
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1920,1080')
            
            try:
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                print(f"ChromeDriverManager failed: {e}")
                driver = webdriver.Chrome(options=options)
                
        elif browser_name == 'firefox':
            options = webdriver.FirefoxOptions()
            options.add_argument('--width=1920')
            options.add_argument('--height=1080')
            
            try:
                service = FirefoxService(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service, options=options)
            except Exception as e:
                print(f"GeckoDriverManager failed: {e}")
                driver = webdriver.Firefox(options=options)
        
        if driver:
            driver.maximize_window()
            driver.implicitly_wait(30)  # Увеличиваем неявное ожидание
            
        yield driver
        
    except Exception as e:
        print(f"Error initializing {browser_name} driver: {e}")
        pytest.skip(f"Could not initialize {browser_name} driver")
    
    finally:
        if driver:
            driver.quit()

@pytest.fixture
def login_driver(driver):
    base_page = BasePage(driver)
    attempts = 2

    for attempt in range(attempts):
        try:
            base_page.going_url(Curls.LOGIN_URL)
            base_page.wait_for_element(LoginPageLocator.EMAIL_FIELD, timeout=40)
            base_page.wait_for_element(LoginPageLocator.PASSWORD_FIELD, timeout=40)

            try:
                base_page.wait_hide_element(MainPageLocator.OVERLAY, timeout=15)
            except TimeoutException:
                # Оверлей может не появиться — продолжаем
                pass

            base_page.send_text_to_input(LoginPageLocator.EMAIL_FIELD, PersonalData.EMAIL)
            base_page.send_text_to_input(LoginPageLocator.PASSWORD_FIELD, PersonalData.PASSWORD)
            base_page.click_on_element(LoginPageLocator.LOGIN_BUTTON, timeout=40)
            base_page.wait_for_element(MainPageLocator.TEXT_COLLECT_BURGER, timeout=40)
            return driver

        except TimeoutException as exc:
            print(f"Login attempt {attempt + 1} failed: {exc}")
            if attempt == attempts - 1:
                raise
            driver.refresh()

    return driver