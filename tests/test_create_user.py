import allure
import pytest
from methods import ApiMethods
from fake_data import FakerMethods


class TestCreateUser:

    @allure.title('Создание уникального пользователя')
    @allure.description('Создаем пользователя с уникальным email и паролем')
    def test_create_user(self):
        with allure.step('Регистрация пользователя'):
            payload = FakerMethods.create_payload()
            response = ApiMethods.user_registration(payload)
        with allure.step('Проверка регистрации пользователя'):
            assert response.status_code == 200
            assert response.json()['success'] is True
        with allure.step('Проверка корректности данных'):
            assert response.json()['user']['email'] == payload['email']
            assert response.json()['user']['name'] == payload['name']
        with allure.step('Удаление пользователя'):
            delete_response = ApiMethods.user_delete(response.json()['accessToken'])
            assert delete_response.status_code == 202

    @allure.title('Создание пользователя, который уже зарегистрирован')
    @allure.description('Создаем пользователя с уникальным '
                        'email и паролем,затем еще раз регистрируемся с этими данными')
    def test_create_user_duplicate(self, ):
        with allure.step('Регистрация пользователя'):
            payload = FakerMethods.create_payload()
            response = ApiMethods.user_registration(payload)
        with allure.step('Проверка регистрации пользователя'):
            assert response.status_code == 200
            assert response.json()['success'] is True
        with allure.step('Повторная регистрация пользователя'):
            duplicate_response = ApiMethods.user_registration(payload)
            assert duplicate_response.status_code == 403
            assert duplicate_response.json()['message'] == 'User already exists'
        with allure.step('Удаление пользователя'):
            delete_response = ApiMethods.user_delete(response.json()['accessToken'])
            assert delete_response.status_code == 202

    @allure.title('Создание пользователя с незаполненным полем')
    @allure.description('Создаем пользователя с незаполненным полем,'
                        ' с помощью параметризации создаем три теста и '
                        'в каждом передаем пустое поле:name, email, password')
    @pytest.mark.parametrize('empty_values', ['name', 'email', 'password'])
    def test_create_user_with_empty_field(self, empty_values):
        with allure.step('Регистрация пользователя'):
            payload = FakerMethods.create_payload_with_empty_field(empty_values)
            response = ApiMethods.user_registration(payload)
        with allure.step('Проверка того,что при пустом поле возвращается ошибка'):
            assert response.status_code == 403
            assert response.json()['success'] is False
            assert response.json()['message'] == 'Email, password and name are required fields'

