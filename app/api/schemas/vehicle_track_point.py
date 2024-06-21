from datetime import datetime
from typing import Any

from fastapi.exceptions import ValidationException
from geoalchemy2 import Geometry, elements
from pydantic import BaseModel, GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from typing_extensions import Annotated

from app.api.schemas.schema_mixin import SchemaMixin

# class ThirdPartyType:
#     """
#     This is meant to represent a type from a third-party library that wasn't designed with Pydantic
#     integration in mind, and so doesn't have a `pydantic_core.CoreSchema` or anything.
#     """

#     x: int

#     def __init__(self):
#         self.x = 0


class _GeometryTypePydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """
        We return a pydantic_core.CoreSchema that behaves in the following ways:

        * ints will be parsed as `ThirdPartyType` instances with the int as the x attribute
        * `ThirdPartyType` instances will be parsed as `ThirdPartyType` instances without any changes
        * Nothing else will pass validation
        * Serialization will always return just an int
        """

        def validate_from_literal(value: str) -> Geometry:
            result = Geometry(value)
            return result

        from_literal_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_literal),
            ]
        )

        def serializer(instance):
            from geoalchemy2.shape import to_shape

            if isinstance(instance, elements.WKBElement):
                return str(to_shape(instance))
            return elements.WKTElement(instance.geometry_type)

        return core_schema.json_or_python_schema(
            json_schema=from_literal_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(elements.WKBElement),
                    from_literal_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(serializer),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `int`
        return handler(core_schema.str_schema())


# We now create an `Annotated` wrapper that we'll use as the annotation for fields on `BaseModel`s, etc.
PydanticGeometryType = Annotated[Geometry, _GeometryTypePydanticAnnotation]


# # Create a model class that uses this annotation as a field
# class Model(BaseModel):
#     third_party_type: PydanticThirdPartyType


# # Demonstrate that this field is handled correctly, that ints are parsed into `ThirdPartyType`, and that
# # these instances are also "dumped" directly into ints as expected.
# m_int = Model(third_party_type=1)
# assert isinstance(m_int.third_party_type, ThirdPartyType)
# assert m_int.third_party_type.x == 1
# assert m_int.model_dump() == {'third_party_type': 1}

# # Do the same thing where an instance of ThirdPartyType is passed in
# instance = ThirdPartyType()
# assert instance.x == 0
# instance.x = 10

# m_instance = Model(third_party_type=instance)
# assert isinstance(m_instance.third_party_type, ThirdPartyType)
# assert m_instance.third_party_type.x == 10
# assert m_instance.model_dump() == {'third_party_type': 10}

# # Demonstrate that validation errors are raised as expected for invalid inputs
# try:
#     Model(third_party_type='a')
# except ValidationError as e:
#     print(e)
#     """
#     2 validation errors for Model
#     third_party_type.is-instance[ThirdPartyType]
#       Input should be an instance of ThirdPartyType [type=is_instance_of, input_value='a', input_type=str]
#     third_party_type.chain[int,function-plain[validate_from_int()]]
#       Input should be a valid integer,
#       unable to parse string as an integer [type=int_parsing, input_value='a', input_type=str]
#     """


# assert Model.model_json_schema() == {
#     'properties': {
#         'third_party_type': {'title': 'Third Party Type', 'type': 'integer'}
#     },
#     'required': ['third_party_type'],
#     'title': 'Model',
#     'type': 'object',
# }


class VehicleCreateTrackPointGeo(BaseModel):
    date_time: datetime
    geotag: PydanticGeometryType
    vehicle_id: int

    class Config:
        from_attributes = True


class VehicleCreateTrackPoint(BaseModel):
    date_time: datetime
    long: float
    lat: float
    vehicle_id: int

    class Config:
        from_attributes = True


class VehicleTrackPoint(VehicleCreateTrackPoint):
    id: int

    class Config:
        from_attributes = False


class VehicleTrackPointGeoJSON(BaseModel):
    id: int
    date_time: datetime
    geometry: dict
    vehicle_id: int

    class Config:
        from_attributes = False


class VehicleTrackPointGeoFromDB(BaseModel, SchemaMixin):
    id: int
    date_time: datetime
    geotag: PydanticGeometryType
    vehicle_id: int

    class Config:
        from_attributes = True

    @classmethod
    def model_validate_datetime_with_tz(cls, obj, tz="UTC"):
        obj = cls.set_user_timezone_to_datetime_fields(obj, tz)

        return cls.model_validate(obj)


def from_geo_point_to_lat_long(track_point, *, tz="UTC"):
    tp_json = VehicleTrackPointGeoFromDB.model_validate_datetime_with_tz(track_point, tz).model_dump()
    match tp_json["geotag"].replace("(", "").replace(")", "").split():
        case ["POINT", long, lat] if long is not None and lat is not None:
            pass
        case _:
            raise ValidationException({"geom": "Wrong data of POINT type"})
    tp = VehicleTrackPoint(
        id=tp_json["id"],
        date_time=tp_json["date_time"],
        long=long,
        lat=lat,
        vehicle_id=tp_json["vehicle_id"],
    )
    return tp


def from_geo_point_to_geojson(track_point, *, tz="UTC"):
    from geojson import Point

    tp_json = VehicleTrackPointGeoFromDB.model_validate_datetime_with_tz(track_point, tz).model_dump()
    match tp_json["geotag"].replace("(", "").replace(")", "").split():
        case ["POINT", long, lat] if long is not None and lat is not None:
            point = Point((float(long), float(lat)))
        case _:
            raise ValidationException({"geom": "Wrong data of POINT type"})
    tp = VehicleTrackPointGeoJSON(
        id=tp_json["id"],
        date_time=tp_json["date_time"],
        geometry=point,
        vehicle_id=tp_json["vehicle_id"],
    )
    return tp
