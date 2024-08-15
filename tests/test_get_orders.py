import allure
from methods import ApiMethods
from fake_data import FakerMethods
from fake_data import Ingredients
from test_data import TestData


class TestGetOrders:

    @allure.title('Получение списка заказов с авторизацией')
    @allure.description('Создается пользователь, создается заказ,'
                        ' затем получается список заказов,затем пользователь удаляется')
    def test_get_orders_success(self):
        with allure.step('Регистрация пользователя'):
            payload = FakerMethods.create_payload()
            response = ApiMethods.user_registration(payload)
        with allure.step('Проверка регистрации пользователя'):
            assert response.status_code == TestData.STATUS_CODE_200
            assert response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_TRUE
        with allure.step('Создание заказа'):
            access_token = response.json()[TestData.ACCESS_TOKEN_KEY]
            order_payload = Ingredients.burger
            response = ApiMethods.create_order(order_payload, access_token)
        with allure.step('Проверка создания заказа'):
            assert response.status_code == TestData.STATUS_CODE_200
            assert response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_TRUE
            assert TestData.ORDER_NUMBER_KEY in response.json()[TestData.ORDER_KEY] and response.json()[TestData.ORDER_KEY][TestData.ORDER_NUMBER_KEY] != ''
            assert TestData.ORDER_INGREDIENTS_KEY in response.json()[TestData.ORDER_KEY] and response.json()[TestData.ORDER_KEY][TestData.ORDER_INGREDIENTS_KEY] != []
        with allure.step('Получение списка заказов'):
            response = ApiMethods.get_user_order(access_token)
            assert response.status_code == TestData.STATUS_CODE_200
            assert TestData.ORDER_INGREDIENTS_KEY in response.json()[TestData.ORDERS_KEY][0] and response.json()[TestData.ORDERS_KEY][0][TestData.ORDER_INGREDIENTS_KEY] != []
        with allure.step('Удаление пользователя'):
            response = ApiMethods.user_delete(access_token)
        with allure.step('Проверка удаления пользователя'):
            assert response.status_code == TestData.STATUS_CODE_202

    @allure.title('Получение списка заказов без авторизации')
    @allure.description('Создается заказ, без создания пользователя')
    def test_get_user_order_without_auth(self):
        with allure.step('Создание заказа'):
            order_payload = Ingredients.burger
            response = ApiMethods.create_order(order_payload)
        with allure.step('Проверка создания заказа'):
            assert response.status_code == TestData.STATUS_CODE_200
            assert response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_TRUE
            assert TestData.ORDER_NUMBER_KEY in response.json()[TestData.ORDER_KEY] and response.json()[TestData.ORDER_KEY][TestData.ORDER_NUMBER_KEY] != ''
        with allure.step('Получение списка заказов'):
            response = ApiMethods.get_user_order()
            assert response.status_code == TestData.STATUS_CODE_401
            assert response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_FALSE
