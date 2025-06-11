# 📋 Billing Management System

A microservice-based backend for managing billing operations, built with **FastAPI**, **PostgreSQL**, and a modular architecture that follows clean separation of concerns.

---

## 📁 Project Structure

```
BillingManagerService/
├── app/
│   ├── __init__.py
│   ├── setup.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py              # Application configuration (e.g., DB URLs)
│   ├── fs/
│   │   ├── __init__.py
│   │   └── fs.py                  # Persistence layer
│   ├── logic/
│   │   ├── __init__.py
│   │   ├── Core/                  # Business logic
│   │   │   ├── Bill.py
│   │   │   ├── user.py
│   │   │   └── __init__.py
│   │   ├── DTO/                   # Request/response DTOs
│   │   │   ├── Bill.py
│   │   │   ├── user.py
│   │   │   └── __init__.py
│   │   ├── handlers/              # Application services
│   │   │   ├── __init__.py
│   │   │   ├── Bill_handler.py
│   │   │   └── user_handler.py
│   │   ├── event_processor/       # For scheduled events, e.g., reminders
│   │   │   ├── __init__.py
│   │   │   └── Bill_reminder_event_processor.py
│   │   └── utils/
│   │       └── __init__.py
│   ├── middlewares/              # Custom middlewares
│   │   └── __init__.py
│   ├── routers/                  # Route registration
│   │   ├── __init__.py
│   │   └── router.py
│   └── tests/                    # Unit and integration tests
│       └── __init__.py
├── main.py                       # Entry point
```

---

## ⚙️ Tech Stack

* **FastAPI** – Modern async web framework
* **PostgreSQL** – Relational DB
* **SQLAlchemy** – ORM
* **Pydantic** – Data validation and serialization
* **Requests** – For testing HTTP endpoints

---

## 🚀 Getting Started

### 1. 🐍 Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# OR
.venv\Scripts\activate          # Windows
```

---

### 2. 📦 Install dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, create one by freezing:

```bash
pip freeze > requirements.txt
```

---

### 3. 🛠️ Configure environment variables

Edit or create `.env` in the root or use `config/config.py`. Sample `.env`:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/billing_db
JWT_SECRET=your-secret-key
```

Make sure `config/config.py` reads from these variables using `os.getenv()`.

---

### 4. 📄 Run PostgreSQL

Ensure PostgreSQL is running and the DB `billing_db` exists. You can create it using:

```bash
psql -U postgres -c "CREATE DATABASE billing_db;"
```

---

### 5. 🏃 Run the server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8980
```

Visit: [http://localhost:8980/docs](http://localhost:8980/docs) for Swagger UI.

---

### 6. 🧪 Run Tests

You can run tests using:

```bash
python tests/test_user_route.py
```

Ensure a test user is seeded if your tests depend on authentication. You can create a seed script:

```bash
python seed_user.py
```

---

## 🧠 Architecture (Clean Hexagonal Style)

```
Client (Browser / Mobile)
        │
        ▼
FastAPI Route Handlers (routers/router.py)
        │
        ▼
Application Services (handlers/user_handler.py / Bill_handler.py)
        │
        ▼
Business Logic Layer (Core/*.py)
        │
        ▼
Persistence Layer (fs/fs.py)
        │
        ▼
Database (PostgreSQL)
```

---

## 📌 Notes

* DTOs (`logic/DTO`) are used for request/response validation.
* Handlers are the service layer — orchestrating logic and persistence.
* Core contains pure domain logic, free of frameworks.
* `event_processor` handles background or scheduled tasks (e.g., reminders).
* Use `middlewares/` to inject headers, handle auth, etc.

---

## 🔒 Authentication

Login using:

```json
POST /api/v0.1/auth/login
{
  "username": "admin",
  "password": "admin123"
}
```

The response will include a JWT token, which should be used in `Authorization` headers:

```
Authorization: Bearer <your_token>
```

---

## ✅ To Do

* [ ] Add user registration
* [ ] Background task scheduling with Celery or FastAPI scheduler
* [ ] Better test coverage using pytest
* [ ] Docker support

---

## 👨‍💼 Author

Tsegay Negassi
2025 © All rights reserved

---
Bill data api's
===============
1. Create Bill — POST /api/v0.1/bills/


{
  "method": "POST",
  "url": "http://localhost:8000/api/v0.1/bills/",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN",
    "Content-Type": "application/json"
  },
  "body": {
    "biller_id": "uuid-string",
    "customer_id": "uuid-string",
    "amount": 123.45,
    "due_date": "2025-07-15T00:00:00Z",
    "status": "pending",
    "description": "Electricity bill for June"
  }
2. Read Bill by ID — GET /api/v0.1/bills/{bill_id}

{
  "method": "GET",
  "url": "http://localhost:8000/api/v0.1/bills/your-bill-uuid",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN"
  }
}
3. Update Bill by ID — PUT /api/v0.1/bills/{bill_id}
{
  "method": "PUT",
  "url": "http://localhost:8000/api/v0.1/bills/your-bill-uuid",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN",
    "Content-Type": "application/json"
  },
  "body": {
    "amount": 150.00,
    "status": "paid",
    "description": "Updated bill amount after adjustment"
  }
}
4. Delete Bill by ID — DELETE /api/v0.1/bills/{bill_id}
{
  "method": "DELETE",
  "url": "http://localhost:8000/api/v0.1/bills/your-bill-uuid",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN"
  }
}
5. Get Bills by Status — GET /api/v0.1/bills/status/{status}
{
  "method": "GET",
  "url": "http://localhost:8000/api/v0.1/bills/status/paid",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN"
  }
}
6. Get Bills by Customer ID — GET /api/v0.1/bills/customer/{customer_id}
{
  "method": "GET",
  "url": "http://localhost:8000/api/v0.1/bills/customer/customer-uuid",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN"
  }
}
7. Get Bills by Biller ID — GET /api/v0.1/bills/biller/{biller_id}
{
  "method": "GET",
  "url": "http://localhost:8000/api/v0.1/bills/biller/biller-uuid",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN"
  }
}
8.Get All Bills — GET /api/v0.1/bills/all
{
  "method": "GET",
  "url": "http://localhost:8000/api/v0.1/bills/all",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN"
  }
}
9.Get Own Bills — GET /api/v0.1/bills/my-bills
{
  "method": "GET",
  "url": "http://localhost:8000/api/v0.1/bills/my-bills",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN"
  }
}
10. Get Reports — GET /api/v0.1/bills/report
{
  "method": "GET",
  "url": "http://localhost:8000/api/v0.1/bills/report",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN"
  }
}


