![workflow](https://github.com/ozzimyt/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
## YaMDb Final

### О проекте:

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв. Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

### Используемые технологии:

* Django - 3.2
* Django Rest Framework - 3.12.4
* Python 3.7
* Docker
* Gunicorn
* Nginx

### Примеры запросов:

Полная документация по API Yatube доступна после запуска сервера, по адресу:

```
http://51.250.84.194:80/redoc/
```

### Как запустить проект (должен быть установлен Docker):


Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:ozzimyt/yamdb_final.git
```

```
cd yamdb_final
```
```
cd infra
```

Далее все команды выполнять из каталога `infra`.

В директории `infra` создать файл `.env` 
```
touch .env
```
```
nano .env
```
```
DB_ENGINE=django.db.backends.postgresql # используем postgresql
POSTGRES_USER=your_login # логин для подключения к БД
POSTGRES_PASSWORD=your_password # пароль для подключения к БД
DB_HOST=127.0.0.1 # ip-адресс БД
DB_PORT=5432 # порт для подключения к БД
```

Выполнить миграции:

```
docker compose exec web python manage.py makemigrations
```
```
docker compose exec web python manage.py migrate
```

Создать суперпользователя:

```
docker compose exec web python manage.py createsuperuser
```

Собрать статику в одну папку:

```
docker compose exec web python manage.py collectstatic --no-input
```