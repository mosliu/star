from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Literal
from datetime import date, datetime
from loguru import logger
import os
import uuid
from pathlib import Path

from app.core.database import get_db
from app.models import Child, StarRecord
from app.schemas import ChildCreate, ChildUpdate, ChildResponse, ChildDetailResponse
from app.core.config import settings

router = APIRouter()

def calculate_age(birthday: date) -> int:
    """Calculate age from birthday"""
    today = date.today()
    age = today.year - birthday.year
    if (today.month, today.day) < (birthday.month, birthday.day):
        age -= 1
    return age

@router.get("/")
async def get_children(db: Session = Depends(get_db)):
    """Get all children"""
    try:
        children = db.query(Child).order_by(Child.created_at.desc()).all()
        
        # Format response like PHP backend
        data = []
        for child in children:
            data.append({
                "id": child.id,
                "name": child.name,
                "birthday": child.birthday.strftime("%Y-%m-%d"),
                "age": calculate_age(child.birthday),
                "gender": child.gender,
                "avatar": f"/storage/{child.avatar}" if child.avatar else None,
                "star_count": child.star_count
            })
            
        logger.info(f"Retrieved {len(children)} children")
        return {
            "success": True,
            "data": data
        }
    except Exception as e:
        logger.error(f"Error retrieving children: {e}")
        return {
            "success": False,
            "message": "Error retrieving children"
        }

@router.get("/{child_id}")
async def get_child(child_id: int, db: Session = Depends(get_db)):
    """Get single child with details including star records and rewards"""
    from sqlalchemy.orm import joinedload
    
    child = db.query(Child).options(
        joinedload(Child.star_records).joinedload(StarRecord.reward),
        joinedload(Child.rewards)
    ).filter(Child.id == child_id).first()
    
    if not child:
        logger.warning(f"Child {child_id} not found")
        return JSONResponse(
            status_code=404,
            content={"success": False, "message": "Child not found"}
        )
    
    # Get recent 20 star records ordered by created_at desc
    star_records = sorted(child.star_records, key=lambda x: x.created_at, reverse=True)[:20]
    
    # Format star records with reward info
    formatted_star_records = []
    for record in star_records:
        formatted_record = {
            "id": record.id,
            "amount": record.amount,
            "type": record.type,
            "reason": record.reason,
            "reward": None,
            "created_at": record.created_at.strftime("%Y-%m-%d %H:%M")
        }
        
        # Add reward info if this is a redemption record
        if record.reward:
            formatted_record["reward"] = {
                "id": record.reward.id,
                "name": record.reward.name,
                "image": f"/storage/{record.reward.image}" if record.reward.image else None
            }
        
        formatted_star_records.append(formatted_record)
    
    # Format rewards this child is participating in
    formatted_rewards = []
    for reward in child.rewards:
        # Calculate total stars from all participating children
        total_stars = sum(c.star_count for c in reward.children)
        is_achieved = total_stars >= reward.star_cost
        
        formatted_rewards.append({
            "id": reward.id,
            "name": reward.name,
            "image": f"/storage/{reward.image}" if reward.image else None,
            "star_cost": reward.star_cost,
            "is_redeemed": reward.is_redeemed,
            "children": [
                {
                    "id": c.id,
                    "name": c.name,
                    "gender": c.gender,
                    "star_count": c.star_count
                }
                for c in reward.children
            ],
            "total_stars": total_stars,
            "is_achieved": is_achieved
        })
    
    logger.info(f"Retrieved child {child_id} details with {len(star_records)} star records and {len(child.rewards)} rewards")
    
    return {
        "success": True,
        "data": {
            "id": child.id,
            "name": child.name,
            "birthday": child.birthday.strftime("%Y-%m-%d"),
            "age": calculate_age(child.birthday),
            "gender": child.gender,
            "avatar": f"/storage/{child.avatar}" if child.avatar else None,
            "star_count": child.star_count,
            "star_records": formatted_star_records,
            "rewards": formatted_rewards
        }
    }

