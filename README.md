# 🛒 FastAPI E-commerce Backend

## 📖 Introduction

This is a fully functional RESTful API backend for an e-commerce platform built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. It supports:

- 🧑‍💻 Admin product management
- 🔐 User authentication (signup, login, forgot & reset password)
- 🔍 Product filtering, search & browsing
- 🛒 Cart functionality
- 📦 Checkout & order history

---

## 🎯 Project Goals

The goal is to deliver a scalable, secure and maintainable backend solution with:

- Full CRUD for admin-managed products
- JWT-based authentication system
- Role-based access control (admin vs user)
- Cart & order management tied to user accounts
- Logging, validation and structured error handling

---

## 📋 Requirements

Ensure the following are installed:

- Python 3.9+
- PostgreSQL
- Alembic (for DB migrations)
- Postman (for API testing)
- Git (for version control)

---

## ⚙️ Tech Stack

| Category          | Tool / Library          |
| ----------------- | ----------------------- |
| Backend Framework | FastAPI                 |
| ORM & DB          | SQLAlchemy + PostgreSQL |
| Authentication    | JWT                     |
| Password Hashing  | bcrypt                  |
| Validation        | Pydantic                |
| Migrations        | Alembic                 |
| Web Server        | Uvicorn                 |
| Logging           | Python Logging Module   |
| Email             | FastAPI-compatible SMTP |

---

## 📁 Folder Structure

```
Ecommerce-Project/
├── alembic/
│ └── versions/
├── app/
│ ├── auth/
│ │ ├── models.py
│ │ ├── routes.py
│ │ ├── crud.py
│ │ ├── schemas.py
│ ├── products/
│ │ ├── models.py
│ │ ├── routes.py
│ │ ├── crud.py
│ │ ├── schemas.py
│ ├── cart/
│ ├── orders/
│ ├── core/
│ │ ├── config.py
│ │ ├── database.py
│ ├── utils/
│ │ ├── oauth2.py
│ │ ├── email.py
├── seed_products.py
├── main.py
├── requirements.txt
├── .env
├── alembic.ini
└── README.md
```

---

## 👨‍💻 Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ecommerce-backend.git
cd ecommerce-backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file in your project root and add the following:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/ecommerce_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

### 5. Run Alembic Migrations

Apply database schema to your PostgreSQL database using Alembic:

```bash
alembic upgrade head
```

### 6. Seed Sample Products

To populate your database with initial product data, run:

```bash
python seed_products.py
```

### 7. Start the Application

Launch the FastAPI server:

```bash
uvicorn main:app --reload
Once the server is running, you can explore the API documentation:

Swagger UI → http://localhost:8000/docs
ReDoc → http://localhost:8000/redoc
```

---

## 🧪 API Testing

Use the included Postman collection or Swagger UI to test the API endpoints.

### 🔐 Auth Endpoints

- `POST /auth/signup` – Register a new user
- `POST /auth/signin` – Login and get tokens
- `POST /auth/forgot-password` – Request password reset
- `POST /auth/reset-password` – Reset password using token

### 📦 Product Endpoints

- `GET /public/products/` – List all public products
- `GET /public/search?query=...` – Search products
- `POST /admin/products/` – Admin: create product
- `PUT /admin/products/{id}` – Admin: update product
- `DELETE /admin/products/{id}` – Admin: delete product

### 🛒 Cart Endpoints

- `POST /cart/add` – Add item to cart
- `GET /cart/view` – View cart items
- `PUT /cart/update` – Update quantity
- `DELETE /cart/delete/{product_id}` – Remove item

### 📑 Orders & Checkout

- `POST /orders/checkout` – Place an order
- `GET /orders/` – Get order history
- `GET /orders/{order_id}` – Get order details

---

## 🔒 Security Highlights

- Passwords are securely hashed using **bcrypt**
- JWT-based authentication for access and refresh tokens
- Reset tokens are:
  - One-time use
  - Time-limited (expire after 30 minutes)
- Role-based access control (admin vs user)
- Input validation using **Pydantic**
- Centralized error handling with consistent response format

---

## 🧾 Database Tables

| Table                   | Description                                |
| ----------------------- | ------------------------------------------ |
| `users`                 | Stores user info, roles, hashed passwords  |
| `products`              | Admin-managed product listings             |
| `cart_items`            | User-specific cart item records            |
| `orders`                | Orders placed by users                     |
| `order_items`           | Items associated with each order           |
| `password_reset_tokens` | One-time secure tokens for password resets |

---

## ❌ Error Response Format

All error responses follow a consistent structure:

```json
{
  "error": true,
  "message": "Reason for failure",
  "code": 400
}
```

---

## 🧪 Manual Testing Checklist

- ✅ Signup, login, logout functionality
- ✅ Forgot password + reset password flow
- ✅ Admin: create, update, delete products
- ✅ Public: browse & search products
- ✅ Cart: add, update, remove items
- ✅ Checkout: place orders
- ✅ Orders: view history and order details

---

## 🙋 Author

**Ishika Sadhwani**  
B.Tech CSE  
GitHub: [@ishikasadhwani](https://github.com/ishikasadhwani)  
Email: ishikasadhwani.tech@gmail.com
