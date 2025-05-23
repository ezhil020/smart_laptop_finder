from app import db
from models import Laptop
import logging
from import_laptops import import_laptops_from_csv

def initialize_laptop_data():
    """
    Initialize the database with laptop data if it doesn't already exist.
    This function checks if laptops exist in the database and adds them if not.
    """
    # Check if we already have laptops in the database
    laptop_count = Laptop.query.count()
    if laptop_count > 0:
        logging.info(f"Database already contains {laptop_count} laptops. Skipping initialization.")
        return

    logging.info("Initializing laptop database with data from the CSV file...")

    # Path to the CSV file
    csv_path = "c:\\Users\\ragur\\Downloads\\Laptop_ranked_with_Extra_Features.csv"

    # Import laptops from the CSV file
    success = import_laptops_from_csv(csv_path)
    if success:
        logging.info("Laptop data import completed successfully.")
    else:
        logging.error("Laptop data import failed.")