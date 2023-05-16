# online_store app
##online магазин по продаже электроники\
``выполните клонирование репозитория``\
git clone https://github.com/sirotkinnikolay/online_store.git

``установите необходивые библиотеки из файла requirements.txt``\
pip install -r requirements.txt

``примените миграции``\
python manage.py makemigrations\
python manage.py migrate

``зугрузите фикстуру для тестового запуска``\
python manage.py loaddata fixtures/online.json