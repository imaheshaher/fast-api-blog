from fastapi import FastAPI,HTTPException
from app.views import user,post
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.databases import engine,Base,SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_prefix="/api")

# Custom exception handler
async def custom_exception_handler(request, exc):
    status_code = 500
    detail = str(exc) or "Internal Server Error"

    # Handle FastAPI HTTPException
    if isinstance(exc, HTTPException):
        status_code = exc.status_code
        detail = exc.detail
    if isinstance(exc, StarletteHTTPException):
        status_code = exc.status_code
        detail = exc.detail

    return JSONResponse(
        status_code=status_code,
        content={"error": detail},
    )

# Add the custom exception handler
app.add_exception_handler(Exception, custom_exception_handler)

app.include_router(user.router)
app.include_router(post.router, tags=["posts"])
