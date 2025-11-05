from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from loguru import logger
import os
import uuid
from pathlib import Path

from app.core.database import get_db
from app.models import Reward, Child, StarRecord
from app.schemas import RewardCreate, RewardUpdate, RewardResponse, RedeemRequest

router = APIRouter()

async def save_reward_image(file: UploadFile) -> str:
    """Save reward image and return the path"""
    # Create public storage directory like Laravel
    storage_dir = Path("public") / "storage" / "rewards"
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
    return f"rewards/{unique_filename}"

@router.get("/")
async def get_rewards(db: Session = Depends(get_db)):
    """Get all rewards with participants and progress"""
    try:
        rewards = db.query(Reward).order_by(Reward.is_redeemed, Reward.created_at.desc()).all()
        
        data = []
        for reward in rewards:
            total_stars = sum(child.star_count for child in reward.children)
            is_achieved = total_stars >= reward.star_cost
            
            data.append({
                "id": reward.id,
                "name": reward.name,
                "image": f"/storage/{reward.image}" if reward.image else None,
                "star_cost": reward.star_cost,
                "is_redeemed": reward.is_redeemed,
                "redeemed_at": reward.redeemed_at.strftime("%Y-%m-%d %H:%M") if reward.redeemed_at else None,
                "children": [
                    {
                        "id": child.id,
                        "name": child.name,
                        "star_count": child.star_count,
                        "avatar": f"/storage/{child.avatar}" if child.avatar else None
                    }
                    for child in reward.children
                ],
                "total_stars": total_stars,
                "is_achieved": is_achieved
            })
        
        logger.info(f"Retrieved {len(rewards)} rewards")
        return {
            "success": True,
            "data": data
        }
    except Exception as e:
        logger.error(f"Error retrieving rewards: {e}")
        return {
            "success": False,
            "message": "Error retrieving rewards"
        }

@router.get("/{reward_id}", response_model=RewardResponse)
async def get_reward(reward_id: int, db: Session = Depends(get_db)):
    """Get single reward"""
    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    
    if not reward:
        logger.warning(f"Reward {reward_id} not found")
        raise HTTPException(status_code=404, detail="Reward not found")
    
    logger.info(f"Retrieved reward {reward_id}")
    return reward

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_reward(
    name: str = Form(...),
    star_cost: int = Form(...),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    child_ids: List[int] = Form(..., alias="child_ids[]"),
    db: Session = Depends(get_db)
):
    """Create new reward"""
    try:
        # Validate child_ids are not empty
        if not child_ids:
            raise HTTPException(status_code=422, detail="At least one child must be selected")
        
        # Handle image upload if provided
        image_path = None
        if image and image.filename:
            image_path = await save_reward_image(image)
        
        # Create reward
        reward = Reward(
            name=name,
            star_cost=star_cost,
            description=description,
            image=image_path,
            is_redeemed=False  # Initialize as not redeemed
        )
        
        # Add children
        children = db.query(Child).filter(Child.id.in_(child_ids)).all()
        if len(children) != len(child_ids):
            raise HTTPException(status_code=422, detail="One or more invalid child IDs")
        reward.children = children
        
        db.add(reward)
        db.commit()
        db.refresh(reward)
        
        logger.info(f"Created reward: {reward.name} (ID: {reward.id})")
        
        # Return response in the expected format
        return {
            "success": True,
            "data": {
                "id": reward.id,
                "name": reward.name,
                "image": f"/storage/{reward.image}" if reward.image else None,
                "star_cost": reward.star_cost,
                "children": [
                    {
                        "id": child.id,
                        "name": child.name,
                        "star_count": child.star_count,
                        "avatar": f"/storage/{child.avatar}" if child.avatar else None
                    }
                    for child in reward.children
                ]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating reward: {e}")
        return {
            "success": False,
            "message": "Failed to create reward"
        }

@router.patch("/{reward_id}")
async def update_reward(
    reward_id: int,
    name: Optional[str] = Form(None),
    star_cost: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    child_ids: Optional[List[int]] = Form(None, alias="child_ids[]"),
    db: Session = Depends(get_db)
):
    """Update reward information"""
    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    
    if not reward:
        logger.warning(f"Reward {reward_id} not found for update")
        raise HTTPException(status_code=404, detail="Reward not found")
    
    # Don't allow updating redeemed rewards
    if reward.is_redeemed:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Cannot update redeemed reward"
            }
        )
    
    try:
        # Update fields if provided
        if name is not None:
            reward.name = name
        if star_cost is not None:
            reward.star_cost = star_cost
        if description is not None:
            reward.description = description
        
        # Handle image upload if provided
        if image and image.filename:
            # Delete old image if it exists
            if reward.image:
                old_image_path = Path("public") / "storage" / reward.image
                if old_image_path.exists():
                    old_image_path.unlink()
            
            # Save new image
            reward.image = await save_reward_image(image)
        
        # Update children if provided
        if child_ids is not None:
            children = db.query(Child).filter(Child.id.in_(child_ids)).all()
            if len(children) != len(child_ids):
                raise HTTPException(status_code=422, detail="One or more invalid child IDs")
            reward.children = children
        
        db.commit()
        db.refresh(reward)
        
        # Calculate total stars
        total_stars = sum(child.star_count for child in reward.children)
        
        logger.info(f"Updated reward {reward_id}")
        return {
            "success": True,
            "data": {
                "id": reward.id,
                "name": reward.name,
                "image": f"/storage/{reward.image}" if reward.image else None,
                "star_cost": reward.star_cost,
                "is_redeemed": reward.is_redeemed,
                "children": [
                    {
                        "id": child.id,
                        "name": child.name,
                        "star_count": child.star_count,
                        "avatar": f"/storage/{child.avatar}" if child.avatar else None
                    }
                    for child in reward.children
                ],
                "total_stars": total_stars,
                "is_achieved": total_stars >= reward.star_cost
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating reward {reward_id}: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Failed to update reward"
            }
        )

