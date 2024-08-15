import allure
from methods import ApiMethods
from fake_data import FakerMethods
from fake_data import Ingredients
from test_data import TestData


class TestCreateOrder:

    @allure.title('Создание заказа с авторизацией')
    @allure.description('Создание заказа с авторизацией и указанием ингредиентов')
    def test_create_order_success(self):
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
        with allure.step('Удаление пользователя'):
            delete_response = ApiMethods.user_delete(access_token)
            assert delete_response.status_code == TestData.STATUS_CODE_202

    @allure.title('Создание заказа без авторизации')
    @allure.description('Создание заказа без авторизации, c указанием ингредиентов')
    def test_create_order_without_auth(self):
        with allure.step('Создание заказа'):
            order_payload = Ingredients.burger
            response = ApiMethods.create_order(order_payload)
        with allure.step('Проверка создания заказа'):
            assert response.status_code == TestData.STATUS_CODE_200
            assert response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_TRUE

    @allure.title('Создание заказа с авторизацией без ингредиентов')
    @allure.description('Создаем пользователя и создаем заказ с авторизацией без указания ингредиентов')
    def test_create_order_without_ingredients(self):
        with allure.step('Регистрация пользователя'):
            payload = FakerMethods.create_payload()
            response = ApiMethods.user_registration(payload)
        with allure.step('Проверка регистрации пользователя'):
            assert response.status_code == TestData.STATUS_CODE_200
            assert response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_TRUE
        with allure.step('Создание заказа'):
            access_token = response.json()[TestData.ACCESS_TOKEN_KEY]
            order_payload = []
            response = ApiMethods.create_order(order_payload, access_token)
        with allure.step('Проверка создания заказа'):
            assert response.status_code == TestData.STATUS_CODE_400
            assert response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_FALSE
            assert response.json()[TestData.MESSAGE_KEY] == TestData.INGREDIENT_IDS_MUST_BE_PROVIDED
        with allure.step('Удаление пользователя'):
            delete_response = ApiMethods.user_delete(access_token)
            assert delete_response.status_code == TestData.STATUS_CODE_202

    @allure.title('Создание заказа без авторизации и без ингредиентов')
    @allure.description('Создание заказа без авторизации и без ингредиентов')
    def test_create_order_without_auth_and_without_ingredients(self):
        with allure.step('Создание заказа'):
            order_payload = []
            response = ApiMethods.create_order(order_payload)
        with allure.step('Проверка создания заказа'):
            assert response.status_code == TestData.STATUS_CODE_400
            assert response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_FALSE
            assert response.json()[TestData.MESSAGE_KEY] == TestData.INGREDIENT_IDS_MUST_BE_PROVIDED

    @allure.title("Создание заказа с авторизацией и неверным хешем ингредиентов")
    @allure.description('Создаем пользователя и создаем заказ с авторизацией и указанием неверных хешей ингредиентов')
    def test_create_order_with_wrong_ingredients(self):
        with allure.step('Регистрация пользователя'):
            payload = FakerMethods.create_payload()
            response = ApiMethods.user_registration(payload)
        with allure.step('Проверка регистрации пользователя'):
            assert response.status_code == TestData.STATUS_CODE_200
            assert response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_TRUE
        with allure.step('Создание заказа'):
            access_token = response.json()[TestData.ACCESS_TOKEN_KEY]
            order_payload = Ingredients.wrong_burger
            response = ApiMethods.create_order(order_payload, access_token)
        with allure.step('Проверка создания заказа'):
            assert response.status_code == TestData.STATUS_CODE_500
            assert TestData.INTERNAL_SERVER_ERROR in response.text
        with allure.step('Удаление пользователя'):
            delete_response = ApiMethods.user_delete(access_token)
            assert delete_response.status_code == TestData.STATUS_CODE_202

