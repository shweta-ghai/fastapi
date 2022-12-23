from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import sys
# from pathlib import Path
# file = Path("app\models.py").resolve()
# package_root_directory = file.parents[0]
# sys.path.append(str(package_root_directory))

from .models import Base
from .database import engine
#import routers.post,routers.user,routers.auth,routers.vote
from .routers import post, user, auth, vote

Base.metadata.create_all(bind = engine)

app = FastAPI()

# while True:
#     try:
#         con = psycopg2.connect(database="fastapi", user="postgres", password="admin", host="localhost", port="5432",cursor_factory=RealDictCursor)

#         print("Database opened successfully")

#         cur = con.cursor()
#         # cur.execute('''CREATE TABLE STUDENT
#         #     (ADMISSION INT PRIMARY KEY     NOT NULL,
#         #     NAME           TEXT    NOT NULL,
#         #     AGE            INT     NOT NULL,
#         #     COURSE        CHAR(50),
#         #     DEPARTMENT        CHAR(50));''')

#         # print("Table created successfully")

#         # con.commit()
#         # con.close()
#         break
#     except Exception as error:
#         print(error)
#         time.sleep(2)



origins = ["*"]

#origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Hello World pushing out to ubantu"}

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(database.get_db)):

#     posts = db.query(models.Post).all()
#     return {"status":posts}




