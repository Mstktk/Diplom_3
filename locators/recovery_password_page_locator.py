from selenium.webdriver.common.by import By

class RecoveryPageLocator:
    RECOVERY_PASSWORD_HEADER = (By.XPATH, '//h2[.="Восстановление пароля"]')
    EMAIL_FIELD = (By.XPATH, '//input[@class="text input__textfield text_type_main-default"]')
    RECOVERY_BUTTON = (By.XPATH, '//button[.="Восстановить"]')
    SHOW_HIDE_PASSWORD_BUTTON = (By.XPATH, '//div[@class="input__icon input__icon-action"]')
    ACTIVE_PASSWORD_FIELD = (By.XPATH, '//label[contains(text(), "Пароль")]/ancestor::div[contains(@class, "input_type")]')
    
   
    FIELD_EMAIL = EMAIL_FIELD
    BUT_RECOVERY = RECOVERY_BUTTON
    BUT_SHOW_HIDE_PASSWORD = SHOW_HIDE_PASSWORD_BUTTON