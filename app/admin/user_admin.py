from sqladmin import ModelView

from app.db.models import User


class UserAdmin(ModelView, model=User):
    column_labels = {
        User.id: "User id",
        User.first_name: "First name",
        User.last_name: "Last name",
        User.get_full_name: "User full name",
        User.enterprises: "Enterprises",
    }
    column_list = [User.id, User.get_full_name]
    column_details_list = (
        "id",
        "username",
        "password",
        "first_name",
        "last_name",
        "enterprises",
        "drivers",
    )
