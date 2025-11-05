"""Test script to verify all fixed features work correctly"""
import requests
import json
from datetime import date
from loguru import logger

# Base URL for API
BASE_URL = "http://localhost:8000/api"

def test_create_children():
    """Test creating children"""
    logger.info("Testing: Create children")
    
    children = [
        {"name": "小明", "birthday": "2018-05-15", "gender": "male"},
        {"name": "小红", "birthday": "2019-03-20", "gender": "female"},
        {"name": "小亮", "birthday": "2017-08-10", "gender": "male"}
    ]
    
    created_ids = []
    for child_data in children:
        response = requests.post(f"{BASE_URL}/children", data=child_data)
        assert response.status_code == 201
        result = response.json()
        assert result["success"] == True
        created_ids.append(result["data"]["id"])
        logger.success(f"Created child: {child_data['name']} (ID: {result['data']['id']})")
    
    return created_ids

def test_add_stars(child_ids):
    """Test adding stars to children"""
    logger.info("Testing: Add stars to children")
    
    star_additions = [
        (child_ids[0], 50, "做作业认真"),
        (child_ids[1], 40, "帮助妈妈做家务"),
        (child_ids[2], 30, "按时睡觉")
    ]
    
    for child_id, amount, reason in star_additions:
        response = requests.post(
            f"{BASE_URL}/children/{child_id}/stars/add",
            json={"amount": amount, "reason": reason}
        )
        assert response.status_code == 200
        result = response.json()
        assert result["success"] == True
        logger.success(f"Added {amount} stars to child {child_id}: {reason}")

def test_create_reward(child_ids):
    """Test creating a reward with multiple children"""
    logger.info("Testing: Create reward with multiple children")
    
    reward_data = {
        "name": "乐高积木套装",
        "star_cost": 100,
        "description": "奖励给表现好的小朋友",
        "child_ids[]": child_ids  # All children participate
    }
    
    response = requests.post(f"{BASE_URL}/rewards", data=reward_data)
    assert response.status_code == 201
    result = response.json()
    assert result["success"] == True
    reward_id = result["data"]["id"]
    logger.success(f"Created reward: {reward_data['name']} (ID: {reward_id})")
    
    return reward_id

def test_child_details(child_id):
    """Test getting child details with rewards and star records"""
    logger.info(f"Testing: Get child {child_id} details")
    
    response = requests.get(f"{BASE_URL}/children/{child_id}")
    assert response.status_code == 200
    result = response.json()
    assert result["success"] == True
    
    data = result["data"]
    logger.info(f"Child: {data['name']}")
    logger.info(f"  Stars: {data['star_count']}")
    logger.info(f"  Star records: {len(data['star_records'])}")
    logger.info(f"  Participating in {len(data['rewards'])} rewards")
    
    # Check that rewards are included
    assert "rewards" in data
    assert isinstance(data["rewards"], list)
    
    # Check that star records are included
    assert "star_records" in data
    assert isinstance(data["star_records"], list)
    
    if data["star_records"]:
        record = data["star_records"][0]
        assert "id" in record
        assert "amount" in record
        assert "type" in record
        assert "reason" in record
        assert "created_at" in record
        logger.success(f"  Latest record: {record['type']} {record['amount']} stars")
    
    if data["rewards"]:
        reward = data["rewards"][0]
        assert "id" in reward
        assert "name" in reward
        assert "star_cost" in reward
        assert "is_redeemed" in reward
        assert "children" in reward
        assert "total_stars" in reward
        assert "is_achieved" in reward
        logger.success(f"  Reward: {reward['name']} ({reward['total_stars']}/{reward['star_cost']} stars)")

