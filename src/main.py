from prefect.deployments import Deployment
from prefect.server.schemas.schedules import IntervalSchedule
from datetime import timedelta
from services.auth_service import AuthService
from database.database import DatabaseManager
from workflows.email_workflow import process_emails
from utils.logger import setup_logger
import logging

logger = setup_logger(__name__)

def main():
    try:
        # Initialize database
        db_manager = DatabaseManager()
        db_manager.init_db()
        logger.info("Database initialized")
        
        # Set up authentication
        auth_service = AuthService()
        credentials = auth_service.get_credentials()
        logger.info("Authentication completed")
        
        # Create Prefect deployment
        deployment = Deployment.build_from_flow(
            flow=process_emails,
            name="email-processor",
            schedule=IntervalSchedule(interval=timedelta(minutes=5)),
            tags=["email"]
        )
        deployment.apply()
        logger.info("Deployment created successfully")
        
    except Exception as e:
        logger.error(f"Application startup failed: {str(e)}")
        raise

if __name__ == "__main__":
    main() 