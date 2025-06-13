# 🐶 Dog API

Dog API — это небольшое RESTful API для менеджмента списка собак и их пород. 
Проект разработан с использованием Django, Django REST Framework и PostgreSQL, упакован в Docker.


# 📦 Возможности

CRUD для собак и пород

Расширенные данные при получении списка собак:

Название породы

Количество собак той же породы

Средний возраст собак той же породы

Расширенные данные при получении списка пород:

Количество собак каждой породы



# 🚀 Быстрый старт


**⚖️ Требования**

Docker

Docker Compose



⚙️ **Установка и запуск**

**Клонируем репозиторий**:

git clone https://github.com/DonnieD-tech/EffectiveMobile-Edu.git

cd dog_api/EffectiveMobile-Edu/Theme\ 3

**Собираем и запускаем контейнеры**:

docker-compose up --build

После запуска API будет доступен по адресу:

http://localhost:8000/api/


# 🛠 Архитектура проекта

dog_api/

├── main_api/                 # Приложение с логикой API

│   ├── models.py             # Модели Dog и Breed

│   ├── serializers.py        # Сериализация данных

│   ├── views.py              # ViewSet'ы

├── dog_api/                  # Основной конфигурационный модуль Django

│   ├── settings.py           # Настройки проекта

│   └── urls.py               # Основная маршрутизация

├── Dockerfile                # Инструкция сборки Docker-образа

├── docker-compose.yml        # Конфигурация контейнеров

├── .env                      # Переменные окружения

├── wait_for_db.py            # Ожидание БД перед запуском приложения

└── requirements.txt          # Зависимости проекта


# 📌 Примеры API

**📂 Список собак**

GET /api/dogs/

Content-Type: application/json

Пример ответа:
```
[
    {
        "id": 2,
        "name": "Don",
        "age": 2,
        "breed": 1,
        "gender": "male",
        "color": "grey",
        "favorite_food": "Acana",
        "favorite_toy": "fluffy bear",
        "breed_name": "German Shepherd",
        "same_breed_count": 3,
        "avg_age_by_breed": 6.0
    },
  ...
]
```
➕ Создание собаки

POST /api/dogs/

Content-Type: application/json
```
{
    "id": 6,
    "name": "Nelly",
    "age": 5,
    "breed": 1,
    "gender": "female",
    "color": "grey",
    "favorite_food": "cookie",
    "favorite_toy": "plate",
    "breed_name": "German Shepherd"
}
```
**🔍 Список пород**

GET /api/breeds/

Content-Type: application/json
```
[
    {
        "id": 1,
        "dog_count": 3,
        "name": "German Shepherd",
        "size": "Large",
        "friendliness": 3,
        "trainability": 5,
        "shedding_amount": 4,
        "exercise_needs": 5
    },
    ...
]
```
# 🤜 Автор

**DonnieD**
