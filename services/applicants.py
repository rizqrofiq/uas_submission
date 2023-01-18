import os
import inquirer
import prettytable
from config.DB import db, users, job_applications, jobs, connection
from session import session


def applicants_main():
    while True:
        os.system("clear")
        print("|++++++++++++++++++ Job Applicants +++++++++++++++++|")
        print("| Here are the options you can choose               |")
        print("| [1]. Show applicants                              |")
        print("| [2]. Change applicants application status         |")
        print("| [3]. Delete applicants                            |")
        print("| [4]. Back to main menu                            |")
        print("|+++++++++++++++++++++++++++++++++++++++++++++++++++|")

        choice = inquirer.prompt([
            inquirer.Text("option", message="What do you want to do?")
        ])

        if choice['option'] == '4':
            return
        elif choice['option'] == '1':
            show_applicants()
        elif choice['option'] == '2':
            change_applicants_status()
        elif choice['option'] == '3':
            delete_applicants()

        input("\nPress any key to continue...")


def show_applicants():
    print("\nHere are the applicants for jobs that you have posted\n")
    table = prettytable.PrettyTable()

    table.align = "l"
    table.field_names = ["No.", "Name", "Email", "Job Title", "Status"]

    query = db.select([users.columns.id, users.columns.name, users.columns.email, jobs.columns.position, job_applications.columns.status]).where(
        job_applications.columns.employee_id == users.columns.id).where(job_applications.columns.job_id == jobs.columns.id).where(jobs.columns.recruiter_id == session.user[0])

    result = connection.execute(query).fetchall()
    # print(result)

    for i, row in enumerate(result):
        table.add_row([i+1, row[1], row[2], row[3], row[4]])

    print(table)


def change_applicants_status():
    print("\nHere are the applicants for jobs that you have posted\n")
    query = db.select([users.columns.id, users.columns.name, users.columns.email, jobs.columns.position, job_applications.columns.status, job_applications.columns.id]).where(
        job_applications.columns.employee_id == users.columns.id).where(job_applications.columns.job_id == jobs.columns.id).where(jobs.columns.recruiter_id == session.user[0])

    result = connection.execute(query).fetchall()

    choices = []
    for row in result:
        choices.append((f"{row[1]} for {row[3]}", row[5]))

    choice = inquirer.prompt([
        inquirer.List(
            "option", message="Choose the applicant you want to change the status", choices=choices)
    ])

    status = inquirer.prompt([
        inquirer.List("option", message="Choose the status",
                      choices=["Accepted", "Rejected"])
    ])

    query = db.update(job_applications).values(status=status['option']).where(
        job_applications.columns.id == choice['option'])
    connection.execute(query)

    print("Applicant status has been changed")


def delete_applicants():
    print("\nHere are the applicants for jobs that you have posted\n")
    query = db.select([users.columns.id, users.columns.name, users.columns.email, jobs.columns.position, job_applications.columns.status, job_applications.columns.id]).where(
        job_applications.columns.employee_id == users.columns.id).where(job_applications.columns.job_id == jobs.columns.id).where(jobs.columns.recruiter_id == session.user[0])

    result = connection.execute(query).fetchall()

    choices = []
    for row in result:
        choices.append((f"{row[1]} for {row[3]}", row[5]))

    choice = inquirer.prompt([
        inquirer.List(
            "option", message="Choose the applicant you want to delete", choices=choices)
    ])

    query = db.delete(job_applications).where(
        job_applications.columns.id == choice['option'])
    connection.execute(query)

    print("Applicant has been deleted")
