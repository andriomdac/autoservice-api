from fastapi import FastAPI
from routes.payment_methods import payment_method_router
from routes.users import user_router
from routes.token import token_router
from routes.autoservice import autoservice_router
from routes.tenant import tenant_router
from routes.roles import role_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)
app.include_router(token_router)
app.include_router(autoservice_router)
app.include_router(payment_method_router)
app.include_router(tenant_router)
app.include_router(role_router)
