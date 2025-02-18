from fastapi import FastAPI
from controllers.rec_controller import rec_router
from controllers.user_controller import user_router
app = FastAPI()

app.include_router(rec_router)
app.include_router(user_router)