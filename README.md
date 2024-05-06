<h1>Як запустити тестове завдання ?</h1>

1. Склонуйте репозиторій проекту:
https://github.com/Yaroslavv05/TestTaskCheckBox.git

2. Встановіть залежності:
[text](pip install -r requirements.txt)

3. Підключення своєї бази данних. Це можна зробити в файлику db_services.py, який знаходиться за таким путем: services/db_services.py

4. Потрібно зробити міграції для цього потрібно перейти в дерикторію alembic и відправити таку команду:
[text](alembic upgrade head)

5. Для того щоб запустити тести потрібно відправити таку команду:
[text](python -m pytest .\Tests\)

6. Для того щоб запустити проект потрібно прописати таку команду:
[text](uvicorn main:app)

<h3>Після цього проект буде доступний за цим посиланням - [text](http://127.0.0.1:8000/docs#/)</h3>