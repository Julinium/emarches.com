# eMarches.com
Visit emarches.com to see what it looks like.
eMarches.com is a web full stack application for the public procurement market in Morocco.

# Steps
01. Pull/download from github.
02. Create a python virtual env
03. Install requirements.txt
04. Start a new django project: django-admin startproject emarches .
05. Start the other apps using django-admin startapp : base, crm and portal.
06. Fill in settings in .env
07. Setup database backend and potentially email backend.
08. If running for the first time against the database, migrate models and create a superuser.
09. Copy static files
10. Test locally using "python manage.py runserver".
11. Deploy. I'm using gunicorn and nginx.

