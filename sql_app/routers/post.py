from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])
# testing endpoint - passing dependency from database.py
# @router.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()  # use query() method to get data from database
#     print(posts)
#     return {"data": "successful"}


# retrieve all posts from postgres database
# @router.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts """)
#     posts = cursor.fetchall()
#     return {"data": posts}


# retrieve all posts from postgres database using SQLalchemy
# current_user code - allow Login user to use this function
# limit, skip, search - is used for query parameters
# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # Allow users to see all users' posts
    # SELECT posts.*, COUNT(votes.post_id) AS votes FROM posts LEFT JOIN votes ON posts.id=votes.post_id GROUP BY posts.id;
    # filter == WHERE (SQL)
    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(search))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )

    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    # print(posts)

    # Allow users to see only their own posts
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts


# INSERT data into posts database using SQL syntax
# @router.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: schemas.Post):
#     cursor.execute(
#         """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
#         (post.title, post.content, post.published),
#     )
#     new_post = cursor.fetchone()  # get the new post after executing
#     conn.commit()  # used whenever something change in the database
#     return {"data": new_post}  # send back latest posts


# INSERT data into posts database using SQLalchemy syntax
# current_user code - allow Login user to use this function
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # print(current_user.id)
    # print(current_user.email)
    # create post to database crated in models.py file
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post  # send back latest posts


# @router.get("/posts/{id}")
# def get_post(id: int):
#     # the query accept string, so need to convert back to string
#     cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"post with id: {id} is not found",
#         )
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message": f"post with id: {id} is not found"}
#     return {"post_detail": post}


# using SQLalchemy
# current_user code - allow Login user to use this function
# @router.get("/{id}", response_model=schemas.Post)
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # the query accept string, so need to convert back to string
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()

    # SELECT posts.*, COUNT(votes.post_id) AS votes FROM posts LEFT JOIN votes ON posts.id=votes.post_id GROUP BY posts.id;
    # filter == WHERE in SQL
    # post = (
    #     db.query(models.Post).filter(models.Post.id == id).first()
    # )
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} is not found",
        )
    # Verify only users can see their own posts
    # if post.owner_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to perform requested action",
    #     )
    return post


# delete post endpoint using raw SQL syntax
# @router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute(
#         """DELETE FROM posts WHERE id = %s RETURNING *""",
#         (str(id)),
#     )
#     deleted_post = cursor.fetchone()
#     conn.commit()

#     if deleted_post == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"post with id: {id} is not found",
#         )
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# delete post endpoint using SQLalchemy
# current_user code - allow Login user to use this function
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:  # noqa: E711
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} is not found",
        )
    # Allow only owner delete the post
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update post endpoint with PostgreSQL query
# @router.put("/posts/{id}")
# def update_post(id: int, post: schemas.Post):
#     cursor.execute(
#         """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
#         (post.title, post.content, post.published, str(id)),
#     )
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"post with id: {id} is not found",
#         )
#     return {"data": updated_post}


# update post endpoint with PostgreSQL query using SQLalchemy
# current_user code - allow Login user to use this function
@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:  # noqa: E711
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} is not found",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    # post_query.update({"title": "title is updated", "content": "content is updated"})
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
