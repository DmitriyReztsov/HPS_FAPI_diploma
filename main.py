import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from app.admin.driver_admin import DriverAdmin, DriverVehicleAdmin
from app.admin.enterprise_admin import EnterpriseAdmin
from app.admin.user_admin import UserAdmin
from app.admin.vehicle_admin import VehicleAdmin, VehicleBrandAdmin, VehicleModelAdmin, VehicleTrackPointAdmin
from app.api.endpoints import (
    driver_router,
    enterprise_router,
    user_router,
    vehicle_brand_router,
    vehicle_model_router,
    vehicle_router,
    vehicle_track_point_router,
    trip_router,
)
from app.db.database import engine

app = FastAPI()
admin = Admin(app, engine)
admin.add_view(UserAdmin)
admin.add_view(VehicleAdmin)
admin.add_view(VehicleBrandAdmin)
admin.add_view(VehicleModelAdmin)
admin.add_view(VehicleTrackPointAdmin)
admin.add_view(DriverAdmin)
admin.add_view(EnterpriseAdmin)
admin.add_view(DriverVehicleAdmin)

app.include_router(vehicle_router)
app.include_router(trip_router)
app.include_router(vehicle_brand_router)
app.include_router(vehicle_model_router)
app.include_router(vehicle_track_point_router)
app.include_router(driver_router)
app.include_router(enterprise_router)
app.include_router(user_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Timezone setting for server
SERVER_TIME_ZONE = "UTC"

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
    )
