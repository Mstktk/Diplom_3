from selenium.webdriver.common.by import By

class LoginPageLocator:
    FORGOT_PASSWORD_BUTTON = (By.XPATH, '//a[@href="/forgot-password"]')
    LOGIN_BUTTON = (By.XPATH,'//button[contains(text(), "Войти")]')
    EMAIL_FIELD = (By.XPATH, '//input[@name="name"]')
    PASSWORD_FIELD = (By.XPATH, '//input[@name="Пароль"]')
    
    
    BUT_FORGOT_PASSWORD = FORGOT_PASSWORD_BUTTON