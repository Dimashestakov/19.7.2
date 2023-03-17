from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Мы проверяем, что при запросе API-ключа статус ответа сервера равен 200, и что 
    в результате присутствует ключевое слово "key"""

    # Посылаем запрос и сохраняем полученный ответ в переменную status,
    # а текст ответа - в переменную result
    status, result = pf.get_api_key(email, password)

    # Проверка данных
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Мы проверяем, что запрос всех питомцев вернул список, который не пустой.
     Для этого мы сначала получаем ключ API и сохраняем его в переменную auth_key.
     Затем мы используем этот ключ, чтобы запросить список всех питомцев и проверяем,
      что список содержит хотя бы одного питомца. Мы можем использовать параметр filter со значением
       "my_pets" или пустую строку. """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_successful_delete_self_pet():
    """Проверка возможности удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Мы проверяем наличие питомцев в нашем списке. Если этот список пуст,
    # то мы добавляем нового питомца и снова запрашиваем список всех наших питомцев.
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Кот", "тигр", "10", "images/tigr.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Извлекаем id 1-го питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Повторно запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем статус  200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Жора', animal_type='зверь', age=50):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список непустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем, что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_new_pet_simple_with_valid_data(name='Волчара', animal_type='волк', age='100'):
    """Проверяем, что можно добавить питомца без фотографии с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_pet_photo_with_valid_data(pet_photo='images/tigr.jpg'):
    """Мы проверяем, можно ли добавить фотографию нашего питомца."""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список непустой, то пробуем добавить фотографию
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем, что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_get_api_key_for_invalid_email(email=invalid_email, password=invalid_password):
    """Проверяем, что запрос api-ключа с неверным email возвращает код 403"""
    status, result = pf.get_api_key(email, password)
    assert status == 403  # Сверяем полученный ответ с ожидаемым результатом
    assert 'This user wasn&#x27;t found in database' in result


def test_get_api_key_for_valid_email_and_invalid_password(email=valid_email, password=invalid_password):
    """Проверяем, что запрос api-ключа с верным email и неверным password возвращает код 403"""
    status, result = pf.get_api_key(email, password)
    assert status == 403  # Сверяем полученный ответ с ожидаемым результатом
    assert 'This user wasn&#x27;t found in database' in result


def test_get_all_pets_with_invalid_key(filter=''):
    """Проверяем, что запрос всех питомцев с неверным api-ключом возвращает код 403"""
    auth_key = {'key': '000'}  # Задаем неверный ключ api и сохраняем в переменную auth_key
    status, result = pf.get_list_of_pets(auth_key, filter)  # Запрашиваем список питомцев
    assert status == 403  # Сверяем полученный ответ с ожидаемым результатом
    assert 'Please provide &#x27;auth_key&#x27; Header' in result


def test_add_new_pet_simple_with_invalid_key(name='Котик', animal_type='пернатый', age='99'):
    """Проверяем, что запрос на добавление питомца без фотографии с неверным api-ключом возвращает код 403"""
    auth_key = {'key': '00000'}  # Задаем неверный ключ api и сохраняем в переменную auth_key
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)  # Создаем питомца
    assert status == 403  # Сверяем полученный ответ с ожидаемым результатом
    assert 'Please provide &#x27;auth_key&#x27; Header' in result





