from fastapi import FastAPI
from controllers.rec_controller import rec_router
app = FastAPI()

app.include_router(rec_router)