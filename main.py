import uvicorn
from fastapi import FastAPI
from sqladmin import Admin

from app.admin.vehicle_admin import VehicleAdmin
from app.api.endpoints.vehicle import vehicle_router
from app.db.database import engine

app = FastAPI()
admin = Admin(app, engine)
admin.add_view(VehicleAdmin)

app.include_router(vehicle_router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
    )
