from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return "Welcome to Social Media API"






















# def find_post(id):
#     for p in my_posts:
#         if p['id'] == int(id):
#             return p
        
# def find_post_index(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == int(id):
#             return i
        
# while True:        
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='root', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Connection successful!!")
#         break

#     except Exception as error:
#         print("Connection failed")
#         print(f"Error: {error}")
#         time.sleep(3)


# my_posts = [{
#         "id": 1,
#         "title": "title of post 1",
#         "content": "content of post 1",
#         "rating": 3
#     },
#     {
#         "id": 2,
#         "title": "title of post 2",
#         "content": "content of post 2",
#         "rating": 4
#     }
# ]

# @app.get("/sqlalchemy")
# def test_post(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}






