import allure
from methods import ApiMethods
from fake_data import FakerMethods
from test_data import TestData


class TestUpdateUser:

    @allure.title('Проверка редактирования пользователя')
    def test_update_user_with_auth_success(self):
        with allure.step('Регистрация пользователя'):
            payload = FakerMethods.create_payload()
            response = ApiMethods.user_registration(payload)
        with allure.step('Проверка регистрации пользователя'):
            assert response.status_code == TestData.STATUS_CODE_200
            assert response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_TRUE
        with allure.step('Редактирование пользователя'):
            access_token = response.json()[TestData.ACCESS_TOKEN_KEY]
            updated_user_data = FakerMethods.create_updated_user_data()
            update_response = ApiMethods.user_update(updated_user_data, access_token)
        with allure.step('Проверка редактирования пользователя'):
            assert update_response.status_code == TestData.STATUS_CODE_200
            assert update_response.json()[TestData.USER_KEY][TestData.EMAIL_KEY] == updated_user_data[TestData.EMAIL_KEY]
            assert update_response.json()[TestData.USER_KEY][TestData.NAME_KEY] == updated_user_data[TestData.NAME_KEY]
        with allure.step('Удаление пользователя'):
            delete_response = ApiMethods.user_delete(access_token)
            assert delete_response.status_code == TestData.STATUS_CODE_202

    @allure.title('Проверка ответа на запрос изменения данных неаутентифицированного пользователя')
    def test_update_user_unauthenticated_expected_error(self):
        updated_user_data = FakerMethods.create_updated_user_data()
        with allure.step('Попытка обновления данных пользователя без авторизации'):
            response = ApiMethods.user_update_without_auth(updated_user_data)
        with allure.step('Проверка ошибки'):
            assert response.status_code == TestData.STATUS_CODE_401
            assert response.json()[TestData.SUCCESS_KEY] is TestData.SUCCESS_FALSE
            assert response.json()[TestData.MESSAGE_KEY] == TestData.UNAUTHORIZED_MESSAGE
