import allure
import time
import requests
from selenium.webdriver.common.by import By
from curls import Urls
from locators.main_page_locator import MainPageLocator
from locators.personal_account_page_locator import PersonalAccountPageLocator
from pages.base_page import BasePage
from locators.order_feed_page_locator import OrderFeedLocator

class OrderFeedPage(BasePage):
    @allure.step('Клик на заказ на странице "Лента заказов"')
    def click_on_order_in_order_feed(self, number):
        locator = OrderFeedLocator.order_history_locator(number)
        self.wait_for_element(locator, timeout=20)
        self.scroll_to_element(locator)
        self.click_on_element(locator)
        self.wait_load_order_card()

    @allure.step('Клик на последний заказ в "История заказов"')
    def click_on_last_order(self):
        self.wait_for_element(PersonalAccountPageLocator.LAST_ORDER_IN_HISTORY, timeout=20)
        self.scroll_to_element(PersonalAccountPageLocator.LAST_ORDER_IN_HISTORY)
        self.click_on_element(PersonalAccountPageLocator.LAST_ORDER_IN_HISTORY)
        self.wait_load_order_card()

    @allure.step('Клик на заказ из истории заказов')
    def click_order_on_href(self, href):
        end_href = href.split('/')[-1]
        order_locator = (By.XPATH, f'//a[contains(@href, "{end_href}")]')
        self.wait_for_element(order_locator, timeout=20)
        self.click_on_element(order_locator)
        self.wait_load_order_card()

    @allure.step('Переход на страницу "История заказов"')
    def going_in_order_history(self):
        self.going_url(Urls.ACCOUNT_URL)
        self.wait_for_element(PersonalAccountPageLocator.BUT_ORDER_HISTORY, timeout=20)
        self.click_on_element(PersonalAccountPageLocator.BUT_ORDER_HISTORY)
        self.wait_for_element(PersonalAccountPageLocator.TEXT_CHANGE_DATA, timeout=20)

    @allure.step('Переход на страницу "Лента заказов"')
    def going_in_feed_order(self):
        self.going_url(Urls.FEED_URL)
        self.wait_for_element(MainPageLocator.TEXT_FEED_ORDER, timeout=20)

    @allure.step('Подождать появления номера заказа в разделе "В работе"')
    def wait_order_in_work(self):
        return self.wait_for_element(OrderFeedLocator.ORDER_IN_WORK_1, timeout=20)

    @allure.step('Получить ссылку заказа')
    def get_link_order(self, number):
        locator = OrderFeedLocator.order_history_locator(number)
        element = self.wait_for_element(locator, timeout=20)
        return element.get_attribute('href')

    @allure.step('Получить количество заказов')
    def get_count_orders(self, locator):
        count_text = self.get_text_on_element(locator)
        return int(count_text)

    @allure.step('Получить ссылку последнего заказа')
    def get_href_last_order(self):
        element = self.wait_for_element(PersonalAccountPageLocator.LAST_ORDER_IN_HISTORY, timeout=20)
        return element.get_attribute('href')

    @allure.step('Получить ID последнего заказа')
    def get_id_last_order(self):
        element = self.wait_for_element(PersonalAccountPageLocator.LAST_ORDER_IN_HISTORY, timeout=20)
        return element.text

    @allure.step('Получить ID заказов в работе')
    def get_id_order_in_work(self):
        elements = self.wait_load_all_elements(OrderFeedLocator.ORDER_IN_WORK_1)
        return [element.text for element in elements]

    @allure.step('Получить ID готовых заказов')
    def get_id_orders_ready(self):
        elements = self.wait_load_all_elements(OrderFeedLocator.ORDER_READY_ITEMS)
        return [element.text for element in elements]

    @allure.step('Подождать появления нового заказа в истории')
    def wait_new_order_in_history(self, previous_text, timeout=60, poll_frequency=3):
        end_time = time.time() + timeout
        last_value = previous_text

        while time.time() < end_time:
            try:
                current_text = self.get_id_last_order()
                if current_text and current_text != previous_text:
                    return current_text
                last_value = current_text
            except Exception:
                pass

            time.sleep(poll_frequency)
            self.refresh_page()
            self.wait_for_element(PersonalAccountPageLocator.LAST_ORDER_IN_HISTORY, timeout=20)

        raise TimeoutError(f"Новый заказ не появился в истории. Последний текст: {last_value}")

    @allure.step('Подождать появления конкретного заказа в разделе "В работе"')
    def wait_for_order_id_in_work(self, order_id, timeout=120, poll_frequency=5):
        normalized_target = str(int(order_id))
        end_time = time.time() + timeout
        last_seen = []

        while time.time() < end_time:
            try:
                ids_in_work = self.get_id_order_in_work()
                last_seen = ids_in_work
                normalized_ids = [
                    str(int(order.strip()))
                    for order in ids_in_work
                    if order and order.strip().isdigit()
                ]
                if normalized_target in normalized_ids:
                    return True
            except Exception:
                pass
            
            try:
                self.refresh_page()
                self.wait_load_page_feed_order()
            except Exception:
                # Если refresh или wait не удались, просто продолжаем цикл
                pass
            
            time.sleep(poll_frequency)
        allure.attach(
            "\n".join(last_seen),
            name="orders_in_work_snapshot",
            attachment_type=allure.attachment_type.TEXT,
        )
        return False

    @allure.step('Подождать появления заказа в списке готовых')
    def wait_for_order_id_ready(self, order_id, timeout=120, poll_frequency=5):
        normalized_target = str(int(order_id))
        end_time = time.time() + timeout
        last_seen = []

        while time.time() < end_time:
            try:
                ids_ready = self.get_id_orders_ready()
                last_seen = ids_ready
                normalized_ids = [
                    str(int(order.strip()))
                    for order in ids_ready
                    if order and order.strip().isdigit()
                ]
                if normalized_target in normalized_ids:
                    return True
            except Exception:
                pass

            try:
                self.refresh_page()
                self.wait_load_page_feed_order()
            except Exception:
                pass

            time.sleep(poll_frequency)

        allure.attach(
            "\n".join(last_seen),
            name="orders_ready_snapshot",
            attachment_type=allure.attachment_type.TEXT,
        )
        return False

    @allure.step('Получить статистику заказов по API')
    def get_feed_stats(self):
        response = requests.get(Urls.FEED_API_URL, timeout=15)
        response.raise_for_status()
        return response.json()

    @allure.step('Подождать увеличения статистики заказов по API')
    def wait_feed_stat_increase(self, stat_key, old_value, timeout=120, poll_frequency=5):
        end_time = time.time() + timeout
        last_value = old_value

        while time.time() < end_time:
            try:
                stats = self.get_feed_stats()
                last_value = stats.get(stat_key, old_value)
                if isinstance(last_value, str) and last_value.isdigit():
                    last_value = int(last_value)
                if last_value > old_value:
                    return last_value
            except Exception:
                pass
            time.sleep(poll_frequency)

        return last_value

    @allure.step('Подождать появления заказа в API ленты заказов')
    def wait_order_in_feed_api(self, order_id, timeout=120, poll_frequency=5):
        normalized_target = str(int(order_id))
        end_time = time.time() + timeout
        last_payload = {}

        while time.time() < end_time:
            try:
                stats = self.get_feed_stats()
                last_payload = stats
                orders = stats.get('orders', [])
                for order in orders:
                    number = order.get('number')
                    if number is not None and str(int(number)) == normalized_target:
                        return True
            except Exception:
                pass

            time.sleep(poll_frequency)

        allure.attach(
            str(last_payload),
            name='feed_api_snapshot',
            attachment_type=allure.attachment_type.JSON,
        )
        return False

    @allure.step('Подождать увеличения счетчика заказов')
    def wait_count_orders_increase(self, locator, old_value, timeout=60, poll_frequency=3):
        end_time = time.time() + timeout
        last_value = old_value

        while time.time() < end_time:
            try:
                last_value = self.get_count_orders(locator)
                if last_value > old_value:
                    return last_value
            except Exception:
                pass
            time.sleep(poll_frequency)
            self.refresh_page()
            self.wait_load_page_feed_order()

        return last_value

    @allure.step('Подождать загрузки страницы ленты заказов')
    def wait_load_page_feed_order(self):
        self.wait_for_element(MainPageLocator.TEXT_FEED_ORDER)

    @allure.step('Получить URL страницы')
    def get_url_page(self):
        return self.get_url()

    @allure.step('Подождать загрузки карточки заказа')
    def wait_load_order_card(self):
        for locator in (
            OrderFeedLocator.MODAL_CONTENT,
            OrderFeedLocator.MODAL_OVERLAY,
            OrderFeedLocator.ORDER_ID_AFTER_PURCHASE,
        ):
            try:
                return self.wait_for_element(locator, timeout=30)
            except Exception:
                continue
        raise TimeoutError("Modal order card did not appear")