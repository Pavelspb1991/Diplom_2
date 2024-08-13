import allure
from methods import ApiMethods
from fake_data import FakerMethods
from fake_data import Ingredients


class TestCreateOrder:

    @allure.title('Создание заказа с авторизацией')
    @allure.description('Создание заказа с авторизацией и указанием ингредиентов')
    def test_create_order_success(self):
        with allure.step('Регистрация пользователя'):
            payload = FakerMethods.create_payload()
            response = ApiMethods.user_registration(payload)
        with allure.step('Проверка регистрации пользователя'):
            assert response.status_code == 200
            assert response.json()['success'] is True
        with allure.step('Создание заказа'):
            access_token = response.json()['accessToken']
            order_payload = Ingredients.burger
            response = ApiMethods.create_order(order_payload, access_token)
        with allure.step('Проверка создания заказа'):
            assert response.status_code == 200
            assert response.json()['success'] is True
            assert 'number' in response.json()['order'] and 'number' != ''
            assert 'ingredients' in response.json()['order'] and 'Ingredients' != []
        with allure.step('Удаление пользователя'):
            delete_response = ApiMethods.user_delete(access_token)
            assert delete_response.status_code == 202

    @allure.title('Создание заказа без авторизации')
    @allure.description('Создание заказа без авторизации,c указанием ингредиентов')
    def test_create_order_without_auth(self):
        with allure.step('Создание заказа'):
            order_payload = Ingredients.burger
            response = ApiMethods.create_order(order_payload)
        with allure.step('Проверка создания заказа'):
            assert response.status_code == 200
            assert response.json()['success'] is True

    @allure.title('Создание заказа с авторизацией без ингредиентов')
    @allure.description('Создаем пользователя и'
                        ' создаем заказ с авторизацией без указания ингредиентов')
    def test_create_order_without_ingredients(self):
        with allure.step('Регистрация пользователя'):
            payload = FakerMethods.create_payload()
            response = ApiMethods.user_registration(payload)
        with allure.step('Проверка регистрации пользователя'):
            assert response.status_code == 200
            assert response.json()['success'] is True
        with allure.step('Создание заказа'):
            access_token = response.json()['accessToken']
            order_payload = []
            response = ApiMethods.create_order(order_payload, access_token)
        with allure.step('Проверка создания заказа'):
            assert response.status_code == 400
            assert response.json()['success'] is False
            assert response.json()['message'] == 'Ingredient ids must be provided'
        with allure.step('Удаление пользователя'):
            delete_response = ApiMethods.user_delete(access_token)
            assert delete_response.status_code == 202

    @allure.title('Создание заказа без авторизации и без ингредиентов')
    @allure.description('Создание заказа без авторизации и без ингредиентов')
    def test_create_order_without_auth_and_without_ingredients(self):
        with allure.step('Создание заказа'):
            order_payload = []
            response = ApiMethods.create_order(order_payload)
        with allure.step('Проверка создания заказа'):
            assert response.status_code == 400
            assert response.json()['success'] is False
            assert response.json()['message'] == 'Ingredient ids must be provided'

    @allure.title("Создание заказа с авторизацией и неверных хешем ингредиентов")
    @allure.description('Создаем пользователя и'
                        ' создаем заказ с авторизацией и указанием неверных хешей ингредиентов')
    def test_create_order_with_wrong_ingredients(self):
        with allure.step('Регистрация пользователя'):
            payload = FakerMethods.create_payload()
            response = ApiMethods.user_registration(payload)
        with allure.step('Проверка регистрации пользователя'):
            assert response.status_code == 200
            assert response.json()['success'] is True
        with allure.step('Создание заказа'):
            access_token = response.json()['accessToken']
            order_payload = Ingredients.wrong_burger
            response = ApiMethods.create_order(order_payload, access_token)
        with allure.step('Проверка создания заказа'):
            assert response.status_code == 500
            assert 'Internal Server Error' in response.text
        with allure.step('Удаление пользователя'):
            delete_response = ApiMethods.user_delete(access_token)
            assert delete_response.status_code == 202

