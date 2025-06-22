# 🍲 Recipe App

![Django CI](https://github.com/reconized/recipe-app/actions/workflows/django-ci.yml/badge.svg)

A modern, API-first Django app for recipe sharing.

## 📦 Features

- 🧆 Categorize recipes by **cuisine**
- 🥞 Tag items for **specific categories**
- 📱 RESTful API design (built with Django Rest Framework)
- 🧪 Built-in testing and CI via GitHub Actions
- 🐳 Containerized with Docker

## 🚀 Tech Stack

- Django 5.x
- Django REST Framework
- PostgreSQL (via Docker)
- Pipenv for dependency management
- GitHub Actions for CI/CD
- Docker & docker-compose
- Python-dotenv for environment management

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/reconized/recipe-app.git
cd recipe-app
```

### 2. Install Dependencies
```bash
pipenv install --dev
```

### 3. Set Up Your ```.env```
```bash
DJANGO_SECRET_KEY=your-secret-key
DJANGO_SETTINGS_MODULE=recipe_app.settings.dev
DEBUG=True
DATABASE_URL=postgres://recipe_user:recipe_pass@localhost:5432/recipe_db
```

### 4. Run the Server
```bash
pipenv run python manage.py migrate
pipenv run python manage.py runserver
```

### 5. Run Tests
```bash
pipenv run python manage.py test
```

## 🐳 Docker Usage
```bash
docker-compose up --build
```
Access the app at: http://localhost:8000


## 🛠️ API Documentation
API is documented using **OpenAPI 3.0** in ```api_docs/recipe_api.yaml```.

You can visualize it using:

- [Swagger Editor](https://editor.swagger.io/)
- [Redoc](https://redocly.github.io/redoc/) 


## 🤝 Contributing
**1.** Fork the repo

**2.** Create your feature branch (```git checkout -b feature/new-feature```)

**3.** Commit your changes (```git commit -am 'Add new feature'```)

**4.** Push to the branch (```git push origin feature/new-feature```)

**5.** Open a Pull Request

## 📝 License
This project is licensed under the MIT License.

## 📬 Contact
For questions, feel free to reach out on [GitHub Issues](hhttps://github.com/reconized/recipe-app/issues).