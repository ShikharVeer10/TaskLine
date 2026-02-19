# 🚀 TaskLine

**A high-performance, AI-ready Task Management API built with FastAPI and Supabase.**

TaskLine is a modern backend solution designed to help users organize, prioritize, and track their tasks efficiently. Built with a focus on clean architecture, security, and scalability, it serves as a robust foundation for next-generation productivity applications.

---

## ✨ Key Features

- **🔐 Secure Authentication**
  - Full OAuth2 implementation with Password Flow
  - JWT (JSON Web Token) access tokens
  - Secure password hashing with Bcrypt
  - Automatic superuser creation on startup

- **📝 Smart Task Management**
  - Complete CRUD operations (Create, Read, Update, Delete)
  - Priority levels (`low` to `urgent`) and status tracking (`todo`, `in_progress`, `completed`)
  - filtering and pagination support

- **⚡ Modern Tech Stack**
  - **FastAPI**: High performance, easy to learn, fast to code, ready for production.
  - **SQLModel**: Combines SQLAlchemy and Pydantic for intuitive database interactions.
  - **Supabase / PostgreSQL**: Scalable and reliable database backend.
  - **Alembic**: Lightweight database migration tool.

- **🛡️ Enterprise-Grade Security**
  - CORS configuration for frontend integration
  - Environment-based configuration management
  - Production-ready security headers and validation

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Language** | Python 3.10+ |
| **Database** | PostgreSQL (via Supabase) |
| **ORM** | [SQLModel](https://sqlmodel.tiangolo.com/) |
| **Migrations** | Alembic |
| **Auth** | PyJWT + Passlib |

---

## 🚀 Getting Started

Follow these steps to get the backend running locally.

### Prerequisites

- Python 3.10 or higher
- A [Supabase](https://supabase.com/) project (or any PostgreSQL database)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/taskline.git
cd taskline/backend
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

### 4. Configure Environment

Create a `.env` file in the `backend` directory:

```env
# Project
PROJECT_NAME="TaskLine"
ENVIRONMENT="local"

# Security
SECRET_KEY="your-super-secret-key-change-in-production"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database (Supabase PostgreSQL Connection)
# Format: postgresql://USER:PASSWORD@HOST:PORT/DB_NAME
DATABASE_URL="postgresql://postgres:[YOUR-PASSWORD]@db.project-ref.supabase.co:5432/postgres"

# Initial Admin User
FIRST_SUPERUSER_EMAIL="admin@taskline.com"
FIRST_SUPERUSER_PASSWORD="changethis"

# CORS (Frontend origins)
BACKEND_CORS_ORIGINS="http://localhost:3000,http://localhost:5173"
```

### 5. Run Database Migrations

Initialize the database tables:

```bash
alembic upgrade head
```

### 6. Start the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at: **http://127.0.0.1:8000**

---

## 📖 API Documentation

TaskLine comes with interactive API documentation generated automatically by FastAPI.

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) - Interactive exploration and testing.
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) - Alternative clean documentation view.

---

## 🧪 Testing Endpoints

You can test the API using the Swagger UI or via `curl`.

**Login (Get Token):**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/login/access-token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@taskline.com&password=changethis"
```

**Create a Task:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/tasks/" \
     -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"title": "My First Task", "priority": "high"}'
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
