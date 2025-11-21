from selenium.webdriver.common.by import By

class OrderFeedLocator:
    MODAL_OVERLAY = (By.XPATH, '//*[contains(@class, "Modal_modal_overlay")]')
    MODAL_CONTENT = (By.XPATH, '//*[contains(@class, "Modal_modal")]')
    ORDER_CARD = MODAL_CONTENT
    ORDER_ID_IN_HISTORY = (By.XPATH, '//p[contains(@class, "text_type_digits-default")]')
    BUT_CLOSE_ORDER = (By.XPATH, '//*[contains(@class, "Modal_modal__close")]')
    COUNT_ORDERS_ALL_TIME = (By.XPATH, '//p[contains(text(), "Выполнено за все время")]/following-sibling::p[contains(@class, "OrderFeed_number")]')
    COUNT_ORDERS_TODAY = (By.XPATH, '//p[contains(text(), "Выполнено за сегодня")]/following-sibling::p[contains(@class, "OrderFeed_number")]')
    ORDER_ID_AFTER_PURCHASE = (By.XPATH, '//*[contains(@class, "Modal_modal__title")]')
    ORDER_READY_ITEMS = (
        By.XPATH,
        '//h3[contains(text(), "Готовы")]/following-sibling::ul[1]//li[contains(@class, "text_type_digits-default")]',
    )
    ORDER_IN_WORK = (
        By.XPATH,
        '//h3[contains(text(), "В работе")]/following-sibling::ul[1]',
    )
    ORDER_IN_WORK_1 = (
        By.XPATH,
        '//h3[contains(text(), "В работе")]/following-sibling::ul[1]//li[contains(@class, "text_type_digits-default")]',
    )
    
    ALL_TIME_ORDER_COUNT = COUNT_ORDERS_ALL_TIME
    TODAY_ORDER_COUNT = COUNT_ORDERS_TODAY

    @staticmethod
    def order_history_locator(number):
        return By.XPATH, f'//li[contains(@class, "OrderHistory_listItem")][{number}]//a[contains(@class, "OrderHistory_link")]'