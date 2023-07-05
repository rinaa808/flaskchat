# О проекте

Это простое приложение на основе фреймворка `flask`, позволяющее создавать личные чаты и обмениваться сообщениями внутри них, а также присоединиться к общему чату среди всех пользователей. Приложение поддерживает систему регистрации и аутентифиакации.

# Инструменты и библиотеки

* Python версии 3.11
* Poetry - для добавления библиотек и модулей
* Flask
* Flask-SocketIO - для чата в реальном времени без обновления страниц
* Flask-Login - для возможности регистрации и авторизации
* Postgresql - для базы данных пользователей
* Flask SQlalchemy
* Jinja2
* Flask-Migrate - для изменения базы данных
* Другие библиотеки и модули можноо посмотреть в файле pyproject.toml

# Как установить

Склонируйте репозиторий в Pycharm:

	$ git clone https://github.com/rina808/flaskchat

Установите библиотеки:

	$ poetry update

Задайте имя запускаемого файла:

	$ export FLASK_APP=run.py

Или:

	$ env:FLASK_APP = "run.py"

Создайте базу данных в postgresql и замените данные в файле `.env` на данные своего пользователя и базы данных.

Инициализируйте базу данных:

	$ flask db init

Создайте миграцию, чтобы добавить модель пользователя в базу:

	$ flask db migrate

Обновите базу данных:

	$ flask db upgrade

# Запуск

Запустите приложение:

	$ flask run

Перейдите на страницу `http://localhost:5000` в одном или нескольих браузерах.
