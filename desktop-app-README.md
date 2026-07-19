# User Registration Desktop App (PyQt5)

A desktop GUI application built with **PyQt5** that registers new users into a local **SQLite** database. The interface is designed separately in Qt Designer (`registration.ui`) and loaded dynamically at runtime — no hand-written GUI layout code.

## What it does

- Displays a registration form (First Name, Last Name, Email, Username, Password, Confirm Password, Phone, Gender, Date of Birth, Address).
- On **Register**, validates the input, then inserts the new user into a local `users.db` SQLite database.
- On **Clear**, resets every field back to empty/default.

## Validation & Data Handling

- **Required fields** — First Name, Last Name, Email, Username, and Password must all be filled, or registration is blocked with a warning dialog.
- **Password confirmation** — Password and Confirm Password must match, or registration is blocked.
- **Duplicate prevention** — `email` and `username` are both `UNIQUE` constraints at the database level; attempting to register an existing one raises `sqlite3.IntegrityError`, which is caught and shown as an error dialog instead of crashing the app.
- **Auto schema creation** — the `users` table is created automatically on first run via `CREATE TABLE IF NOT EXISTS`, so there's no separate DB setup step.

## Tech Stack

- **PyQt5** — GUI framework (`QtWidgets`, `uic` for loading the `.ui` file at runtime)
- **SQLite3** (Python standard library) — local file-based database, no server required
- **Qt Designer** — used to build `registration.ui` (drag-and-drop form layout, not hand-coded)

## Project Structure

```
desktop_application/
├── main.py            - App entry point: loads UI, wires up buttons, handles registration logic
├── registration.ui     - Qt Designer form definition (loaded at runtime via uic.loadUi)
├── users.db             - SQLite database (auto-created if missing; ships with sample/existing data)
└── demo-vid-link.txt     - Link to a demo video of the app in action
```

## How to Run

```bash
pip install PyQt5
python main.py
```

The app window will open directly to the registration form. `users.db` is created in the same directory if it doesn't already exist.

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT,
    lastname TEXT,
    email TEXT UNIQUE,
    username TEXT UNIQUE,
    password TEXT,
    phone TEXT,
    gender TEXT,
    dob TEXT,
    address TEXT
)
```

## Known Limitations

- Passwords are stored in **plain text** — fine for a learning/demo project, but worth mentioning if asked: a real system would hash passwords (e.g. with `bcrypt`) before storing them.
- No login/authentication screen — this project only covers registration, not sign-in.
- No input format validation on email or phone (e.g. regex checks) beyond the required-field and password-match checks.

## Possible Extensions

- Add a login screen that checks entered credentials against the `users` table.
- Hash passwords before storing (`bcrypt` or `hashlib`).
- Add email/phone format validation with regex.
- Add an "edit profile" or "view all users" screen (would double as a second CRUD demo alongside this one).
