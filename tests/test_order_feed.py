import allure
import pytest
import re
from locators.order_feed_page_locator import OrderFeedLocator
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage

class TestOrderFeed:
    
    # ... другие тесты ...

    @allure.title('Тест появления номера заказа в разделе "В работе" после оформления заказа')
    def test_display_order_(self, login_driver):
        order_feed_page = OrderFeedPage(login_driver)
        order_feed_page.going_in_order_history()
        try:
            previous_order_text = order_feed_page.get_id_last_order()
        except Exception:
            previous_order_text = ""

        main_page = MainPage(login_driver)
        main_page.going_main_page()
        main_page.add_ingredient_in_burger()
        main_page.click_but_create_order()
        main_page.wait_load_order_card()

        order_feed_page.going_in_order_history()
        new_order_text = order_feed_page.wait_new_order_in_history(previous_order_text)

        order_id_match = re.search(r'\d+', new_order_text)
        if not order_id_match:
            pytest.fail(f"Не удалось извлечь номер заказа из истории: {new_order_text}")

        order_id = order_id_match.group()
        order_feed_page.going_in_feed_order()

        in_work = order_feed_page.wait_for_order_id_in_work(order_id)
        if not in_work:
            ready = order_feed_page.wait_for_order_id_ready(order_id)
            if not ready:
                api_found = order_feed_page.wait_order_in_feed_api(order_id)
                assert api_found, (
                    f"Заказ {order_id} не найден ни в разделе 'В работе', "
                    f"ни в разделе 'Готовы', ни в API ленты"
                )

    @pytest.mark.parametrize(
        'locator, stat_key, name_test',
        [
            (
                OrderFeedLocator.ALL_TIME_ORDER_COUNT,
                'total',
                'Тест увеличения счетчика "Выполнено за всё время"',
            ),
            (
                OrderFeedLocator.TODAY_ORDER_COUNT,
                'totalToday',
                'Тест увеличения счетчика "Выполнено за сегодня"',
            ),
        ],
    )
    def test_count_orders_in_feed_order_page(self, login_driver, locator, stat_key, name_test):
        allure.dynamic.title(name_test)
        order_feed_page = OrderFeedPage(login_driver)
        order_feed_page.going_in_feed_order()
        old_value = order_feed_page.get_count_orders(locator)
        
        main_page = MainPage(login_driver)
        main_page.going_main_page()
        main_page.add_ingredient_in_burger()
        main_page.click_but_create_order()
        main_page.wait_load_order_card()
        
        order_feed_page.going_in_feed_order()
        new_value = order_feed_page.wait_count_orders_increase(locator, old_value)

        if new_value <= old_value:
            api_value = order_feed_page.wait_feed_stat_increase(stat_key, old_value)
            assert api_value > old_value, (
                f"Счетчик по API не увеличился: было {old_value}, стало {api_value}"
            )
            order_feed_page.going_in_feed_order()
            ui_value = order_feed_page.get_count_orders(locator)
            assert ui_value == api_value, (
                f"Значение на UI ({ui_value}) не совпадает с API ({api_value}) "
                f"для {name_test}"
            )
        else:
            assert new_value > old_value, f"Счетчик не увеличился: было {old_value}, стало {new_value}"