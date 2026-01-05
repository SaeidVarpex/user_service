# User Service

[![Django Version](https://img.shields.io/badge/Django-5.0+-green)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## Overview

A brief description of what this project does. This is a tutorial-friendly Django project demonstrating best practices for beginners, including models, views, templates, forms, admin customization, and environment-based configuration.

Key features:
- User authentication
- CRUD operations (example: blog posts or whatever your app does)
- Responsive templates with Bootstrap (if used)
- Database switching: SQLite (dev) / PostgreSQL (prod)

This project is designed as a learning resource for new Django developers.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Database Configuration](#database-configuration)
- [Admin Setup](#admin-setup)
- [Running Tests](#running-tests)
- [Deployment Notes](#deployment-notes)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- Python 3.10+
- pip (Python package manager)
- Virtual environment tool (recommended: venv or virtualenv)
- Git

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SaeidVarpex/user_service.git
   cd user_service
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy example env file (if needed for local overrides):
   ```bash
   cp .env.example .env
   ```

## Running the Project

1. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

3. Run the development server:
   ```bash
   python manage.py runserver
   ```

Visit http://127.0.0.1:8000/ in your browser.

## Database Configuration:

- Development (default): Uses SQLite – no extra setup required.

- Production: Switch to PostgreSQL via environment variables (see .env.example). Install psycopg2-binary and set:
   ```bash
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=your_db
   DB_USER=...
   # etc.
   ```

## Admin Setup

Access the admin panel at /admin/ with your superuser credentials. All models are registered with explanatory list displays and search fields.

## Running Tests

   ```bash
   python manage.py test
   ```

## Deployment Notes

- Use Gunicorn + Nginx or deploy to Heroku/Render/DigitalOcean.
- Set DEBUG=False and PostgreSQL env vars in production.
- Collect static files: python manage.py collectstatic

## License

MIT License
