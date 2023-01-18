import inquirer
import re
from config.DB import db, users, connection


def email_validate(answer, current):
    query = db.select([users]).where(
        users.columns.email == current)

    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", current):
        raise inquirer.errors.ValidationError(
            "",
            reason="Email is not valid"
        )

    elif connection.execute(query).fetchone() is not None:
        raise inquirer.errors.ValidationError(
            "",
            reason="Email already exists"
        )

    return True


def password_validate(answer, current):
    if len(current) < 8:
        raise inquirer.errors.ValidationError(
            "",
            reason="Password min length is 8"
        )

    return True


def password_confirm_validate(answers, current):
    if current != answers["password"]:
        raise inquirer.errors.ValidationError(
            "",
            reason="Password does not match",
        )

    return True