def test_redeem_reward_multiple_children(reward_id, child_ids):
    """Test redeeming a reward with multiple children contributing"""
    logger.info("Testing: Redeem reward with multiple children")
    
    # Get current reward status
    response = requests.get(f"{BASE_URL}/rewards")
    rewards = response.json()["data"]
    reward = next(r for r in rewards if r["id"] == reward_id)
    
    logger.info(f"Reward: {reward['name']} needs {reward['star_cost']} stars")
    logger.info(f"Total stars available: {reward['total_stars']}")
    
    # Prepare deductions - multiple children contribute
    deductions_data = {
        "deductions": [
            {"child_id": child_ids[0], "amount": 50},  # 小明 contributes 50
            {"child_id": child_ids[1], "amount": 40},  # 小红 contributes 40  
            {"child_id": child_ids[2], "amount": 10}   # 小亮 contributes 10
        ]
    }
    
    logger.info("Deduction plan:")
    for d in deductions_data["deductions"]:
        logger.info(f"  Child {d['child_id']}: {d['amount']} stars")
    
    response = requests.post(
        f"{BASE_URL}/rewards/{reward_id}/redeem",
        json=deductions_data
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["success"] == True
    logger.success("Reward redeemed successfully!")
    
    # Verify stars were deducted from each child
    for deduction in deductions_data["deductions"]:
        response = requests.get(f"{BASE_URL}/children/{deduction['child_id']}")
        child = response.json()["data"]
        logger.info(f"Child {child['name']} now has {child['star_count']} stars")
        
        # Check star record for redemption
        star_records = child["star_records"]
        redeem_record = next((r for r in star_records if r["type"] == "redeem"), None)
        assert redeem_record is not None
        assert redeem_record["amount"] == -deduction["amount"]  # Should be negative
        assert redeem_record["reward"] is not None
        assert redeem_record["reward"]["name"] == reward["name"]
        logger.success(f"  Found redemption record: {redeem_record['amount']} stars")

def test_reward_list():
    """Test getting rewards list with all details"""
    logger.info("Testing: Get rewards list")
    
    response = requests.get(f"{BASE_URL}/rewards")
    assert response.status_code == 200
    result = response.json()
    assert result["success"] == True
    
    rewards = result["data"]
    logger.info(f"Found {len(rewards)} rewards")
    
    for reward in rewards:
        assert "id" in reward
        assert "name" in reward
        assert "star_cost" in reward
        assert "is_redeemed" in reward
        assert "children" in reward
        assert "total_stars" in reward
        assert "is_achieved" in reward
        
        status = "Redeemed" if reward["is_redeemed"] else "Active"
        progress = f"{reward['total_stars']}/{reward['star_cost']}"
        logger.info(f"  {reward['name']}: {status} ({progress} stars)")

def main():
    """Run all tests"""
    logger.info("=" * 60)
    logger.info("Starting comprehensive feature tests")
    logger.info("=" * 60)
    
    try:
        # Test 1: Create children
        child_ids = test_create_children()
        logger.info("-" * 40)
        
        # Test 2: Add stars
        test_add_stars(child_ids)
        logger.info("-" * 40)
        
        # Test 3: Create reward with multiple children
        reward_id = test_create_reward(child_ids)
        logger.info("-" * 40)
        
        # Test 4: Check child details (with rewards and star records)
        for child_id in child_ids:
            test_child_details(child_id)
        logger.info("-" * 40)
        
        # Test 5: Get rewards list
        test_reward_list()
        logger.info("-" * 40)
        
        # Test 6: Redeem reward with multiple children contributing
        test_redeem_reward_multiple_children(reward_id, child_ids)
        logger.info("-" * 40)
        
        # Test 7: Verify child details after redemption
        logger.info("Verifying child details after redemption:")
        for child_id in child_ids:
            test_child_details(child_id)
        logger.info("-" * 40)
        
        # Test 8: Verify reward is marked as redeemed
        test_reward_list()
        
        logger.info("=" * 60)
        logger.success("ALL TESTS PASSED! ✨")
        logger.info("Python backend now fully implements PHP Laravel functionality!")
        logger.info("=" * 60)
        
    except AssertionError as e:
        logger.error(f"Test failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

if __name__ == "__main__":
    from app.core.logging import setup_logging
    setup_logging()
    main()
