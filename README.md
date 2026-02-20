# proof
modular jwt auth for flask so you don't have to worry about login

## what is it
a plug-and-play authentication system for flask apps that uses jwts. fast game. modular so you can drop it into your
project as-is

---
## features
- modular structure - routes/services/models separation
- jwt-based auth - stateless token verification (no server-side sessions required)
- security-focused defaults - password hashing, input validation patterns, clear error handling
- flask-native - uses blueprints + app factory
---

## project structure
This project follows a layered Flask app-factory structure for clean separation of concerns:

- `routes/`    → HTTP endpoints only (request parsing, response formatting)
- `services/`  → Business logic (validation, workflows, database actions)
- `models/`    → Database schema (SQLAlchemy models)
- `extensions/`→ Flask extension initialization (SQLAlchemy, Bcrypt, etc.)
- `instance/`  → Runtime data (local SQLite database), not committed to Git

```structure
.
├── run.py
├── requirements.txt
├── .env
├── .env.example
├── instance/
│   └── dev.db
└── app/
    ├── __init__.py
    ├── config.py
    ├── extensions.py
    ├── models/
    │   ├── __init__.py
    │   └── user.py
    ├── routes/
    │   ├── __init__.py
    │   ├── auth.py
    │   └── common.py
    ├── services/
    │   ├── __init__.py
    │   └── auth_service.py
    ├── templates/
    │   └── auth/
    │       └── register.html
    └── static/
```
---

## how to set it up
### 1. Set up the virtual environment
```bash
python -m venv venv
venv\Scripts\Activate
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Configure environment variables
Create a `.env` file or copy from .env.example
```bash
copy .env.example .env
```
Set at least:
- SECRET_KEY
- JWT_SECRET_KEY
### 4. Run the App
```bash
python run.py
```

---
## contribute
let me know if your thoughts!