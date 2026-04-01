# IrenFantasyArt
Веб-сайт-портфолио. Проект реализован на Django и включает галерею работ, блог и аналитику.

**Cайт:** [irenfantasyart.ru](https://irenfantasyart.ru/) 

## 🛠 Технологии

- **Backend:** Python 3, Django
- **Frontend:** HTML5, CSS3, JavaScript
- **База данных:** SQLite (разработка), на продакшене PostgreSQL
- **Дополнительно:** Gunicorn, Nginx (при необходимости), переменные окружения через `.env`

## 📁 Структура проекта
IrenFantasyArt/
├── IrenFantasyArt/ # Основной каталог проекта (настройки Django)
├── analytics/ # Приложение для сбора и отображения аналитики
├── artworks/ # Приложение для управления галереей
├── blog/ # Приложение для блога
├── static/ # Статические файлы (CSS, JS, изображения)
├── templates/ # Шаблоны HTML
├── manage.py # Управляющий скрипт Django
├── requirements.txt # Зависимости Python
├── .env.example # Пример файла с переменными окружения
└── .gitignore

## 🔧 Установка и запуск (локально)
1. **Клонировать репозиторий**
   ```bash
   git clone https://github.com/DanilBabikov0/IrenFantasyArt.git
   cd IrenFantasyArt
   ```
2. **Создать виртуальное окружение и активировать его**
   ```bash
   python -m venv venv
   source venv/bin/activate   # для Linux/macOS
   venv\Scripts\activate      # для Windows
   ```
3. **Установить зависимости**
   ```bash
   pip install -r requirements.txt
   ```
4. **Настроить переменные окружения**

Скопируйте .env.example в .env и заполните необходимые значения

В .env укажите SECRET_KEY, режим отладки (DEBUG) и другие параметры.
5. **Применить миграции**
   ```bash
   python manage.py migrate
   ```
6. **Создать суперпользователя**
   ```bash
   python manage.py createsuperuser
   ```
7. **Запустить сервер**
   ```bash
   python manage.py runserver
   ```

## Для продакшена
Установить DEBUG=False в .env

Настроить базу данных (например, PostgreSQL)

Собрать статические файлы: ```python manage.py collectstatic```

## Скриншоты
### Главная страница
![Скриншот главной страницы](https://private-user-images.githubusercontent.com/116505393/572460953-216aaaed-98d3-4bb9-af9e-4883dd2193ad.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzUwNDQxODgsIm5iZiI6MTc3NTA0Mzg4OCwicGF0aCI6Ii8xMTY1MDUzOTMvNTcyNDYwOTUzLTIxNmFhYWVkLTk4ZDMtNGJiOS1hZjllLTQ4ODNkZDIxOTNhZC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNDAxJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDQwMVQxMTQ0NDhaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT01MjdlMDYzODRjODhkMGM5ZmJlNWY0MjhhNWU3Yzk3ZTdlZmQxNDZiNjI1NGY4YmYzZDdkN2I4NzRkMDhmYjJlJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.QpQonzl-CjdC6xdce8GM_d9JDjwUs3HIA3o8meI83RU)
### Каталог картин
![Скриншот каталога картин](https://private-user-images.githubusercontent.com/116505393/572461151-de793374-987c-4caf-8fa4-fa4ce8cf9f09.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzUwNDQxODgsIm5iZiI6MTc3NTA0Mzg4OCwicGF0aCI6Ii8xMTY1MDUzOTMvNTcyNDYxMTUxLWRlNzkzMzc0LTk4N2MtNGNhZi04ZmE0LWZhNGNlOGNmOWYwOS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNDAxJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDQwMVQxMTQ0NDhaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT00Zjk3MjM0ZWE1OWE3ZTBiNTc2N2JjOWFkMzdiMTM4MWU3ZmRmNzRhNjNmMjMyOTRmNmFlYThlMDNlOTU4Y2U2JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.Lpn9ad3hTF1PUo1EDoxSRIcdAPlJ5CxXo0yEQXaQ_Ng)
### Коллекции картин
![Скриншот коллекций картин](https://private-user-images.githubusercontent.com/116505393/572461574-da4e54ad-07c5-4a5a-8145-90920fde163d.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzUwNDQxODgsIm5iZiI6MTc3NTA0Mzg4OCwicGF0aCI6Ii8xMTY1MDUzOTMvNTcyNDYxNTc0LWRhNGU1NGFkLTA3YzUtNGE1YS04MTQ1LTkwOTIwZmRlMTYzZC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNDAxJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDQwMVQxMTQ0NDhaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0zYzE2ODZmMzg5YTE5ODVjYWY2YWQzMGJhOWNlZjBhMTk3OTczYmEyNmYzYjgzZjRlZTMxMmZjYWJkMzhjYmI0JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.q5pA_THeKF-yaWxMifAbHj4iDVmx3VSig81zDkqjmmQ)
### Аналитика
![Скриншот аналитики](https://private-user-images.githubusercontent.com/116505393/572461862-c8e29f2f-7154-483d-be39-0c34b937c6bf.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzUwNDQxODgsIm5iZiI6MTc3NTA0Mzg4OCwicGF0aCI6Ii8xMTY1MDUzOTMvNTcyNDYxODYyLWM4ZTI5ZjJmLTcxNTQtNDgzZC1iZTM5LTBjMzRiOTM3YzZiZi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNDAxJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDQwMVQxMTQ0NDhaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1lNGM3Njc0MzIxZDc3ZjM5YmIzYzYyMDFkZjhkMjgyNDZjMTNjNzAyYmI4NWMyNjM2OWFmZWIyM2RkNTJjYWU3JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.wozdDlVUUorxSzkas9zp_QRV9N5WUzp023S6sjrxtdQ)

## 📄 Лицензия
Проект не содержит явной лицензии. Все права принадлежат автору.

## 👤 Автор
Danil Babikov
