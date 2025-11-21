import allure
import time
from curls import Urls
from locators.order_feed_page_locator import OrderFeedLocator
from pages.base_page import BasePage
from locators.main_page_locator import MainPageLocator


class MainPage(BasePage):
    @allure.step('Клик на кнопку "Личный кабинет"')
    def click_but_personal_account(self):
        self.click_on_element(MainPageLocator.BUT_PERSONAL_ACCOUNT)

    @allure.step('Клик на кнопку "Конструктор"')
    def click_but_constructor(self):
        self.click_on_element(MainPageLocator.BUT_CONSTRUCTOR)

    @allure.step('Клик на кнопку "Лента заказов"')
    def click_but_feed_order(self):
        self.click_on_element(MainPageLocator.BUT_FEED_ORDER)

    @allure.step('Клик на крестик в карточке ингредиента')
    def click_but_cross(self):
        self.click_on_element(MainPageLocator.BUT_CROSS)

    @allure.step('Клик на кнопку "Оформить заказ"')
    def click_but_create_order(self):
        self.click_on_element(MainPageLocator.BUT_CREATE_ORDER)

    @allure.step('Клик на ингредиент')
    def click_ingredient(self, locator):
        self.click_on_element(locator)

    @allure.step('Переход на страницу авторизации')
    def going_page_login(self):
        self.going_url(Urls.LOGIN_URL)

    @allure.step('Переход на главную страницу')
    def going_main_page(self):
        self.going_url(Urls.MAIN_URL)

    @allure.step('Подождать загрузки главной страницы')
    def wait_load_main_page(self):
        self.wait_for_element(MainPageLocator.TEXT_COLLECT_BURGER)

    @allure.step('Подождать загрузки карточки ингредиента')
    def wait_load_card_ingredient(self):
        return self.wait_for_element(MainPageLocator.HEAD_INGREDIENT_DETAIL)

    @allure.step('Подождать загрузки номера заказа')
    def wait_load_order_card(self):
        for locator in (
            OrderFeedLocator.ORDER_ID_AFTER_PURCHASE,
            MainPageLocator.TEXT_ORDER_ID,
            OrderFeedLocator.MODAL_CONTENT,
            OrderFeedLocator.MODAL_OVERLAY,
        ):
            try:
                element = self.wait_for_element(locator, timeout=40)
                if element and element.text:
                    return element.text
            except Exception:
                continue
        return ""

    @allure.step('Подождать загрузки страницы "Лента заказов"')
    def wait_load_page_feed_order(self):
        self.wait_for_element(MainPageLocator.TEXT_FEED_ORDER)

    @allure.step('Подождать скрытия карточки ингредиента')
    def wait_hide_card_ingredient(self):
        return self.wait_hide_element(MainPageLocator.HEAD_INGREDIENT_DETAIL)

    @allure.step('Получить текущего URL страницы')
    def get_url_page(self):
        return self.get_url()

    @allure.step('Скролл до элемента на странице')
    def scroll_to_element_page(self, locator):
        self.scroll_to_element(locator)

    @allure.step('Открытие карточки ингредиента')
    def open_card_ingredient(self, category):
        from helpers import get_ingredient
        locator = get_ingredient(category)
        self.going_main_page()
        self.wait_load_main_page()
        self.scroll_to_element(locator[1])
        self.wait_for_element(locator[1])
        self.click_ingredient(locator[1])
        self.wait_load_card_ingredient()

    @allure.step('Перетащить ингредиент')
    def drag_and_drop_ingredient(self, locator):
        self.wait_for_element(locator)
        source = self.find_element(locator)
        target = self.find_element(MainPageLocator.BURGER_CONSTRUCTOR)
        self.drag_and_drop_element(source, target)
        # Ждем обновления счетчика ингредиента
        self.wait_for_element(MainPageLocator.BURGER_CONSTRUCTOR)

    @allure.step('Получить количество добавленных ингредиентов')
    def get_count_element(self, locator):
        try:
            return self.get_text_on_element(locator)
        except:
            return "0"

    @allure.step('Получить локатор ингредиента')
    def get_locator_ingredient(self, category):
        from helpers import get_ingredient
        return get_ingredient(category)

    @allure.step('Собрать бургер')
    def add_ingredient_in_burger(self):
        bun_locator = self.get_locator_ingredient('buns')
        self.drag_and_drop_ingredient(bun_locator[1])
        self.wait_for_element(MainPageLocator.BURGER_CONSTRUCTOR)

        sauces_locator = self.get_locator_ingredient('souses')
        self.drag_and_drop_ingredient(sauces_locator[1])
        self.wait_for_element(MainPageLocator.BURGER_CONSTRUCTOR)

        toppings_locator = self.get_locator_ingredient('toppings')
        self.drag_and_drop_ingredient(toppings_locator[1])
        self.wait_for_element(MainPageLocator.BURGER_CONSTRUCTOR)