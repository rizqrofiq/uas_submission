import inquirer
import os
import locale
from config.DB import db, connection, users, jobs, job_applications
from prettytable import PrettyTable
from session import session

locale.setlocale(locale.LC_ALL, 'id_ID.utf8')


def employe_page():
    while True:
        os.system("clear")  # use os.system("cls") for windows
        print("You're logged in as a employee")
        print(
            "Here are the options you can choose before using features that we've provided:\n")
        print("[1]. Job list")
        print("[2]. Apply for a job")
        print("[3]. View your application")
        print("[4]. Logout\n")

        choice = inquirer.prompt([
            inquirer.Text('option', message="What do you want to do?")
        ])

        if choice['option'] == '4':
            print("You have been logged out")
            return
        elif choice['option'] == '1':
            job_list()
        elif choice['option'] == '2':
            apply()
        elif choice['option'] == '3':
            view_application()

        input("Press any key to continue ...")


def job_list():
    print("Job list")
    print("Here are the jobs that you can apply for:\n")

    query = db.select([jobs, users.columns.name]).where(jobs.columns.status == 'open').join(
        users, jobs.columns.recruiter_id == users.columns.id)
    result = connection.execute(query).fetchall()

    table = PrettyTable()
    table.field_names = ["No.", "Job Title", "Company",
                         "Recruiter Name", "Applicants", "Min. YOE"]
    table.align = "l"

    for i, row in enumerate(result):
        table.add_row([i+1, row[2], row[1], row[10], row[6], row[4]])

    print(table)


def apply():
    print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++|")
    print("|                  Apply for a job                   |")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++|\n")
    query = db.select([jobs])
    result = connection.execute(query).fetchall()

    list_job = []
    for row in result:
        list_job.append((f"{row[2]} at {row[1]}", row[0]))

    choice = inquirer.prompt([
        inquirer.List(
            'option', message="Which job do you want to apply for?", choices=list_job)
    ])

    query = db.select([jobs, users.columns.name]).where(
        jobs.columns.id == choice['option']).join(users, jobs.columns.recruiter_id == users.columns.id)
    result = connection.execute(query).fetchone()

    print("\nHere are the details of the job you want to apply for:")
    print("=====================================================")
    print(f"Job Title \t\t :{result[2]}")
    print(f"Job Description \t :{result[3]}")
    print(f"Company \t\t :{result[1]}")
    print(f"Recruiter Name \t\t :{result[10]}")
    print(f"Applicants \t\t :{result[6]}")
    print(f"Minimum experiences \t :{result[4]}years")
    print(f"Salary \t\t\t :{locale.currency(result[5], grouping=True)}")
    print("=====================================================")

    confirm = inquirer.prompt([
        inquirer.Confirm(
            'option', message="Do you want to apply for this job?")
    ])

    if confirm['option'] == True:
        query = db.update(jobs).where(jobs.columns.id == choice['option']).values(
            applicants=jobs.columns.applicants+1)
        connection.execute(query)

        query = db.insert(job_applications).values(
            employee_id=session.user[0], job_id=choice['option'])
        connection.execute(query)

        print("\nYou have successfully applied for this job")
        print("If you are selected, you will be notified via email")
        print("You can check your application status in the View your application menu\n")
    else:
        print("You have canceled the application")


def view_application():
    print("\nView your application")
    print("Here are the jobs that you have applied for:\n")

    # query = db.select([jobs, job_applications.columns.status]).where(job_applications.columns.employee_id == session.user[0]).join(
    #     job_applications, jobs.columns.id == job_applications.columns.job_id)
    # result = connection.execute(query).fetchall()

    query = db.select([job_applications, users.columns.name, jobs.columns.company, jobs.columns.position]).where(job_applications.columns.employee_id == session.user[0]).join(users, jobs.columns.recruiter_id ==
                                                                                                                                                                               users.columns.id).join(job_applications,  jobs.columns.id == job_applications.columns.job_id)
    result = connection.execute(query).fetchall()

    # print(result)
    table = PrettyTable()
    table.field_names = ["No.", "Job Title", "Company",
                         "Recruiter Name", "Status"]
    table.align = "l"

    for i, row in enumerate(result):
        table.add_row([i+1, row[7], row[6], row[5],  row[3]])

    print(table)
