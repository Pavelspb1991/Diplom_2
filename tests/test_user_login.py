import allure
from methods import ApiMethods
from fake_data import FakerMethods
from test_data import TestData


class TestUserLogin:
    @allure.title('Проверка успешной авторизации')
    @allure.description('Проверка успешной авторизации '
                        'зарегистрированного пользователя с корректными данными')
    def test_user_login_success(self):
        with allure.step('Регистрация пользователя'):
            payload = FakerMethods.create_payload()
            response = ApiMethods.user_registration(payload)
        with allure.step('Проверка регистрации пользователя'):
            assert response.status_code == TestData.STATUS_CODE_200
            assert response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_TRUE
        with allure.step('Авторизация пользователя'):
            response = ApiMethods.user_login(payload)
        with allure.step('Проверка авторизации пользователя'):
            assert response.status_code == TestData.STATUS_CODE_200
            assert response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_TRUE
            assert TestData.ACCESS_TOKEN_KEY in response.json() and TestData.ACCESS_TOKEN_KEY != ''
            assert 'refreshToken' in response.json() and 'refreshToken' != ''
        with allure.step('Удаление пользователя'):
            response = ApiMethods.user_delete(response.json()[TestData.ACCESS_TOKEN_KEY])
        with allure.step('Проверка удаления пользователя'):
            assert response.status_code == TestData.STATUS_CODE_202

    @allure.title('Проверка авторизации с незарегистрированным логином(email)')
    @allure.description('Проверка авторизации с незарегистрированным(неверным) логином(email) ')
    def test_user_login_fail(self):
        with allure.step('Авторизация пользователя без регистрации'):
            payload = FakerMethods.create_payload()
            response = ApiMethods.user_login(payload)
        with allure.step('Проверка ошибки при авторизации пользователя'):
            assert response.status_code == TestData.STATUS_CODE_401
            assert response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_FALSE

    @allure.title('Проверка авторизации с неправильным паролем')
    @allure.description('Проверка авторизации с неправильным паролем')
    def test_user_login_fail_password(self):
        with allure.step('Регистрация пользователя'):
            payload = FakerMethods.create_payload()
            registration_response = ApiMethods.user_registration(payload)
        with allure.step('Проверка регистрации пользователя'):
            assert registration_response.status_code == TestData.STATUS_CODE_200
            assert registration_response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_TRUE
            access_token = registration_response.json()[TestData.ACCESS_TOKEN_KEY]
        with allure.step('Авторизация пользователя с неправильным паролем'):
            payload_failed = payload.copy()
            payload_failed['password'] = '123456789'
            login_response = ApiMethods.user_login(payload_failed)
        with allure.step('Проверка авторизации пользователя'):
            assert login_response.status_code == TestData.STATUS_CODE_401
            assert login_response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_FALSE
        with allure.step('Удаление пользователя'):
            delete_response = ApiMethods.user_delete(access_token)
        with allure.step('Проверка удаления пользователя'):
            assert delete_response.status_code == TestData.STATUS_CODE_202
            assert delete_response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_TRUE