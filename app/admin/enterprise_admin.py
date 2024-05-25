from sqladmin import ModelView

from app.db.models import Enterprise


class EnterpriseAdmin(ModelView, model=Enterprise):
    column_labels = {Enterprise.id: "Company id", Enterprise.company_name: "Company name"}
    column_list = [Enterprise.id, Enterprise.company_name]
    column_details_list = (
        "id",
        "company_timezone",
        "company_name",
        "vehicles",
        "drivers",
        "company_address",
        "contact_email",
        "users",
    )
    form_excluded_columns = ("vehicles", "drivers", "users")
