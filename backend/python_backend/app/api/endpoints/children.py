from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from loguru import logger

from app.core.database import get_db
from app.models import Child
from app.schemas import ChildCreate, ChildUpdate, ChildResponse, ChildDetailResponse

router = APIRouter()

def calculate_age(birthday: date) -> int:
    """Calculate age from birthday"""
    today = date.today()
    age = today.year - birthday.year
    if (today.month, today.day) < (birthday.month, birthday.day):
        age -= 1
    return age

@router.get("/", response_model=List[ChildResponse])
async def get_children(db: Session = Depends(get_db)):
    """Get all children"""
    try:
        children = db.query(Child).order_by(Child.created_at.desc()).all()
        
        # Add calculated age to each child
        for child in children:
            child.age = calculate_age(child.birthday)
            
        logger.info(f"Retrieved {len(children)} children")
        return children
    except Exception as e:
        logger.error(f"Error retrieving children: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving children")

@router.get("/{child_id}", response_model=ChildDetailResponse)
async def get_child(child_id: int, db: Session = Depends(get_db)):
    """Get single child with details"""
    child = db.query(Child).filter(Child.id == child_id).first()
    
    if not child:
        logger.warning(f"Child {child_id} not found")
        raise HTTPException(status_code=404, detail="Child not found")
    
    child.age = calculate_age(child.birthday)
    
    # Load recent star records (limit to 20)
    child.star_records = child.star_records[-20:] if child.star_records else []
    
    logger.info(f"Retrieved child {child_id} details")
    return child

@router.post("/", response_model=ChildResponse, status_code=status.HTTP_201_CREATED)
async def create_child(child_data: ChildCreate, db: Session = Depends(get_db)):
    """Create new child"""
    try:
        child = Child(**child_data.dict())
        db.add(child)
        db.commit()
        db.refresh(child)
        
        child.age = calculate_age(child.birthday)
        
        logger.info(f"Created child: {child.name} (ID: {child.id})")
        return child
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating child: {e}")
        raise HTTPException(status_code=500, detail="Error creating child")

@router.patch("/{child_id}", response_model=ChildResponse)
async def update_child(child_id: int, child_data: ChildUpdate, db: Session = Depends(get_db)):
    """Update child information"""
    child = db.query(Child).filter(Child.id == child_id).first()
    
    if not child:
        logger.warning(f"Child {child_id} not found for update")
        raise HTTPException(status_code=404, detail="Child not found")
    
    try:
        update_data = child_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(child, field, value)
        
        db.commit()
        db.refresh(child)
        
        child.age = calculate_age(child.birthday)
        
        logger.info(f"Updated child {child_id}")
        return child
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating child {child_id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating child")

@router.delete("/{child_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_child(child_id: int, db: Session = Depends(get_db)):
    """Delete child"""
    child = db.query(Child).filter(Child.id == child_id).first()
    
    if not child:
        logger.warning(f"Child {child_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Child not found")
    
    try:
        db.delete(child)
        db.commit()
        logger.info(f"Deleted child {child_id}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting child {child_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting child")
