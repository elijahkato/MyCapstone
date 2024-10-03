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


## Access the Admin Panel
- **Admin Panel**: Visit [Admin Panel](http://127.0.0.1:8000/admin/)

## API Documentation
- **Swagger UI**: Visit [Swagger UI](http://127.0.0.1:8000/swagger/)
- **ReDoc**: Visit [ReDoc](http://127.0.0.1:8000/redoc/)

---

## API Endpoints

### Authentication Endpoints
| Method | Endpoint              | Description             |
|--------|-----------------------|-------------------------|
| POST   | `/api/token/`          | Obtain JWT Token        |
| POST   | `/api/token/refresh/`  | Refresh JWT Token       |
| POST   | `/register/`           | Register new user       |

---

### Inventory Management
| Method | Endpoint                  | Description                       |
|--------|---------------------------|-----------------------------------|
| GET    | `/api/inventory/`          | Get all inventory items           |
| POST   | `/api/inventory/`          | Create a new inventory item       |
| GET    | `/api/inventory/<id>/`     | Retrieve a single inventory item  |
| PATCH  | `/api/inventory/<id>/`     | Update an inventory item          |
| DELETE | `/api/inventory/<id>/`     | Delete an inventory item          |

---

### Change Logs
| Method | Endpoint                          | Description                 |
|--------|-----------------------------------|-----------------------------|
| GET    | `/api/inventory-change-logs/`      | Get all inventory change logs|
| GET    | `/api/inventory-change-logs/<id>/` | Get change log by ID         |

---

### Low Stock Items
| Method | Endpoint                  | Description                          |
|--------|---------------------------|--------------------------------------|
| GET    | `/api/inventory/low-stock/`| Get all items below their low stock threshold |

---

## Usage

### Create Inventory Items:
- **Admin users** can create categories and assign inventory items.
- Each item has a **name**, **price**, **quantity**, and **associated category**.

### Track Inventory Changes:
- Automatic change logs are maintained for every edit to inventory **quantity** or **price**.
- **Admins** can also add reasons for any change.

### Low Stock View:
- Set **low stock thresholds** for items.
- View all items that have stock levels **below the threshold**.

---

## Models

### CustomUser:
- Custom user model with additional fields like **profile picture**.

### Category:
- Categories to organize inventory items.

### InventoryItem:
- Represents each inventory item, with fields for **quantity**, **price**, and **image**.

### InventoryChangeLog:
- Logs changes to inventory such as **price** or **quantity adjustments**.

---

## Technologies Used
- **Backend**: Django, Django Rest Framework
- **Authentication**: JWT Authentication (Simple JWT)
- **API Documentation**: Swagger UI, ReDoc
- **Image Handling**: Pillow, ImageKit
- **Database**: SQLite (default) / PostgreSQL (optional)


6. Run Development Server:
    ```bash
    python manage.py runserver
