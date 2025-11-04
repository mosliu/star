from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loguru import logger

from app.core.database import get_db
from app.models import Child, StarRecord
from app.schemas import StarAdd, StarSubtract, StarRecordResponse

router = APIRouter()

@router.post("/children/{child_id}/stars/add", response_model=StarRecordResponse, status_code=status.HTTP_201_CREATED)
async def add_stars(child_id: int, star_data: StarAdd, db: Session = Depends(get_db)):
    """Add stars to a child"""
    child = db.query(Child).filter(Child.id == child_id).first()
    
    if not child:
        logger.warning(f"Child {child_id} not found for adding stars")
        raise HTTPException(status_code=404, detail="Child not found")
    
    try:
        # Create star record
        star_record = StarRecord(
            child_id=child_id,
            type="add",
            amount=star_data.amount,
            reason=star_data.reason
        )
        
        # Update child's star count
        child.star_count += star_data.amount
        
        db.add(star_record)
        db.commit()
        db.refresh(star_record)
        
        logger.info(f"Added {star_data.amount} stars to child {child_id}. New total: {child.star_count}")
        return star_record
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding stars to child {child_id}: {e}")
        raise HTTPException(status_code=500, detail="Error adding stars")

@router.post("/children/{child_id}/stars/subtract", response_model=StarRecordResponse, status_code=status.HTTP_201_CREATED)
async def subtract_stars(child_id: int, star_data: StarSubtract, db: Session = Depends(get_db)):
    """Subtract stars from a child"""
    child = db.query(Child).filter(Child.id == child_id).first()
    
    if not child:
        logger.warning(f"Child {child_id} not found for subtracting stars")
        raise HTTPException(status_code=404, detail="Child not found")
    
    # Check if child has enough stars
    if child.star_count < star_data.amount:
        logger.warning(f"Child {child_id} has insufficient stars: {child.star_count} < {star_data.amount}")
        raise HTTPException(status_code=400, detail="Insufficient stars")
    
    try:
        # Create star record
        star_record = StarRecord(
            child_id=child_id,
            type="subtract",
            amount=star_data.amount,
            reason=star_data.reason
        )
        
        # Update child's star count
        child.star_count -= star_data.amount
        
        db.add(star_record)
        db.commit()
        db.refresh(star_record)
        
        logger.info(f"Subtracted {star_data.amount} stars from child {child_id}. New total: {child.star_count}")
        return star_record
    except Exception as e:
        db.rollback()
        logger.error(f"Error subtracting stars from child {child_id}: {e}")
        raise HTTPException(status_code=500, detail="Error subtracting stars")