async def save_avatar_file(file: UploadFile) -> str:
    """Save avatar file and return the path"""
    # Create public storage directory like Laravel
    storage_dir = Path("public") / "storage" / "avatars"
    storage_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = storage_dir / unique_filename
    
    # Save file
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Return relative path for storage in database (matches Laravel format)
    return f"avatars/{unique_filename}"

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_child(
    name: str = Form(...),
    birthday: date = Form(...),
    gender: Literal["boy", "girl", "male", "female"] = Form(...),
    avatar: Optional[UploadFile] = File(None),
    avatar_url: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Create new child - accepts form data with optional avatar file upload"""
    try:
        # Store original gender for database (PHP uses male/female)
        db_gender = gender
        if gender == "boy":
            db_gender = "male"
        elif gender == "girl":
            db_gender = "female"
            
        # Handle avatar - file upload takes precedence over URL
        avatar_path = None
        if avatar and avatar.filename:
            # Validate file type
            allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
            file_extension = os.path.splitext(avatar.filename)[1].lower()
            if file_extension not in allowed_extensions:
                return {
                    "success": False,
                    "errors": {
                        "avatar": [f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"]
                    }
                }
            
            # Check file size (100MB max like PHP)
            if avatar.size and avatar.size > 104857600:  # 100MB in bytes
                return {
                    "success": False,
                    "errors": {
                        "avatar": ["File too large. Maximum size: 100MB"]
                    }
                }
            
            avatar_path = await save_avatar_file(avatar)
        elif avatar_url:
            avatar_path = avatar_url
            
        child = Child(
            name=name,
            birthday=birthday,
            gender=db_gender,  # Store as male/female in database
            avatar=avatar_path
        )
        db.add(child)
        db.commit()
        db.refresh(child)
        
        logger.info(f"Created child: {child.name} (ID: {child.id})")
        
        # Return response matching PHP format
        return {
            "success": True,
            "data": {
                "id": child.id,
                "name": child.name,
                "birthday": child.birthday.strftime("%Y-%m-%d"),
                "age": calculate_age(child.birthday),
                "gender": child.gender,
                "avatar": f"/storage/{child.avatar}" if child.avatar else None,
                "star_count": child.star_count
            }
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating child: {e}")
        return {
            "success": False,
            "errors": {
                "general": [f"Error creating child: {str(e)}"]
            }
        }

@router.post("/json", response_model=ChildResponse, status_code=status.HTTP_201_CREATED)
async def create_child_json(child_data: ChildCreate, db: Session = Depends(get_db)):
    """Create new child - accepts JSON data"""
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

@router.patch("/{child_id}")
async def update_child(child_id: int, child_data: ChildUpdate, db: Session = Depends(get_db)):
    """Update child information"""
    child = db.query(Child).filter(Child.id == child_id).first()
    
    if not child:
        logger.warning(f"Child {child_id} not found for update")
        return JSONResponse(
            status_code=404,
            content={"success": False, "message": "Child not found"}
        )
    
    try:
        update_data = child_data.dict(exclude_unset=True)
        
        # Convert gender if needed
        if "gender" in update_data:
            if update_data["gender"] == "boy":
                update_data["gender"] = "male"
            elif update_data["gender"] == "girl":
                update_data["gender"] = "female"
        
        for field, value in update_data.items():
            setattr(child, field, value)
        
        db.commit()
        db.refresh(child)
        
        logger.info(f"Updated child {child_id}")
        
        return {
            "success": True,
            "data": {
                "id": child.id,
                "name": child.name,
                "birthday": child.birthday.strftime("%Y-%m-%d"),
                "age": calculate_age(child.birthday),
                "gender": child.gender,
                "avatar": f"/storage/{child.avatar}" if child.avatar else None,
                "star_count": child.star_count
            }
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating child {child_id}: {e}")
        return {
            "success": False,
            "message": "Error updating child"
        }

@router.delete("/{child_id}")
async def delete_child(child_id: int, db: Session = Depends(get_db)):
    """Delete child"""
    child = db.query(Child).filter(Child.id == child_id).first()
    
    if not child:
        logger.warning(f"Child {child_id} not found for deletion")
        return JSONResponse(
            status_code=404,
            content={"success": False, "message": "Child not found"}
        )
    
    try:
        # Delete avatar file if exists
        if child.avatar:
            avatar_path = Path("public/storage") / child.avatar
            if avatar_path.exists():
                avatar_path.unlink()
        
        db.delete(child)
        db.commit()
        logger.info(f"Deleted child {child_id}")
        
        return {
            "success": True,
            "message": "Child deleted successfully"
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting child {child_id}: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Error deleting child"}
        )