@router.delete("/{reward_id}")
async def delete_reward(reward_id: int, db: Session = Depends(get_db)):
    """Delete reward"""
    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    
    if not reward:
        logger.warning(f"Reward {reward_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Reward not found")
    
    # Don't allow deleting redeemed rewards
    if reward.is_redeemed:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Cannot delete redeemed reward"
            }
        )
    
    try:
        # Delete image if it exists
        if reward.image:
            image_path = Path("public") / "storage" / reward.image
            if image_path.exists():
                image_path.unlink()
        
        db.delete(reward)
        db.commit()
        logger.info(f"Deleted reward {reward_id}")
        
        return {
            "success": True,
            "message": "Reward deleted successfully"
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting reward {reward_id}: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Error deleting reward"
            }
        )

@router.post("/{reward_id}/redeem")
async def redeem_reward(reward_id: int, redeem_data: RedeemRequest, db: Session = Depends(get_db)):
    """Redeem a reward with multiple children contributing stars"""
    from datetime import datetime
    from sqlalchemy import text
    
    # Get reward
    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    if not reward:
        logger.warning(f"Reward {reward_id} not found for redemption")
        return JSONResponse(
            status_code=404,
            content={"success": False, "message": "Reward not found"}
        )
    
    # Check if already redeemed
    if reward.is_redeemed:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "Reward already redeemed"}
        )
    
    # Validate total deduction >= star_cost
    total_deduction = sum(d.amount for d in redeem_data.deductions)
    if total_deduction < reward.star_cost:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "Total deduction is less than required stars"}
        )
    
    # Validate each child has enough stars
    for deduction in redeem_data.deductions:
        child = db.query(Child).filter(Child.id == deduction.child_id).first()
        if not child:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": f"Child {deduction.child_id} not found"}
            )
        if child.star_count < deduction.amount:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": f"Child {child.name} doesn't have enough stars"}
            )
    
    try:
        # Process each deduction
        for deduction in redeem_data.deductions:
            if deduction.amount == 0:
                continue  # Skip if no deduction
                
            child = db.query(Child).filter(Child.id == deduction.child_id).first()
            
            # Create star record (redemption type) with negative amount like PHP
            star_record = StarRecord(
                child_id=child.id,
                type="redeem",
                amount=-deduction.amount,  # Store as negative like PHP
                reason=None,  # PHP doesn't set reason for redeem
                reward_id=reward.id
            )
            
            # Update child's star count
            child.star_count -= deduction.amount
            
            # Update deduction_amount in pivot table using raw SQL
            # First check if the relationship exists
            existing = db.execute(
                text("SELECT * FROM reward_children WHERE reward_id = :rid AND child_id = :cid"),
                {"rid": reward.id, "cid": child.id}
            ).fetchone()
            
            if existing:
                # Update existing relationship with deduction amount
                db.execute(
                    text("UPDATE reward_children SET deduction_amount = :amount, updated_at = :now WHERE reward_id = :rid AND child_id = :cid"),
                    {"amount": deduction.amount, "now": datetime.now(), "rid": reward.id, "cid": child.id}
                )
            else:
                # Insert new relationship with deduction amount
                db.execute(
                    text("INSERT INTO reward_children (reward_id, child_id, deduction_amount, created_at, updated_at) VALUES (:rid, :cid, :amount, :now, :now)"),
                    {"rid": reward.id, "cid": child.id, "amount": deduction.amount, "now": datetime.now()}
                )
            
            db.add(star_record)
        
        # Mark reward as redeemed
        reward.is_redeemed = True
        reward.redeemed_at = datetime.now()
        
        db.commit()
        
        logger.info(f"Reward {reward_id} redeemed successfully with deductions from multiple children")
        return {
            "success": True,
            "message": "Reward redeemed successfully"
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error redeeming reward {reward_id}: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Failed to redeem reward",
                "error": str(e)
            }
        )
