import uvicorn
from fastapi import FastAPI
from sqladmin import Admin

from app.admin.vehicle_admin import VehicleAdmin, VehicleBrandAdmin, VehicleModelAdmin
from app.api.endpoints import vehicle_brand_router, vehicle_model_router, vehicle_router
from app.db.database import engine

app = FastAPI()
admin = Admin(app, engine)
admin.add_view(VehicleAdmin)
admin.add_view(VehicleBrandAdmin)
admin.add_view(VehicleModelAdmin)

app.include_router(vehicle_router)
app.include_router(vehicle_brand_router)
app.include_router(vehicle_model_router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
    )
