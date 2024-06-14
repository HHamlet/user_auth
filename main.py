from typing import Annotated
from fastapi import FastAPI, Request, HTTPException, status, Depends
import uvicorn
from sqlalchemy.orm import Session
import views
from auth import get_current_user
from database import get_db
from models import User

app = FastAPI()
app.include_router(views.router)

user_dependency = Annotated[dict, Depends(get_current_user)]


@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    db: Session = get_db()
    if request.url.path.startswith("/auth"):
        return await call_next(request)
    api_kay = request.headers.get("x-api-kay")
    if not api_kay:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key missing")
    user = db.query(User).where(User.api_key == api_kay).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    response = await call_next(request)
    return response


@app.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
