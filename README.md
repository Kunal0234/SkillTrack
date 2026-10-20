# SkillTrack LMS

**SkillTrack LMS** is a Learning Management System built to help students access learning resources and instructors manage courses through a structured platform.

The project is being developed as a full-stack application using modern backend technologies and a React frontend.

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- JWT Authentication
- Pytest

### Frontend

- React
- Vite
- JavaScript

## Features

### Implemented

- User registration
- User login
- Password hashing
- JWT-based authentication
- Protected API endpoints
- PostgreSQL database integration
- User and Course database models
- Initial automated API tests

### Planned

- Role-based access for students and instructors
- Course creation and management
- Course enrollment
- Student learning dashboard
- Course progress tracking
- Frontend integration with the backend
- Expanded automated test coverage

## Project Structure

```text
SkillTrack/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   └── tests/
├── frontend/
├── .gitignore
└── README.md
```

_The structure may evolve as development continues._

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL
- Node.js and npm

### Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Kunal0234/SkillTrack.git
   cd SkillTrack
   ```

2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r backend/requirements.txt
   ```

4. Configure your environment variables in a `.env` file in the project root:

   ```env
   DATABASE_URL=your_postgresql_connection_string
   ```

   Replace the placeholder with your actual PostgreSQL connection string. Never commit credentials or secrets.

5. Start the backend from the project root:

   ```powershell
   $env:PYTHONPATH = "backend"
   uvicorn app.main:app --reload
   ```

6. Open the API documentation:
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

### Running Tests

From the project root, with the virtual environment activated:

```powershell
$env:PYTHONPATH = "backend"
python -m pytest backend/tests -v
```

### Frontend Setup

Frontend setup instructions will be added when the React application is ready.

## Development Status

- [x] Set up the FastAPI backend
- [x] Configure PostgreSQL and SQLAlchemy
- [x] Implement user registration and login
- [x] Add JWT-based authentication
- [x] Create initial database models
- [ ] Complete course management APIs
- [ ] Add role-based authorization
- [ ] Build the React frontend
- [ ] Add comprehensive automated tests
- [ ] Write API usage and deployment documentation

## Project Goals

- Build a maintainable full-stack application.
- Practice backend development and database design.
- Improve API security and automated testing.
- Follow Git and GitHub best practices throughout development.

## API Endpoints

The backend exposes REST API endpoints for user authentication and application functionality.

| Method | Endpoint           | Purpose                        |
| ------ | ------------------ | ------------------------------ |
| GET    | `/`                | Check the API welcome response |
| POST   | `/register`        | Register a new user            |
| POST   | `/login`           | Authenticate a user            |
| GET    | Protected endpoint | Demonstrate JWT authentication |

_Refer to Swagger UI at `/docs` for the exact endpoint paths, request schemas, and response formats._

## Security Practices

Security is an important part of SkillTrack's development.

- Passwords are stored as hashes rather than plain text.
- JWT authentication is used to protect restricted endpoints.
- Environment variables are used for database configuration.
- Secret keys and database credentials should never be committed to Git.
- Input validation is handled using Pydantic schemas.

## Contribution Workflow

Contributions and suggestions are welcome.

1. Create a branch for your changes.
2. Make a focused improvement.
3. Run the relevant automated tests.
4. Use a descriptive Git commit message.
5. Submit a pull request with a clear explanation of your changes.

## License

This project is currently under development. A license will be added when one is selected.

## Author

**Kunal**

GitHub: [@Kunal0234](https://github.com/Kunal0234)
