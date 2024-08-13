import allure
from methods import ApiMethods
from fake_data import FakerMethods


class TestUpdateUser:

    @allure.title('Проверка редактирования пользователя')
    def test_update_user_with_auth_success(self):
        with allure.step('Регистрация пользователя'):
            payload = FakerMethods.create_payload()
            response = ApiMethods.user_registration(payload)
        with allure.step('Проверка регистрации пользователя'):
            assert response.status_code == 200
            assert response.json()['success'] is True
        with allure.step('Редактирование пользователя'):
            access_token = response.json()['accessToken']
            updated_user_data = FakerMethods.create_updated_user_data()
            update_response = ApiMethods.user_update(updated_user_data, access_token)
        with allure.step('Проверка редактирования пользователя'):
            assert update_response.status_code == 200
            assert update_response.json()['user']['email'] == updated_user_data['email']
            assert update_response.json()['user']['name'] == updated_user_data['name']
        with allure.step('Удаление пользователя'):
            delete_response = ApiMethods.user_delete(access_token)
            assert delete_response.status_code == 202

    @allure.title('Проверка ответа на запрос изменения данных неаутентифицированного пользователя')
    def test_update_user_unauthenticated_expected_error(self):
        updated_user_data = FakerMethods.create_updated_user_data()
        with allure.step('Попытка обновления данных пользователя без авторизации'):
            response = ApiMethods.user_update_without_auth(updated_user_data)
        with allure.step('Проверка ошибки'):
            assert response.status_code == 401
            assert response.json() == {'success': False, 'message': 'You should be authorised'}
