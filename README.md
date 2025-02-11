## Тестовое задание

# Web-сервер на фреймворке Sanic

Текст ТЗ указан в файле "[Web_Server_ТЗ.docx](Web_Server_%D2%C7.docx)"

__Доступные адреса (эндпоинты) и функции:__

* "/" - корневой адрес - страница приветствия
* "/login" - страница ввода данных для авторизации
* "/logout" - страница выхода из авторизации
* "/user/" - страница получения списка зарегистрированных пользователей
* "/user/<user_id:int>" - страница Личного Кабинета авторизованного пользователя
* "/user/<user_id:int>/accounts" - страница отображения списка счетов пользователя
* "/user/<user_id:int>/payments" - страница отображения списка платежей пользователя
* "/user/crud/create" - страница создания нового аккаунта (пользователя)
* "/user/crud/update" - страница обновления данных пользователя
* "/user/crud/delete" - страница удаления пользователя из БД

### Тестовые аккаунты:

1. Пользователь:
* **Логин**: user@example.com
* **Пароль**: user123

2. Администратор:
* **Логин**: admin@example.com
* **Пароль**: admin123

### Команды для запуска:
* pip install -r requirements.txt
* alembic upgrade head 
* docker-compose up --build

### Простейший эмулятор платежной системы:
https://github.com/ildarius116/Webhook_payment_service

### Примеры:

* ### _"/":_
* ![welcome.JPG](README%2Fwelcome.JPG)
* ### _"/login":_
* ![login.JPG](README%2Flogin.JPG)
* ### _"/user/" - только для админа:_
* ![user_list.JPG](README%2Fuser_list.JPG)
* ### _"/user/<user_id:int>" - для пользователя и админа:_
* ![lk_user.JPG](README%2Flk_user.JPG)
* ![lk_admin.JPG](README%2Flk_admin.JPG)
* ### _"/user/<user_id:int>/accounts" - для пользователя и админа:_
* ![accounts_user.JPG](README%2Faccounts_user.JPG)
* ![accounts_admin.JPG](README%2Faccounts_admin.JPG)
* ### _"/user/<user_id:int>/payments" - только для пользователя:_
* ![payments_user_null.JPG](README%2Fpayments_user_null.JPG)
* ![payments_user.JPG](README%2Fpayments_user.JPG)
* ### _"/user/crud/create" - только для админа:_
* ![create_before.JPG](README%2Fcreate_before.JPG)
* ![create_after.JPG](README%2Fcreate_after.JPG)
* ### _"/user/crud/update" - только для админа:_
* ![update_before.JPG](README%2Fupdate_before.JPG)
* ![update_after.JPG](README%2Fupdate_after.JPG)
* ### _"/user/crud/delete" - только для админа:_
* ![delete_before.JPG](README%2Fdelete_before.JPG)
* ![delete_after.JPG](README%2Fdelete_after.JPG)
