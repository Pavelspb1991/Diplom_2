import allure
from methods import ApiMethods
from fake_data import FakerMethods
from fake_data import Ingredients


class TestGetOrders:

    @allure.title('Получение списка заказов с авторизацией')
    @allure.description('Создается пользователь, создается заказ,'
                        ' затем получается список заказов,затем пользователь удаляется')
    def test_get_orders_success(self):
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
        with allure.step('Получение списка заказов'):
            response = ApiMethods.get_user_order(access_token)
            assert response.status_code == 200
            assert 'ingredients' in response.json()['orders'][0] and 'Ingredients' != []
        with allure.step('Удаление пользователя'):
            response = ApiMethods.user_delete(access_token)
        with allure.step('Проверка удаления пользователя'):
            assert response.status_code == 202

    @allure.title('Получение списка заказов без авторизации')
    @allure.description('Создается заказ, без создания пользователя')
    def test_get_user_order_without_auth(self):
        with allure.step('Создание заказа'):
            order_payload = Ingredients.burger
            response = ApiMethods.create_order(order_payload)
        with allure.step('Проверка создания заказа'):
            assert response.status_code == 200
            assert response.json()['success'] is True
            assert 'number' in response.json()['order'] and 'number' != ''
        with allure.step('Получение списка заказов'):
            response = ApiMethods.get_user_order()
            assert response.status_code == 401
            assert response.json()['success'] is False
