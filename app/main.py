
# Project imports
from app.routes.passengers import router as passenger_router
from app.config import get_data_source

# Lib imports
from fastapi import FastAPI

app = FastAPI(title="Titanic Web Service")

# Inject correct datasource on startup
@app.on_event("startup")
async def startup_event():
    ds = await get_data_source()
    app.state.datasource = ds

# Routes
app.include_router(passenger_router)

if __name__ == '__main__':
    pass