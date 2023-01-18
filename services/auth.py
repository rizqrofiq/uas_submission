import inquirer
import bcrypt
import os
from helper.validation import email_validate, password_validate, password_confirm_validate
from validation.main import login_email_validate
from config.DB import db, users, connection


def login():
    print("\n")
    print("|=========================================|")
    print("|                 Log in                  |")
    print("|=========================================|")

    while True:

        forms = inquirer.prompt([
            inquirer.Text("email", message="Email",
                          validate=login_email_validate),
            inquirer.Password("password", message="Password")
        ])

        query = db.select([users]).where(users.columns.email == forms["email"])
        user = connection.execute(query).fetchone()

        if user is None:
            print("Login failed: User with provided email doesn't exist")
            retryConfirm = inquirer.prompt([
                inquirer.Confirm("retry", message="Retry?")
            ])

            if retryConfirm["retry"] == False:
                return

            continue

        if bcrypt.checkpw(forms["password"].encode("utf-8"), user[3].encode("utf-8")):
            print("Logged in")
            return user
        else:
            print("Login failed: Password is incorrect")
            retryConfirm = inquirer.prompt([
                inquirer.Confirm("retry", message="Retry?")
            ])

            if retryConfirm["retry"] == False:
                print("Login aborted")
                return

            continue


def register():
    print("\n")
    print("|=========================================|")
    print("|                 Sign up                 |")
    print("|=========================================|")

    fields = [
        inquirer.Text("name", message="Full name"),
        inquirer.Text("email", message="Email",
                      validate=email_validate),
        inquirer.Password("password", message="Password",
                          validate=password_validate),
        inquirer.Password("confirm-password", message="Confirm Password",
                          validate=password_confirm_validate),
        inquirer.List('role', message="What is your role?",
                      choices=['employee', 'recruiter'])
    ]

    forms = inquirer.prompt(fields)

    encoded_password = forms["password"].encode('utf-8')
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt(10))

    query = db.insert(users).values(
        name=forms['name'], email=forms['email'], password=hashed_password, roles=forms['role'])

    transactions = connection.execute(query)

    choice = inquirer.prompt([
        inquirer.Confirm(
            "login", message="You have successfully registered, do you want to login now?", default=True)
    ])

    if choice['login'] == True:
        return {
            "state": "login"
        }

    return
