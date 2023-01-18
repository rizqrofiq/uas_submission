import inquirer
import os
from validation.main import recruiter_option_validate
from services.jobs import job_ad_main
from services.applicants import applicants_main


def recruiter_page():
    while True:
        os.system("clear")  # use os.system("cls") on Windows
        print("You're logged in as a recruiter")
        print(
            "Here are the options you can choose before using features that we've provided as a recruiter:\n")
        print("[1]. Job Advertising")
        print("[2]. Job Applicants")
        print("[3]. Logout\n")

        choice = inquirer.prompt([
            inquirer.Text("option", message="What do you want to do?",
                          validate=recruiter_option_validate)
        ])

        if choice['option'] == '3':
            print('You have been logged out')
            return
        elif choice['option'] == '1':
            job_ad_main()
        elif choice['option'] == '2':
            applicants_main()

        input("Press any key to continue...")
