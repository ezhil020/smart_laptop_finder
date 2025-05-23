import pandas as pd

def clean_csv(input_csv, output_csv):
    # Read the CSV file
    df = pd.read_csv(input_csv)
    
    # Define default values
    default_values = {
        'company': 0,
        'Price (in Indian Rupees)': 0,
        'Processor name': 'Unknown Processor',
        'RAM (in GB)': 8,
        'Storage': 512,
        'user rating': 4.0
    }
    
    # Fill missing values with defaults
    for column, default in default_values.items():
        if column in df.columns:
            df[column] = df[column].fillna(default)
    
    # Save the cleaned CSV
    df.to_csv(output_csv, index=False)
    print(f"Cleaned CSV saved to {output_csv}")

# Example usage
clean_csv('Laptop_ranked_with_Extra_Features.csv', 'Cleaned_Laptop_Data.csv')