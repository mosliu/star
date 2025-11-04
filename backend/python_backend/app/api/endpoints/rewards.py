from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from loguru import logger

from app.core.database import get_db
from app.models import Reward, Child, StarRecord
from app.schemas import RewardCreate, RewardUpdate, RewardResponse, RedeemRequest

router = APIRouter()

@router.get("/", response_model=List[RewardResponse])
async def get_rewards(db: Session = Depends(get_db)):
    """Get all rewards"""
    try:
        rewards = db.query(Reward).order_by(Reward.created_at.desc()).all()
        logger.info(f"Retrieved {len(rewards)} rewards")
        return rewards
    except Exception as e:
        logger.error(f"Error retrieving rewards: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving rewards")

@router.get("/{reward_id}", response_model=RewardResponse)
async def get_reward(reward_id: int, db: Session = Depends(get_db)):
    """Get single reward"""
    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    
    if not reward:
        logger.warning(f"Reward {reward_id} not found")
        raise HTTPException(status_code=404, detail="Reward not found")
    
    logger.info(f"Retrieved reward {reward_id}")
    return reward

@router.post("/", response_model=RewardResponse, status_code=status.HTTP_201_CREATED)
async def create_reward(reward_data: RewardCreate, db: Session = Depends(get_db)):
    """Create new reward"""
    try:
        reward = Reward(**reward_data.dict())
        db.add(reward)
        db.commit()
        db.refresh(reward)
        
        logger.info(f"Created reward: {reward.name} (ID: {reward.id})")
        return reward
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating reward: {e}")
        raise HTTPException(status_code=500, detail="Error creating reward")

@router.patch("/{reward_id}", response_model=RewardResponse)
async def update_reward(reward_id: int, reward_data: RewardUpdate, db: Session = Depends(get_db)):
    """Update reward information"""
    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    
    if not reward:
        logger.warning(f"Reward {reward_id} not found for update")
        raise HTTPException(status_code=404, detail="Reward not found")
    
    try:
        update_data = reward_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(reward, field, value)
        
        db.commit()
        db.refresh(reward)
        
        logger.info(f"Updated reward {reward_id}")
        return reward
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating reward {reward_id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating reward")

@router.delete("/{reward_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reward(reward_id: int, db: Session = Depends(get_db)):
    """Delete reward"""
    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    
    if not reward:
        logger.warning(f"Reward {reward_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Reward not found")
    
    try:
        db.delete(reward)
        db.commit()
        logger.info(f"Deleted reward {reward_id}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting reward {reward_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting reward")

@router.post("/{reward_id}/redeem")
async def redeem_reward(reward_id: int, redeem_data: RedeemRequest, db: Session = Depends(get_db)):
    """Redeem a reward for a child"""
    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    if not reward:
        logger.warning(f"Reward {reward_id} not found for redemption")
        raise HTTPException(status_code=404, detail="Reward not found")
    
    child = db.query(Child).filter(Child.id == redeem_data.child_id).first()
    if not child:
        logger.warning(f"Child {redeem_data.child_id} not found for redemption")
        raise HTTPException(status_code=404, detail="Child not found")
    
    # Check if child has enough stars
    if child.star_count < reward.star_cost:
        logger.warning(f"Child {redeem_data.child_id} has insufficient stars for reward {reward_id}: {child.star_count} < {reward.star_cost}")
        raise HTTPException(status_code=400, detail="Insufficient stars for this reward")
    
    try:
        # Create star record for redemption
        star_record = StarRecord(
            child_id=child.id,
            type="redeem",
            amount=reward.star_cost,
            reason=f"Redeemed: {reward.name}",
            reward_id=reward.id
        )
        
        # Deduct stars from child
        child.star_count -= reward.star_cost
        
        # Add child to reward's children list if not already there
        if child not in reward.children:
            reward.children.append(child)
        
        db.add(star_record)
        db.commit()
        
        logger.info(f"Child {redeem_data.child_id} redeemed reward {reward_id} for {reward.star_cost} stars")
        return {
            "success": True,
            "message": f"Successfully redeemed {reward.name}",
            "remaining_stars": child.star_count
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error redeeming reward {reward_id} for child {redeem_data.child_id}: {e}")
        raise HTTPException(status_code=500, detail="Error redeeming reward")
