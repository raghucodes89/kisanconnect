from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, farmers, crops, weather, marketplace, labour
import traceback

app = FastAPI(
    title="KisanConnect API",
    description="AgriTech platform for Indian farmers",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def catch_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(farmers.router, prefix="/farmers", tags=["Farmers"])
app.include_router(crops.router, prefix="/crops", tags=["Crops"])
app.include_router(weather.router, prefix="/weather", tags=["Weather"])
app.include_router(marketplace.router, prefix="/marketplace", tags=["Marketplace"])
app.include_router(labour.router, prefix="/labour", tags=["Labour"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Welcome to KisanConnect API"}