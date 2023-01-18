import pyfiglet
import os
import inquirer
from validation.main import main_validate
from session import session
from services.auth import register, login
from pages.employee import employe_page
from pages.recruiter import recruiter_page
from config.DB import db, users, connection


def main():
    loginState = False

    while True:
        os.system("clear")  # use os.system("cls") on windows
        if loginState == False:
            print(pyfiglet.figlet_format("Recr. Portal"))
            print("Welcome to the Recruitment Portal")
            print("Here you can apply for a job or you can post a job\n")
            print(
                "Here are the options you can choose before using features that we've provided:")
            print("[1]. Login")
            print("[2]. Register")
            print("[3]. Exit\n")

            choice = inquirer.prompt([
                inquirer.Text('option', message="What do you want to do?",
                              validate=main_validate),
            ])

            if choice['option'] == '1':
                user = login()
                if user is not None:
                    loginState = True
                    session.set(user)
                else:
                    print("Login failed")

            elif choice['option'] == '2':
                prompt = register()
                if prompt is not None:
                    if prompt['state'] == "login":
                        user = login()
                        if user is not None:
                            loginState = True
                            session.set(user)
                        else:
                            print("Login failed")

            elif choice["option"] == '3':
                print("Thank you for using our service. Bye!")
                return
        else:
            print(pyfiglet.figlet_format("Recr. Portal"))
            print(f"Hello {session.user[1]}, welcome back!\n")
            if session.user[4] == "employee":
                print("You are logged in as employee")
                employe_page()
                loginState = False
                session.clear()
            else:
                print("You are logged in as recruiter")
                recruiter_page()
                loginState = False
                session.clear()

        input("Press any key to continue ...")


if __name__ == "__main__":
    main()
