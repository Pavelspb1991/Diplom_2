import allure
from methods import ApiMethods
from fake_data import FakerMethods


class TestUserLogin:
    @allure.title('Проверка успешной авторизации')
    @allure.description('Проверка успешной авторизации '
                        'зарегистрированного пользователя с корректными данными')
    def test_user_login_success(self):
        with allure.step('Регистрация пользователя'):
            payload = FakerMethods.create_payload()
            response = ApiMethods.user_registration(payload)
        with allure.step('Проверка регистрации пользователя'):
            assert response.status_code == 200
            assert response.json()['success'] is True
        with allure.step('Авторизация пользователя'):
            response = ApiMethods.user_login(payload)
        with allure.step('Проверка авторизации пользователя'):
            assert response.status_code == 200
            assert response.json()['success'] is True
            assert 'accessToken' and 'refreshToken' in response.json()
        with allure.step('Удаление пользователя'):
            response = ApiMethods.user_delete(response.json()['accessToken'])
        with allure.step('Проверка удаления пользователя'):
            assert response.status_code == 202

    @allure.title('Проверка авторизации с незарегистрированным логином(email)')
    @allure.description('Проверка авторизации с незарегистрированным(неверным) логином(email) ')
    def test_user_login_fail(self):
        with allure.step('Авторизация пользователя без регистрации'):
            payload = FakerMethods.create_payload()
            response = ApiMethods.user_login(payload)
        with allure.step('Проверка ошибки при авторизации пользователя'):
            assert response.status_code == 401
            assert response.json()['success'] is False

    @allure.title('Проверка авторизации с неправильным паролем')
    @allure.description('Проверка авторизации с неправильным паролем')
    def test_user_login_fail_password(self):
        with allure.step('Регистрация пользователя'):
            payload = FakerMethods.create_payload()
            registration_response = ApiMethods.user_registration(payload)
        with allure.step('Проверка регистрации пользователя'):
            assert registration_response.status_code == 200
            assert registration_response.json()['success'] is True
            access_token = registration_response.json()['accessToken']
        with allure.step('Авторизация пользователя с неправильным паролем'):
            payload_failed = payload.copy()
            payload_failed['password'] = '123456789'
            login_response = ApiMethods.user_login(payload_failed)
        with allure.step('Проверка авторизации пользователя'):
            assert login_response.status_code == 401
            assert login_response.json()['success'] is False
        with allure.step('Удаление пользователя'):
            delete_response = ApiMethods.user_delete(access_token)
        with allure.step('Проверка удаления пользователя'):
            assert delete_response.status_code == 202
            assert delete_response.json()['success'] is True
