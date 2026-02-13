from fastapi import FastAPI

# from product.product_api import router
# from product_adv.routers.product_router import router as product_router
from product_db.routers.product_router import router as product_db_router
from product_db.routers.category_router import router as category_db_router
from product_db.routers.user_router import router as user_db_router
from product_db.routers.user_router2 import router as user_db_router2
from product_db.routers.auth_router import router as auth_router

from database import engine
from product_db import models


# models.Base.metadata.drop_all(bind=engine)

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(product_db_router)
app.include_router(category_db_router)
app.include_router(user_db_router)
app.include_router(user_db_router2)
app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"Hello": "asd"}
