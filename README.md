# Django Inventory Management API

## Project Overview
This is a **Django-based Inventory Management System** built with Django Rest Framework (DRF). The project allows users to manage inventory items, track changes in inventory levels, and manage categories. Additionally, it provides JWT authentication and API views for accessing and interacting with inventory data.

### Features:
- **User Registration & Authentication**
    - Custom user model with profile picture.
    - JWT-based authentication for secured endpoints.
- **Inventory Management**
    - View and manage inventory items, categories, and associated details.
    - Add/edit inventory items, including price and quantity.
    - Upload images for inventory items.
- **Change Logs**
    - Track changes in inventory, such as price and quantity updates.
    - Automatically log changes with reasons and user details.
- **Low Stock Alerts**
    - Set thresholds for items and get a view of items below a certain quantity.
- **API Documentation**
    - Swagger and ReDoc for interactive API documentation.

---

## Table of Contents
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Models](#models)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [License](#license)

---

## Installation

### Prerequisites
- Python 3.9+
- Django 5.x
- Virtual Environment (recommended)
- PostgreSQL (optional) or SQLite (default)
  
### Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/inventory-manager.git
   cd inventory-manager
Certainly! Here’s a structured README.md template for your Django Inventory Management project. It includes all the important details such as project description, setup instructions, usage, and more.

markdown
Copy code
# Django Inventory Management API

## Project Overview
This is a **Django-based Inventory Management System** built with Django Rest Framework (DRF). The project allows users to manage inventory items, track changes in inventory levels, and manage categories. Additionally, it provides JWT authentication and API views for accessing and interacting with inventory data.

### Features:
- **User Registration & Authentication**
    - Custom user model with profile picture.
    - JWT-based authentication for secured endpoints.
- **Inventory Management**
    - View and manage inventory items, categories, and associated details.
    - Add/edit inventory items, including price and quantity.
    - Upload images for inventory items.
- **Change Logs**
    - Track changes in inventory, such as price and quantity updates.
    - Automatically log changes with reasons and user details.
- **Low Stock Alerts**
    - Set thresholds for items and get a view of items below a certain quantity.
- **API Documentation**
    - Swagger and ReDoc for interactive API documentation.

---

## Table of Contents
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Models](#models)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [License](#license)

---

## Installation

### Prerequisites
- Python 3.9+
- Django 5.x
- Virtual Environment (recommended)
- PostgreSQL (optional) or SQLite (default)
  
### Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/inventory-manager.git
   cd inventory-manager
   
2. Create and Activate a Virtual Environment:
    ```bash
    python -m venv env
    source env/bin/activate  # For Linux/Mac
    .\env\Scripts\activate  # For Windows

3. Install Dependencies:

    ```bash
    pip install -r requirements.txt
4. Apply Migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
5. Create Superuser:
    ```bash
    python manage.py createsuperuser

6. Run Development Server:
    ```bash
    python manage.py runserver
