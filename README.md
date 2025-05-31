# Foodgram - Продуктовый помощник

## Описание проекта

Foodgram - веб-приложение, позволяющее пользователям публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в избранное, а также формировать список покупок для выбранных рецептов.

## Функциональность

- Регистрация и авторизация пользователей
- Создание, просмотр, редактирование и удаление рецептов
- Фильтрация рецептов по тегам
- Добавление рецептов в избранное
- Добавление рецептов в список покупок
- Скачивание списка покупок в формате TXT
- Подписка на авторов
- Поиск по ингредиентам
- Управление профилем пользователя (смена пароля, аватара)
- Получение коротких ссылок на рецепты

## Технологии
- **Бэкенд**: Django, Django REST Framework, PostgreSQL
- **Фронтенд**: React (предоставлен в виде готового SPA-приложения)
- **Инфраструктура**: Docker, Nginx, Gunicorn
- **CI/CD**: GitHub Actions

## Требования
- Python 3.12
- Django 5.2.1
- Django REST Framework 3.16.0
- PostgreSQL 15
- Docker

## Запуск проекта

### Предварительные требования
- Docker
- Docker Compose

### Шаги по запуску

1. Клонируйте репозиторий:
```bash
git clone https://github.com/SonderLor/foodgram-st.git
cd foodgram-st
```

2. Создайте файл `.env` в директории `infra/` со следующими переменными (из `.env.example`):
```dotenv
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
```

3. Запустите проект с помощью `Docker Compose`:
```bash
cd infra
docker-compose up -d
```

4. Создайте суперпользователя:
```bash
docker-compose exec backend python manage.py createsuperuser
```

5. Приложение будет доступно по адресу http://localhost

## Автор
- [@SonderLor](https://github.com/SonderLor) Константинов Алексей