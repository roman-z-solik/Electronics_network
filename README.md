# Electronics Supply Chain Platform

Django REST API для управления сетью продаж электроники. Приложение позволяет создавать, отслеживать и управлять иерархической структурой поставщиков (заводы, розничные сети, индивидуальные предприниматели) с системой контроля задолженностей.

## Технологии

- **Python 3.13** - основной язык программирования
- **Django 5.2** - веб-фреймворк
- **Django REST Framework 3.16** - REST API
- **PostgreSQL 15** - база данных
- **Django Filter** - фильтрация данных
- **Docker** - контейнеризация (опционально)

## Использование

Открыть проект в PyCharm или другой IDE.

### Приложение users

**`users/models.py`**:

`CustomUser` - кастомная модель пользователя с дополнительными полями: телефон, отдел, должность. Основана на AbstractUser.

**`users/admin.py`**:

`CustomUserAdmin` - кастомизированная админ-панель для пользователей с отображением дополнительных полей.

### Приложение electronics

**`electronics/models.py`**:

`Product` - модель продукта с полями: название, модель, дата выхода на рынок.

`NetworkNode` - модель звена сети с полями: название, тип звена (завод/розничная сеть/ИП), контактные данные (email, страна, город, улица, номер дома), продукты (ManyToMany), поставщик (ForeignKey на себя), задолженность, время создания. Уровень иерархии вычисляется автоматически через свойство level.

**`electronics/serializers.py`**:

`ProductSerializer` - сериализатор для продуктов  
`NetworkNodeSerializer` - сериализатор для звеньев сети с валидацией запрета обновления поля debt

**`electronics/views.py`**:

`IsActiveEmployee` - permission только для активных сотрудников  
`NetworkNodeViewSet` - ViewSet для CRUD операций со звеньями сети с фильтрацией по стране

**`electronics/admin.py`**:

`ProductAdmin` - админ-панель для продуктов  
`NetworkNodeAdmin` - админ-панель для звеньев сети с:
- Ссылкой на поставщика
- Фильтром по городу
- Action для очистки задолженности

## API Endpoints

### Аутентификация
- Сессионная аутентификация через `/api-auth/login/`
- Только активные пользователи (`is_active=True`) имеют доступ к API

### Звенья сети (NetworkNode ViewSet)
- `GET /api/network-nodes/` - список всех звеньев сети (требуется аутентификация)
- `POST /api/network-nodes/` - создание нового звена
- `GET /api/network-nodes/{id}/` - получение конкретного звена
- `PUT /api/network-nodes/{id}/` - обновление звена (запрещено обновление поля debt)
- `PATCH /api/network-nodes/{id}/` - частичное обновление
- `DELETE /api/network-nodes/{id}/` - удаление звена

### Фильтрация
- `GET /api/network-nodes/?country=Россия` - фильтрация по стране
- `GET /api/network-nodes/?search=Москва` - поиск по названию, email, городу
- `GET /api/network-nodes/?ordering=-created_at` - сортировка по дате создания

## Функциональность

### Иерархическая структура
- 3 уровня: Завод (уровень 0), Розничная сеть (уровень 1), ИП (уровень 2)
- Уровень вычисляется динамически по цепочке поставщиков
- Каждое звено ссылается на одного поставщика (может быть любой уровень выше)

### Валидация и ограничения
- Запрет обновления поля `debt` через API (только через админ-панель)
- Валидация контактных данных (email, обязательные поля адреса)
- Автоматическое заполнение времени создания

### Админ-панель
- Ссылки на поставщиков в списке объектов
- Фильтры: по городу, стране, типу звена
- Admin action для очистки задолженности у выбранных объектов
- Отображение вычисляемого уровня иерархии

### Права доступа
- Только активные сотрудники имеют доступ к API
- Сессионная аутентификация
- Разграничение прав в админ-панели

## Настройка окружения
### Создайте файл .env на основе .env.sample:
Django  
SECRET_KEY          #SECRET_KEY for django project  
DEBUG               #DEBUG mode on/off (True/False)  
Database  
BASE_NAME           #NAME of postgres database  
BASE_USER           #USERNAME for postgres database  
BASE_PASSWORD       #PASSWORD for postgres database  
BASE_HOST           #HOST for postgres database  
BASE_PORT           #PORT for postgres database  

### Права доступа
- Только активные сотрудники имеют доступ к API
- Сессионная аутентификация
- Разграничение прав в админ-панели

## Запуск приложения

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Выполнение миграций
```bash
python manage.py migrate
```

### Создание суперпользователя
```bash
python manage.py createsuperuser
```

### Запуск сервера разработки
```bash
python manage.py runserver
```

## Команда проекта
[Roman Z](https://github.com/roman-z-solik)