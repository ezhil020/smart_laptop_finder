import pandas as pd
import logging
import os
import sys
from app import app, db
from models import Laptop

logging.basicConfig(level=logging.INFO)

def import_laptops_from_csv(csv_path):
    """
    Import laptops from a CSV file into the database.
    
    Args:
        csv_path: Path to the CSV file containing laptop data
    """
    try:
        # Read CSV file
        logging.info(f"Reading laptop data from {csv_path}")
        df = pd.read_csv(csv_path)
        
        # Define the mapping for company tokens
        company_mapping = {
            1: "ASUS",
            2: "HP",
            3: "Lenovo",
            4: "Dell",
            5: "MSI",
            6: "Realme",
            7: "Avita",
            8: "Acer",
            9: "Samsung",
            10: "Infinix",
            11: "LG",
            12: "Apple",
            13: "Nokia",
            14: "RedmiBook",
            15: "Mi",
            16: "Vaio"
        }
        
        # Clean up data
        logging.info(f"Processing {len(df)} laptop records")
        
        with app.app_context():
            # Clear existing data
            num_deleted = db.session.query(Laptop).delete()
            logging.info(f"Cleared {num_deleted} existing laptop records")
            db.session.commit()
            
            # Process laptops
            count = 0
            for _, row in df.iterrows():
                try:
                    # Map the company token to the actual brand name
                    company_token = int(row['company']) if pd.notna(row['company']) else None
                    brand = company_mapping.get(company_token, "Unknown")  # Map token to company name
                    brand = brand[:100]  # Limit to 100 characters
                    
                    # Extract and clean other fields (existing logic)
                    model = str(row['name']).strip() if pd.notna(row['name']) else "Unknown Model"
                    model = model[:500]  # Limit to 500 chars
                    
                    price = float(row['Price (in Indian Rupees)']) if pd.notna(row['Price (in Indian Rupees)']) else 0
                    
                    cpu = str(row['Processor name']).strip() if pd.notna(row['Processor name']) else "Unknown CPU"
                    cpu = cpu[:200]  # Limit to 200 chars
                    
                    gpu_column = 'gpu name ' if 'gpu name ' in row else 'gpu name'
                    gpu = str(row[gpu_column]).strip() if pd.notna(row[gpu_column]) else "Integrated Graphics"
                    gpu = gpu[:200]  # Limit to 200 chars
                    
                    ram = int(row['RAM (in GB)']) if pd.notna(row['RAM (in GB)']) else 8
                    storage_capacity = int(row['Storage']) if pd.notna(row['Storage']) else 512
                    storage_type = "SSD" if "SSD" in str(row['Type']).upper() else "HDD"
                    
                    display_size = float(row['Screen Size (in inch)']) if pd.notna(row['Screen Size (in inch)']) else 15.6
                    display_resolution = str(row['screen_resolution']).strip() if pd.notna(row['screen_resolution']) else "1920x1080"
                    display_resolution = display_resolution[:50]  # Limit to 50 chars
                    refresh_rate = int(row['Refresh Rate']) if pd.notna(row['Refresh Rate']) else 60
                    
                    weight = float(row['Weight (in kg)']) if pd.notna(row['Weight (in kg)']) else 2.0
                    battery_life = float(row['Battery Life (hrs)']) if pd.notna(row['Battery Life (hrs)']) else 6.0
                    
                    os = str(row['Operating System']).strip() if pd.notna(row['Operating System']) else "Windows 10"
                    os = os[:100]  # Limit to 100 chars
                    
                    cinebench_score = int(row['Cinebench R23 Score']) if pd.notna(row['Cinebench R23 Score']) else None
                    geekbench_score = int(row['Geekbench 6 Score']) if pd.notna(row['Geekbench 6 Score']) else None
                    
                    gaming_fps = None
                    if 'Gaming Performance (FPS)' in row and pd.notna(row['Gaming Performance (FPS)']):
                        gaming_fps = float(row['Gaming Performance (FPS)'])
                    elif 'Gaming Performance Score' in row and pd.notna(row['Gaming Performance Score']):
                        gaming_fps = float(row['Gaming Performance Score'])
                    
                    user_rating = float(row['user rating']) if pd.notna(row['user rating']) else 4.0
                    build_quality = str(row['Build Material']).strip() if pd.notna(row['Build Material']) else "Average"
                    build_quality = build_quality[:100]  # Limit to 100 chars
                    
                    if price < 40000:
                        value_category = "Budget"
                    elif price < 80000:
                        value_category = "Mid-Range"
                    else:
                        value_category = "High-End"
                    value_category = value_category[:50]  # Limit to 50 chars
                    
                    is_gaming = "gaming" in str(row['Type']).lower() or "gtx" in str(gpu).lower() or "rtx" in str(gpu).lower()
                    is_business = "business" in str(row['Type']).lower() or "thinkpad" in str(model).lower() or "xps" in str(model).lower()
                    is_student = ram >= 8 and price <= 80000
                    is_content_creation = ram >= 16 or "i7" in str(cpu).lower() or "i9" in str(cpu).lower() or "ryzen 7" in str(cpu).lower()
                    
                    perf_score = 0
                    if pd.notna(row['CPU_ranking']):
                        perf_score += float(row['CPU_ranking']) * 0.5
                    if pd.notna(row['gpu_benchmark']):
                        perf_score += float(row['gpu_benchmark']) * 0.3
                    if pd.notna(ram):
                        perf_score += ram * 0.2
                        
                    price_perf_ratio = perf_score / price if price > 0 else 0.5
                    price_perf_ratio = min(1.0, price_perf_ratio)  # Normalize to max 1.0
                    
                    product_url = str(row['link']) if pd.notna(row.get('link')) else None
                    
                    laptop = Laptop(
                        brand=brand,
                        model=model,
                        price=price,
                        product_url=product_url,
                        cpu=cpu,
                        gpu=gpu,
                        ram=ram,
                        storage_type=storage_type,
                        storage_capacity=storage_capacity,
                        display_size=display_size,
                        display_resolution=display_resolution,
                        display_refresh_rate=refresh_rate,
                        weight=weight,
                        battery_life=battery_life,
                        operating_system=os,
                        cinebench_score=cinebench_score,
                        geekbench_score=geekbench_score,
                        gaming_fps=gaming_fps,
                        user_rating=user_rating,
                        build_quality=build_quality,
                        value_category=value_category,
                        suitable_for_gaming=is_gaming,
                        suitable_for_business=is_business,
                        suitable_for_students=is_student,
                        suitable_for_content_creation=is_content_creation,
                        price_performance_ratio=price_perf_ratio
                    )
                    
                    db.session.add(laptop)
                    count += 1
                    
                    if count % 50 == 0:
                        db.session.commit()
                        logging.info(f"Imported {count} laptops so far...")
                    
                except Exception as e:
                    logging.error(f"Error processing laptop row: {e}")
                    continue
            
            db.session.commit()
            logging.info(f"Successfully imported {count} laptops")
    
    except Exception as e:
        logging.error(f"Error importing laptops: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_laptops.py path/to/laptops.csv")
        sys.exit(1)
        
    csv_path = sys.argv[1]
    if not os.path.exists(csv_path):
        print(f"Error: File {csv_path} not found")
        sys.exit(1)
        
    success = import_laptops_from_csv(csv_path)
    if success:
        print("Laptop data import completed successfully")
    else:
        print("Laptop data import failed")
        sys.exit(1)