from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .... import crud, schemas, db as database_module

router = APIRouter(
    prefix="/animals",
    tags=["animals"]
)

@router.post("/", response_model=schemas.Animal)
def register_animal(
    animal: schemas.AnimalCreate, 
    owner_mobile: str, # For simplicity, passing mobile instead of parsing JWT in this demo
    db: Session = Depends(database_module.get_db)
):
    user = crud.get_user_by_mobile(db, owner_mobile)
    if not user:
        raise HTTPException(status_code=404, detail="User (owner) not found")
    
    # Check for duplicate tag
    if animal.tag_number:
        existing = crud.get_animal_by_tag(db, animal.tag_number)
        if existing:
            raise HTTPException(status_code=400, detail="Animal with this tag number already exists")
            
    return crud.create_animal(db=db, animal=animal, owner_id=user.id)

@router.get("/owner/{mobile}", response_model=List[schemas.Animal])
def list_owner_animals(mobile: str, db: Session = Depends(database_module.get_db)):
    user = crud.get_user_by_mobile(db, mobile)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_user_animals(db, owner_id=user.id)
