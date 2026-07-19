from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
import sqlite3
import sys


# -----------------------------\
# 1. LOAD UI


app = QtWidgets.QApplication(sys.argv)
window = uic.loadUi("registration.ui")   


# ----------------------------\
# 2. CREATE DATABASE

con = sqlite3.connect("users.db")
cur = con.cursor()

cur.execute("""
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
""")
con.commit()


# -----------------------------\
# 3. REGISTER FUNCTION


def register_user():

    firstname = window.input_firstname.text()
    lastname = window.input_lastname.text()
    email = window.input_email.text()
    username = window.input_username.text()
    password = window.input_password.text()
    confirm  = window.input_confirm.text()
    phone    = window.input_phone.text()
    gender   = window.combo_gender.currentText()
    dob      = window.date_dob.text()
    address  = window.input_address.toPlainText()

    # ---- Required Fields Check ----\

    if firstname == "" or lastname == "" or email == "" or username == "" or password == "":
        QMessageBox.warning(window, "Error", "Please fill all required fields!")
        return
    
    if password != confirm:
        QMessageBox.warning(window, "Error", "Passwords do not match!")
        return

    try:
        cur.execute("""
            INSERT INTO users
            (firstname, lastname, email, username, password, phone, gender, dob, address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (firstname, lastname, email, username, password, phone, gender, dob, address))

        con.commit()

        QMessageBox.information(window, "Success", "User Registered Successfully!")
        clear_fields()

    except sqlite3.IntegrityError:
        QMessageBox.critical(window, "Error", "Username or Email already exists!")


# -----------------------------\
# 4. CLEAR FIELDS

def clear_fields():
    window.input_firstname.clear()
    window.input_lastname.clear()
    window.input_email.clear()
    window.input_username.clear()
    window.input_password.clear()
    window.input_confirm.clear()
    window.input_phone.clear()
    window.input_address.clear()
    window.combo_gender.setCurrentIndex(0)


# -----------------------------\
# 5. BUTTON CONNECTIONS

window.btn_register.clicked.connect(register_user)
window.btn_clear.clicked.connect(clear_fields)


# -----------------------------\
# 6. SHOW WINDOW

window.show()
sys.exit(app.exec_())
