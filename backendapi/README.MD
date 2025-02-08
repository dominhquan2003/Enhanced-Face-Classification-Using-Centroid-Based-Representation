### Delete database 
Delete the sqlite database file (often db.sqlite3) in your django project folder (or wherever you placed it)
Delete everything except __init__.py file from migration folder in all django apps (eg: rm */migrations/0*.py)
Make changes in your models (models.py).
Run the command python manage.py makemigrations or python3 manage.py makemigrations
Then run the command python manage.py migrate.
### Reset 
manage.py flush