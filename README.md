# VK autoread

Автоматически помечает беседы прочитанными, чтобы не маячил гребанный кружочек с циферкой.

## Конфиг

Файл с конфигом должен быть в рабочей папке под названием `config.yml`.

Пример конфига есть в файле `config.yml.template`.

Описание конфига:
```
vk_token: str                     # access-токен вк
autoread_all_muted: bool          # автоматически отмечать прочитанными все чаты
always_autoread_chats: List[str]  # список названий бесед, которые всегда нужно отмечать прочитанными
deny_autoread_chats: List[str]    # список названий бесед, которые никогда не нужно отмечать прочитанными
```

## Access-токен ВК

Как получить токен:

1. Создать приложение на https://vk.com/apps?act=manage
2. Заменить в такой ссылке номер приложения:
    ```
    https://oauth.vk.com/authorize?client_id=<НОМЕР ПРИЛОЖЕНИЯ>&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=offline,messages&response_type=token&v=5.85
    ```
3. Перейти по ссылке, разрешить права. Потом скопировать из адресной строки access_token.

## Запуск

```sh
pip3 install -r requirement.txt  # чтобы установить зависимости

python3 ./app.py
```

