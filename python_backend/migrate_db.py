"""Database migration script to update existing database structure"""
from sqlalchemy import create_engine, text
from app.core.config import settings
from loguru import logger

def migrate_database():
    """Migrate database to match PHP Laravel structure"""
    logger.info("Starting database migration...")
    
    # Create engine
    engine = create_engine(settings.database_url)
    
    with engine.connect() as conn:
        # Check if reward_children table exists
        result = conn.execute(text(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='reward_children'"
        ))
        table_exists = result.fetchone() is not None
        
        if not table_exists:
            logger.info("Creating reward_children table...")
            
            # Create reward_children table to match PHP's structure
            conn.execute(text("""
                CREATE TABLE reward_children (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reward_id INTEGER NOT NULL,
                    child_id INTEGER NOT NULL,
                    deduction_amount INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (reward_id) REFERENCES rewards(id),
                    FOREIGN KEY (child_id) REFERENCES children(id),
                    UNIQUE(reward_id, child_id)
                )
            """))
            conn.commit()
            
            # Check if old child_reward table exists and migrate data
            result = conn.execute(text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='child_reward'"
            ))
            old_table_exists = result.fetchone() is not None
            
            if old_table_exists:
                logger.info("Migrating data from child_reward to reward_children...")
                
                # Copy data from old table to new table
                conn.execute(text("""
                    INSERT INTO reward_children (reward_id, child_id, created_at)
                    SELECT reward_id, child_id, created_at 
                    FROM child_reward
                """))
                conn.commit()
                
                # Drop old table
                conn.execute(text("DROP TABLE child_reward"))
                conn.commit()
                
                logger.info("Data migration completed")
        else:
            logger.info("reward_children table already exists")
            
            # Check if deduction_amount column exists
            result = conn.execute(text("PRAGMA table_info(reward_children)"))
            columns = [row[1] for row in result]
            
            if 'deduction_amount' not in columns:
                logger.info("Adding deduction_amount column to reward_children table...")
                conn.execute(text(
                    "ALTER TABLE reward_children ADD COLUMN deduction_amount INTEGER"
                ))
                conn.commit()
                logger.info("Column added successfully")
        
        # Check and update children table gender column if needed
        logger.info("Checking children table gender column...")
        result = conn.execute(text("PRAGMA table_info(children)"))
        columns = result.fetchall()
        
        # Find gender column info
        gender_col = None
        for col in columns:
            if col[1] == 'gender':
                gender_col = col
                break
        
        if gender_col and ('boy' in str(gender_col[2]) or 'girl' in str(gender_col[2])):
            logger.info("Updating gender values from boy/girl to male/female...")
            
            # Update existing data
            conn.execute(text("UPDATE children SET gender = 'male' WHERE gender = 'boy'"))
            conn.execute(text("UPDATE children SET gender = 'female' WHERE gender = 'girl'"))
            conn.commit()
            
            logger.info("Gender values updated")
            
            # Note: SQLite doesn't support modifying column types easily
            # The enum constraint will still be boy/girl but data is now male/female
            # This is acceptable as the Python code handles the conversion
    
    logger.info("Database migration completed successfully!")

if __name__ == "__main__":
    from app.core.logging import setup_logging
    setup_logging()
    migrate_database()
