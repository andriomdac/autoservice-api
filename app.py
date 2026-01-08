from fastapi import FastAPI
from routes.users import user_router
from routes.token import token_router
from routes.autoservice import autoservice_router


app = FastAPI()
app.include_router(user_router)
app.include_router(token_router)
app.include_router(autoservice_router)


@app.get("/")
def root():
    return {"success": "Hello, World!"}
