from fastapi import FastAPI
from routes.payment_methods import payment_method_router
from routes.payment_values import payment_value_router
from routes.users import user_router
from routes.token import token_router
from routes.autoservice import autoservice_router


app = FastAPI()
app.include_router(user_router)
app.include_router(token_router)
app.include_router(autoservice_router)
app.include_router(payment_value_router)
app.include_router(payment_method_router)


@app.get("/")
def root():
    return {"success": "Hello, World!"}
