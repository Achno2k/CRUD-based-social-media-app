from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import schemas, models, oauth2, database
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/vote',
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), 
         current_user: models.User = Depends(oauth2.get_current_user)
    ):

    #checking if the post exists or not
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with ID: {vote.post_id} does not exist.")
    
    #checking if the user has already voted on a post or not, for furthur use
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()

    #if he has not voted the particular post, then we will add the vote
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The user with user ID: {current_user.id} has already voted the post with post ID: {vote.post_id}.")
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote."}
    
    #if he does not already have a vote then we cannot remove a vote from the post
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The user with user ID: {current_user.id}, do not have a pre-existing vote on the post with post ID: {vote.post_id}.")
        vote_query.delete(synchronize_session= False)
        db.commit()
        return {"message": "successfully deleted vote"}
    