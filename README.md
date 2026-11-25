# Inventory Management Backend API

A RESTful backend API for managing inventory, products, categories, suppliers, warehouses, and stock movements (`IN` / `OUT` / `ADJUSTMENT`), built with **Django** and **Django REST Framework (DRF)**.

## Key Features

- **JWT Authentication**: Token-based authentication using `djangorestframework-simplejwt`.
- **Role-Based Access Control (RBAC)**: Custom user roles (`ADMIN`, `MANAGER`, `STAFF`) with granular viewset permissions:
  - `IsStaffOrReadOnly` for `Supplier`, `Category`, `Warehouse`, and `Stock Movement` endpoints.
  - `IsAuthenticatedDeleteStaffOnly` for `Product` endpoints (authenticated users can create/read/update, while `DELETE` is restricted to staff/superusers).
- **Stock Movement Validation**: Handles stock `IN` and `OUT` operations with edge-case checks (preventing negative stock, zero/negative quantities, or exceeding available stock).
- **Environment-Based Configuration**: Loads sensitive settings such as `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` from a local `.env` file.
- **Interactive API Documentation**: OpenAPI schema, Swagger UI, and ReDoc powered by `drf-spectacular`.
- **Unit & Integration Tests**: Automated API tests covering permissions, JWT auth, and stock `OUT` edge cases.

## Tech Stack

- **Language**: Python
- **Framework**: Django, Django REST Framework
- **Authentication**: `djangorestframework-simplejwt`
- **API Schema & Docs**: `drf-spectacular`
- **Database**: SQLite (local development)

## Project Structure (Overview)

- `config/` — Project settings, root URLs, and environment loading
- `account/` — Custom user model, roles, and authentication
- `inventory/` — Categories, suppliers, warehouses, and products
- `transactions/` — Stock movement (`IN` / `OUT` / `ADJUSTMENT`) logic and endpoints

## API Endpoints Overview

| Category | Method | Endpoint | Access / Permission | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Auth** | `POST` | `/api/token/` | Public | Obtain JWT access & refresh tokens |
| **Auth** | `POST` | `/api/token/refresh/` | Public | Refresh expired access token |
| **Products** | `GET` | `/api/v1/products/` | Authenticated / Read | List all products |
| **Products** | `POST` | `/api/v1/products/` | Authenticated | Create a new product |
| **Products** | `PUT` / `PATCH` | `/api/v1/products/{id}/` | Authenticated | Update an existing product |
| **Products** | `DELETE` | `/api/v1/products/{id}/` | Staff / Superuser only | Delete a product |
| **Categories** | `GET` / `POST` / `PUT` / `DELETE` | `/api/v1/categories/` | Staff write, Read-only others | Manage product categories |
| **Suppliers** | `GET` / `POST` / `PUT` / `DELETE` | `/api/v1/suppliers/` | Staff write, Read-only others | Manage suppliers |
| **Warehouses** | `GET` / `POST` / `PUT` / `DELETE` | `/api/v1/warehouses/` | Staff write, Read-only others | Manage warehouses |
| **Stock Movements** | `GET` / `POST` | `/api/v1/movements/` | Staff write, Read-only others | Record stock `IN` / `OUT` / `ADJUSTMENT` movements |

### Authentication Header Example

Include the JWT `access` token in the `Authorization` header for protected requests:

```http
Authorization: Bearer <your_access_token>
```

## Local Setup & Installation

### 1. Clone the repository & create a virtual environment

```bash
git clone <your-repository-url>
cd <your-project-folder>
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Configure environment variables
Create a .env file in the project root (do not commit .env to Git):

```env
SECRET_KEY=replace-with-your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 4. Run migrations & start the development server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## API Documentation
Once the server is running, access the interactive documentation at:

- Swagger UI: http://127.0.0.1:8000/api/docs/

- ReDoc: http://127.0.0.1:8000/api/redoc/

- OpenAPI Schema: http://127.0.0.1:8000/api/schema/


## Running Tests
Run the test suite with verbose output:
```bash
python manage.py test -v 2
```