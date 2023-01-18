import os
import inquirer
import prettytable
from config.DB import db, jobs, connection
from session import session


def job_ad_main():
    while True:
        os.system("clear")  # use os.system("cls") for windows
        print("|++++++++++++++++ Job Advertising ++++++++++++++++++|")
        print("| Here are the options you can choose               |")
        print("| [1]. Post a job                                   |")
        print("| [2]. View job                                     |")
        print("| [3]. Update existing job                          |")
        print("| [4]. Delete job                                   |")
        print("| [5]. Back to main menu                            |")
        print("|+++++++++++++++++++++++++++++++++++++++++++++++++++|")

        choice = inquirer.prompt([
            inquirer.Text("option", message="What do you want to do?")
        ])

        if choice['option'] == '5':
            return
        elif choice['option'] == '1':
            create_job_ad()
        elif choice['option'] == '2':
            show_jobs()
        elif choice['option'] == '3':
            update_job()
        elif choice['option'] == '4':
            delete_job()

        input("\nPress any key to continue...")


def create_job_ad():
    print("\nPost a new job\n")

    forms = inquirer.prompt([
        inquirer.Text("company", message="Company name"),
        inquirer.Text("position", message="Position"),
        inquirer.Text("description", message="Description"),
        inquirer.Text("yoe", message="Minimum years of experience(min: 0)"),
        inquirer.Text("salary", message="Salary"),
    ])

    query = db.insert(jobs).values(
        company=forms['company'], position=forms['position'], description=forms['description'], years_of_experience=forms['yoe'], salary=forms['salary'], recruiter_id=session.user[0])

    result = connection.execute(query)
    print("\nJob has been posted successfully")


def show_jobs():
    print("\nHere are the jobs that you have posted\n")
    table = prettytable.PrettyTable()

    table.align = "l"
    table.field_names = ["No", "ID JP", "Company",
                         "Position", "Description", "Min YOE", "Salary", "Applicants", "Status", "Created At"]

    query = db.select([jobs]).where(
        jobs.columns.recruiter_id == session.user[0])
    result = connection.execute(query).fetchall()

    for i, row in enumerate(result):
        date = row[9].strftime("%d-%m-%Y")
        table.add_row([i+1, row[0], row[1], row[2],
                      row[3][:12] + "..." if len(row[3]) >= 15 else row[3], row[4], row[5], row[6], row[8], date])

    print(table)


def update_job():
    print("\nUpdate an existing job\n")

    form = inquirer.prompt([
        inquirer.Text("id", message="Enter the Job ID")
    ])

    query = db.select([jobs]).where(jobs.columns.id == form['id']
                                    and jobs.columns.recruiter_id == session.user[0])
    result = connection.execute(query).fetchone()

    if result is None:
        print("\nJob not found")
        return

    forms = inquirer.prompt([
        inquirer.Text("company", message="Company name", default=result[1]),
        inquirer.Text("position", message="Position", default=result[2]),
        inquirer.Text("description", message="Description", default=result[3]),
        inquirer.Text(
            "yoe", message="Minimum years of experience(min: 0)", default=result[4]),
        inquirer.Text("salary", message="Salary", default=result[5]),
        inquirer.List("status", message="Status", choices=[
                      'open', 'closed'], default=result[7])
    ])

    query = db.update(jobs).values(company=forms['company'], position=forms['position'], description=forms['description'],
                                   years_of_experience=forms['yoe'], salary=forms['salary'], status=forms['status']).where(jobs.columns.id == form['id'])
    result = connection.execute(query)

    print("\nJob has been updated successfully")


def delete_job():
    print("\nDelete a job\n")

    form = inquirer.prompt([
        inquirer.Text("id", message="Enter the Job ID")
    ])

    query = db.select([jobs]).where(jobs.columns.id == form['id']
                                    and jobs.columns.recruiter_id == session.user[0])
    result = connection.execute(query).fetchone()

    if result is None:
        print("\nJob not found")
        return

    query = db.delete(jobs).where(jobs.columns.id == form['id'])
    result = connection.execute(query)

    print("\nJob has been deleted successfully")
