from faker import Faker


class FakerMethods:
    @staticmethod
    def create_payload():
        payload = {
            "email": fake.free_email(),
            "password": fake.password(length=6, digits=False, lower_case=True, upper_case=True, special_chars=False),
            "name": fake.first_name(),
        }
        return payload

    @staticmethod
    def create_payload_with_empty_field(field_to_empty):
        payload = FakerMethods.create_payload()
        payload[field_to_empty] = ''
        return payload

    @staticmethod
    def create_email():
        return fake.free_email()

    @staticmethod
    def create_name():
        return fake.first_name()

    @staticmethod
    def create_password():
        return fake.password(length=6, digits=False, lower_case=True, upper_case=True, special_chars=False)

    @staticmethod
    def create_updated_user_data():
        return {
            'email': FakerMethods.create_email(),
            'name': FakerMethods.create_name()
        }

    @staticmethod
    def create_updated_user_data_with_password():
        updated_user_data = {
            'email': FakerMethods.create_email(),
            'name': FakerMethods.create_name(),
            'password': FakerMethods.create_password()  # Добавьте поле password
        }
        return updated_user_data


fake = Faker("ru_RU")


class Ingredients:
    burger = ['61c0c5a71d1f82001bdaaa72', '61c0c5a71d1f82001bdaaa6f', '61c0c5a71d1f82001bdaaa72']
    wrong_burger = ['61c0c5a71d1f088005553535123', '61c0c5a71d1f088005553535124']



