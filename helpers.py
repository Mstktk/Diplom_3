import random
from locators.main_page_locator import MainPageLocator
from selenium.webdriver.common.by import By

def get_ingredient(category):
    if category not in MainPageLocator.INGREDIENT_LOCATOR:
        raise ValueError(f"Категория {category} не существует!")
    return random.choice(MainPageLocator.INGREDIENT_LOCATOR[category])

def get_order_locator(href):
    return By.XPATH, f'//a[contains(@href, "{href}")]'
