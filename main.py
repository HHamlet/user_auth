from typing import Annotated
from fastapi import FastAPI, HTTPException, status, Depends
import uvicorn
import views
from auth import get_current_user

app = FastAPI()
app.include_router(views.router)

user_dependency = Annotated[dict, Depends(get_current_user)]


@app.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
