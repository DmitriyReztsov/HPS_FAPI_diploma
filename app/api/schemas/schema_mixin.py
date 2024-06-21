from datetime import datetime

from pytz import timezone


class SchemaMixin:
    @staticmethod
    def set_user_timezone_to_datetime_fields(obj, tz="UTC"):
        from main import SERVER_TIME_ZONE

        for field, value in obj.__dict__.items():
            match value:
                case datetime(tzinfo=tzinfo) if tzinfo is None:
                    new_value = value.replace(tzinfo=timezone(SERVER_TIME_ZONE))
                case datetime(tzinfo=tzinfo) if tzinfo is not None:
                    new_value = value.astimezone(tz=timezone(tz))
                case _:
                    continue
            setattr(obj, field, new_value)
        return obj

    def model_dump_with_tz_align(self, tz="UTC", **kwargs):
        from main import SERVER_TIME_ZONE

        for field, value in self.__dict__.items():
            match value:
                case datetime(tzinfo=tzinfo) if tzinfo is None:
                    value_with_tz = value.replace(tzinfo=timezone(tz))
                    new_value = value_with_tz.astimezone(tz=timezone(SERVER_TIME_ZONE))
                case datetime(tzinfo=tzinfo) if tzinfo is not None:
                    new_value = value.astimezone(tz=timezone(SERVER_TIME_ZONE))
                case _:
                    continue

            setattr(self, field, new_value)
        return self.model_dump(**kwargs)
