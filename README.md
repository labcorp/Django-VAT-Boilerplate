# Django VAT (Vite, Alpine.js and Tailwind) Boilerplate
An awesome boilerplate to kickstart your next project with Django, Vite, Alpine.js, and Tailwind CSS. It’s designed for developers who want a fast, modern stack with a powerful backend and a sleek, reactive frontend — perfect for building beautiful, responsive web apps.

![Python](https://img.shields.io/badge/python-3.11-blue)
![Build](https://img.shields.io/badge/build-passing-brightgreen)

> **IMPORTANT:**  
> • Python >= 3.11.*   
> • Docker setup is not ready for production, yet :)  

### Installed django APPs
 - Django REST Framework [[github]](https://github.com/encode/django-rest-framework)
 - Django Cotton [[github]](https://github.com/wrabit/django-cotton)
 - Django Vite [[github]](https://github.com/MrBin99/django-vite)
 - Django Admin Interface [[github]](https://github.com/fabiocaccamo/django-admin-interface)
 - DjangoQL [[github]](https://github.com/ivelum/djangoql)
 - Django TinyMCE [[github]](https://github.com/jazzband/django-tinymce)
 - Django Filer [[github]][(https://github.com/ivelum/djangoql](https://github.com/django-cms/django-filer))

## Docker (development)
0. Rename `.env.example` > `.env` and update it
1. Run `docker compose build --no-cache`
2. Run `docker compose up -d`
3. Run first-time migrations with `docker compose run --rm app python manage.py migrate`
4. [optional] Run `docker compose exec app python manage.py createsuperuser` to create admin user
5. Profit...

It will create 2 containers (front and back)  
**Tip**: Search for "awesome" is all files and change it with your new project's name.

## Debugging Django App in VSCode (.vscode folder included)
Django App can be debugged attaching VSCode to the PTVSD server (launch.json is included in this boilerplate), so:

1. Add your breakpoints (or not)
2. Go to 'Run and Debug' on the left panel
3. Select 'Docker'
4. Start it (F5)  

## Simple usage (legacy, but still works - kindof)

**Front-end**
1. Run `npm install`
2. Run `npm run dev`
3. Profit...

**Back-end**
1. Create virtualenv && activate
2. Run `pip install -r requirements-dev.txt`
3. Rename `.env.example` > `.env` and update it
4. [optional] Make `manage.py` "runabble": `$ chmod +x manage.py`
5. Run first-time migrations with `./manage.py migrate`
6. [optional] Run `./manage.py createsuperuser`
7. Run `./manage.py runserver`
8. Profit...

---

### Questions?!
