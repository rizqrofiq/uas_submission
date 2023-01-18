import inquirer
import re


def main_validate(answers, current):
    if current not in ('1', '2', '3'):
        raise inquirer.errors.ValidationError(
            '',
            reason='Please enter a valid option',
        )

    return True


def employee_option_validate(answers, current):
    if current not in ('1', '2', '3', '4', '5', '6'):
        raise inquirer.errors.ValidationError(
            '',
            reason='Please enter a valid option',
        )

    return True


def recruiter_option_validate(answers, current):
    if current not in ('1', '2', '3'):
        raise inquirer.errors.ValidationError(
            '',
            reason='Please enter a valid option',
        )

    return True


def login_email_validate(answers, current):
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", current):
        raise inquirer.errors.ValidationError(
            '',
            reason='Please enter a valid email',
        )

    return True
