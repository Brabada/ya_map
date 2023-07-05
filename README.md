# Карта с достопримечательностями

Данный сайт отображает карту и позволяет добавлять на неё точки с достопримечательностями.

Достопримечательности можно добавлять/удалять/редактировать в админке по адресу "http://ip-вашего-сайта/admin".

Код написан на Python 3.11 на Django 4.2 фреймворке. В качестве БД использован sqlite3.

Потыкать, посмотреть: http://brabada1.pythonanywhere.com/

## Библиотеки

1. `Django 4.2` - основной фреймворк разработки.
2. `Pillow 9.5` - работа с изображениями на фронте.
3. `django-admin-sortable2 2.1` - drag'n'drop порядка фотокарточек в админке Django.
4. `django-tinymce 3.6` - поддержка редактора текста TinyMCE для полей описания достопримечательности.
5. `environs 9.5` - для работы с файлом `.env` для считывания переменных окружения.

## Переменные среды

Для запуска сайта в prod режиме нужно создать файл `.env` и прописать параметры следующих полей:
- `export DEBUG=<bool>` - запуск сайта в режиме Debug. При запуске с _True_, все остальные параметры не будут действительны.
- `export SECRET_KEY=<string>` - секретный токен для запуска сайта, который нужно создать самому.
- `export ALLOWED_HOSTS=<list>`- ip с которых разрешено открывать сайт. Пример: _127.0.0.1, localhost_.
- `export SECURE_SSL_REDIRECT=<bool>` - поддержка безопасного SSL редиректа.
- `export SESSION_COOKIE_SECURE=<bool>` - поддержка защиты от сниффинга куков сессии. 
- `export CSRF_COOKIE_SECURE=<bool>` - поддержка маркировки куков, как безопасные, что гарантирует их отправку через HTTPS соединение браузером.
- `export DB_SECRET=<string>` - пароль для БД.

## Быстрый запуск

1. Установить пакеты. Django 4.2 поддерживает Python версии 3.8-3.11, но желательно устанавливать под 3.11.
```bash
$ pip install -r requirements.txt
```
2. Создать файл `.env` в корне проекта и задать в нём нужные вам параметры. Для запуска в режиме отладки не выставлять настройки.

3. Инициализировать проект
```bash
$ python manage.py migrate
```
4. Запустить сайт. (Указан пример для запуска в режиме отладки)
```bash
$ python manage.py runserver
```