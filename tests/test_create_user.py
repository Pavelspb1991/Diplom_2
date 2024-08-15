import allure
import pytest
from methods import ApiMethods
from fake_data import FakerMethods
from test_data import TestData


class TestCreateUser:

    @allure.title('Создание уникального пользователя')
    @allure.description('Создаем пользователя с уникальным email и паролем')
    def test_create_user(self):
        with allure.step('Регистрация пользователя'):
            payload = FakerMethods.create_payload()
            response = ApiMethods.user_registration(payload)
        with allure.step('Проверка регистрации пользователя'):
            assert response.status_code == TestData.STATUS_CODE_200
            assert response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_TRUE
        with allure.step('Проверка корректности данных'):
            assert response.json()[TestData.USER_KEY][TestData.EMAIL_KEY] == payload[TestData.EMAIL_KEY]
            assert response.json()[TestData.USER_KEY][TestData.NAME_KEY] == payload[TestData.NAME_KEY]
        with allure.step('Удаление пользователя'):
            delete_response = ApiMethods.user_delete(response.json()[TestData.ACCESS_TOKEN_KEY])
            assert delete_response.status_code == TestData.STATUS_CODE_202

    @allure.title('Создание пользователя, который уже зарегистрирован')
    @allure.description(
        'Создаем пользователя с уникальным email и паролем, затем еще раз регистрируемся с этими данными')
    def test_create_user_duplicate(self):
        with allure.step('Регистрация пользователя'):
            payload = FakerMethods.create_payload()
            response = ApiMethods.user_registration(payload)
        with allure.step('Проверка регистрации пользователя'):
            assert response.status_code == TestData.STATUS_CODE_200
            assert response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_TRUE
        with allure.step('Повторная регистрация пользователя'):
            duplicate_response = ApiMethods.user_registration(payload)
            assert duplicate_response.status_code == TestData.STATUS_CODE_403
            assert duplicate_response.json()[TestData.MESSAGE_KEY] == TestData.USER_ALREADY_EXISTS
        with allure.step('Удаление пользователя'):
            delete_response = ApiMethods.user_delete(response.json()[TestData.ACCESS_TOKEN_KEY])
            assert delete_response.status_code == TestData.STATUS_CODE_202

    @allure.title('Создание пользователя с незаполненным полем')
    @allure.description(
        'Создаем пользователя с незаполненным полем, с помощью параметризации создаем три теста и в каждом передаем пустое поле: name, email, password')
    @pytest.mark.parametrize('empty_values', [TestData.NAME_KEY, TestData.EMAIL_KEY, 'password'])
    def test_create_user_with_empty_field(self, empty_values):
        with allure.step('Регистрация пользователя'):
            payload = FakerMethods.create_payload_with_empty_field(empty_values)
            response = ApiMethods.user_registration(payload)
        with allure.step('Проверка того, что при пустом поле возвращается ошибка'):
            assert response.status_code == TestData.STATUS_CODE_403
            assert response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_FALSE
            assert response.json()[TestData.MESSAGE_KEY] == TestData.REQUIRED_FIELDS_MESSAGE
