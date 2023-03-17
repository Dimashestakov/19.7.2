import json

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """Библиотека API к веб-приложению PetFriends"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, passwd: str) -> json:
        """Этот метод отправляет запрос к серверу API, после чего возвращает статус запроса и результат
         в формате JSON, содержащий уникальный идентификатор пользователя,
        который был найден по указанным электронной почте и паролю"""

        headers = {
            'email': email,
            'password': passwd,
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """Данный метод осуществляет запрос к серверу API и возвращает статус
          запроса вместе с результатом, представленным в формате JSON.
          Результат содержит список найденных питомцев, соответствующих заданному фильтру.
          На данный момент, фильтр может принимать два значения:
          пустое значение, которое означает получение списка всех питомцев,
          или значение "my_pets", которое позволяет получить список собственных питомцев."""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        """Этот метод отправляет данные о добавляемом питомце на сервер, и, если у питомца есть фотография,
         то также отправляет ее.
         После этого метод возвращает статус запроса на сервер и результат в формате JSON,
         содержащий информацию о добавленном питомце."""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Данный метод отправляет запрос на сервер на удаление питомца с указанным ID. После выполнения запроса,
         метод возвращает статус запроса и результат в формате JSON с
         текстом уведомления об успешном удалении питомца.."""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """Этот метод отправляет запрос на сервер с целью обновления данных питомца с указанным ID.
         После выполнения запроса, метод возвращает статус запроса и результат
         в формате JSON с обновленными данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet_simple(self, auth_key: json, name: str, animal_type: str,
                           age: str) -> json:
        """Этот метод отправляет данные о добавляемом питомце на сервер, но без фотографии питомца.
         После этого метод возвращает статус запроса на сервер и результат в формате JSON,
         содержащий информацию о добавленном питомце."""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def add_pet_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Этот метод отправляет запрос на сервер с целью добавления фотографии питомца по указанному ID.
        После выполнения запроса, метод возвращает статус запроса и результат
        в формате JSON с обновленными данными питомца"""

        data = MultipartEncoder(
            fields={'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')})
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result