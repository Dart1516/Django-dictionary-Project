# Overview

As a software engineer, I want to understand how server-side web frameworks generate pages dynamically. I had already built an English dictionary app in TypeScript that ran entirely in the browser, so for this project I am rebuilding the same idea with Django and Python, moving the logic to the server and adding a database. Before writing my own app, I worked through the official Django tutorial (parts 1–5) to learn models, views, URLs, templates, forms and testing.

**Django Dictionary** is a vocabulary website for people learning English. The user searches for a word, the app gets its definition, and the user can save it to a personal word list to review later. The core idea is: **search → save → review**.

### How to run it

1. Activate the virtual environment from the repository root (Windows PowerShell):
   ```
   .venv\Scripts\Activate.ps1
   ```
2. Install Django (only the first time):
   ```
   pip install django
   ```
3. Go into the project folder, create the database, and start the test server:
   ```
   cd dictionary_project
   python manage.py migrate
   python manage.py runserver
   ```
4. Open **http://127.0.0.1:8000/** in a web browser.

My purpose for writing this software is to learn how a request travels through a web framework: from the URL, to a Python view, to the database, and back to the user as an HTML page generated from a template.

[Software Demo Video](http://youtube.link.goes.here)

# Web Pages

{Describe each of the web pages you created and how the web app transitions between each of them.  Also describe what is dynamically created on each page.}

# Development Environment

* Visual Studio Code
* Git and GitHub for version control
* Python virtual environment (`venv`)
* Django's built-in development server and admin site

**Language and libraries:**

* Python 3.14
* Django 6.1 — web framework (URLs, views, templates, ORM)
* SQLite — database, through Django's ORM

# Useful Websites

* [Django Overview](https://docs.djangoproject.com/en/6.1/intro/overview/)
* [Django Installation Guide](https://docs.djangoproject.com/en/6.1/intro/install/)
* [Django Tutorial (parts 1–5)](https://docs.djangoproject.com/en/6.1/intro/tutorial01/)
* [Django Templates](https://docs.djangoproject.com/en/6.1/topics/templates/)
* [Django Settings](https://docs.djangoproject.com/en/6.1/topics/settings/)
* [Django Deployment Checklist](https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/)
* [Python Tutorial: Modules and Packages](https://docs.python.org/3/tutorial/modules.html#tut-packages)
* [Django Forum](https://forum.djangoproject.com/)

# Future Work

* Mark words as learned and filter the list by pending / learned words
* Show more information for each word (examples, synonyms, pronunciation)
* Add user accounts so each person has their own word list
* Deploy the app online so it can be used outside my computer
