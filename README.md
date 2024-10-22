

---

# Task Manager Backend

This repository contains the **FastAPI** backend for the Task Manager application. It provides a RESTful API for task management operations, including user authentication and task CRUD functionality.

## Features

- **Task Management API**: Endpoints for creating, reading, updating, and deleting tasks.
- **User Authentication**: User registration and login functionality.
- **Task Filtering**: Filter tasks by completion status.
- **User-Specific Tasks**: Each user has their own set of tasks.
- **SQLAlchemy ORM**: For database management.
- **JWT Authentication**: Secured routes using JSON Web Tokens (JWT).
  
## Technologies Used

- **FastAPI**: High-performance Python framework for building APIs.
- **SQLAlchemy**: ORM for interacting with the database.
- **SQLite**: Default database (can be switched to PostgreSQL, MySQL, etc.).
- **Pydantic**: Data validation and serialization.
- **Passlib**: For secure password hashing.
- **JWT**: For secure user authentication.
- **Uvicorn**: ASGI server to run the FastAPI application.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Virtual environment tool (optional but recommended)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Rhonaiye/Task-manager-backend-made-with-Fastapi.git
    cd task-manager-backend
    ```

2. Set up a virtual environment:

    ```bash
    python -m venv fastenv
    source fastenv/bin/activate  # On Windows, use fastenv\Scripts\activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file for environment variables:

    ```bash
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5. Run the database migrations (if using migrations):

    ```bash
    alembic upgrade head
    ```

6. Start the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

7. The API will be accessible at [http://localhost:4000](http://localhost:4000).

## Project Structure

```bash
.
├── alembic/                    # Alembic migrations
├── database.py                 # Database connection
├── models.py                   # SQLAlchemy models
├── routers/                    # API routers (auth, todos, etc.)
├── schemas/                    # Pydantic schemas for validation
├── auth.py                     # Authentication functions (JWT, password hashing)
├── main.py                     # FastAPI entry point
├── .env                        # Environment variables
└── requirements.txt            # Python dependencies
```

## API Endpoints

### Auth

- **POST /auth/register**: Register a new user.
- **POST /auth/login**: Login and get a JWT token.

### Todos

- **GET /todos/**: Get all tasks for the authenticated user.
- **GET /todos/{id}**: Get a task by its ID.
- **POST /todos/**: Create a new task.
- **PUT /todos/{id}**: Update a task.
- **DELETE /todos/{id}**: Delete a task.
- **PATCH /todos/{id}/complete**: Mark a task as complete.

### Example Request

To create a task:

```bash
POST /todos/
Authorization: Bearer <JWT_TOKEN>

{
  "title": "Buy groceries",
  "description": "Get milk, eggs, and bread",
}
```

## Authentication

This API uses **JWT** for authentication. After logging in, include the token in the `Authorization` header of all subsequent requests:

```bash
Authorization: Bearer <JWT_TOKEN>
```

## Running the Backend

1. **Start the development server**:

    ```bash
    uvicorn main:app --reload --port 4000
    ```

2. **Running in Production**:

    Use a production-ready server like **gunicorn**:

    ```bash
    gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
    ```

## Running Tests

You can write tests using **pytest**. To run the test suite:

```bash
pytest
```

## Deployment

1. Set environment variables for production in `.env`.
2. Use a production ASGI server such as **gunicorn**.
3. Ensure your database and secret keys are properly configured.

## License

This project is licensed under the MIT License.

---
