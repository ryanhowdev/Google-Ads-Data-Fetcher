import pandas as pd
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import sys
import getpass
from cryptography.fernet import Fernet

# Initialize the Google Ads API client
client = GoogleAdsClient.load_from_storage("path/to/google-ads.yaml")

# Function to encrypt the password
def encrypt_password(password, key):
    fernet = Fernet(key)
    return fernet.encrypt(password.encode())

# Function to decrypt the password
def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password).decode()

def generate_encryption_key():
    return Fernet.generate_key()

def download_report(client, customer_id, start_date, end_date):
    ga_service = client.get_service("GoogleAdsService")
    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            ad_group.id,
            ad_group.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros
        FROM campaign
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
    """
    response = ga_service.search_stream(customer_id=customer_id, query=query)
    
    rows = []
    for batch in response:
        for row in batch.results:
            rows.append({
                "Campaign ID": row.campaign.id.value,
                "Campaign Name": row.campaign.name.value,
                "Ad Group ID": row.ad_group.id.value,
                "Ad Group Name": row.ad_group.name.value,
                "Impressions": row.metrics.impressions.value,
                "Clicks": row.metrics.clicks.value,
                "Cost": row.metrics.cost_micros.value / 1e6  # Convert from micros to units
            })
    
    return pd.DataFrame(rows)

def save_to_csv(data_frame, file_name):
    try:
        data_frame.to_csv(file_name, index=False)
    except Exception as e:
        print(f"Failed to save CSV: {e}")
        sys.exit(1)

def save_to_json(data_frame, file_name):
    try:
        data_frame.to_json(file_name)
    except Exception as e:
        print(f"Failed to save JSON: {e}")
        sys.exit(1)

def save_to_sqlite(data_frame, table_name, db_name="google_ads_data.db"):
    try:
        engine = create_engine(f'sqlite:///{db_name}')
        data_frame.to_sql(table_name, con=engine, if_exists='replace', index=False)
    except SQLAlchemyError as e:
        print(f"Failed to save to SQLite: {e}")
        sys.exit(1)

def save_to_mysql(data_frame, table_name, db_details, key):
    try:
        password = decrypt_password(db_details['password'], key)
        engine = create_engine(f"mysql+pymysql://{db_details['username']}:{password}@{db_details['host']}/{db_details['database']}")
        data_frame.to_sql(table_name, con=engine, if_exists='replace', index=False)
    except SQLAlchemyError as e:
        print(f"Failed to save to MySQL: {e}")
        sys.exit(1)

def main():
    # Encryption key generation (for demonstration; in practice, use a securely stored key)
    key = generate_encryption_key()
    
    # Your existing setup and download logic
    
    customer_id = input("Enter the customer ID: ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    output_format = input("Enter output format (csv, json, sqlite, mysql): ").lower()

    if not customer_id.isdigit() or len(customer_id) != 10:
        print("Invalid customer ID. The customer ID should be a 10-digit number.")
        sys.exit(1)

    try:
        data_frame = download_report(client, customer_id, start_date, end_date)
        
        if output_format == 'csv':
            file_name = "google_ads_data.csv"
            save_to_csv(data_frame, file_name)
            print(f"Data saved to {file_name}.")
        elif output_format == 'json':
            file_name = "google_ads_data.json"
            save_to_json(data_frame, file_name)
            print(f"Data saved to {file_name}.")
        elif output_format == 'sqlite':
            table_name = "google_ads_data"
            save_to_sqlite(data_frame, table_name)
            print(f"Data saved to SQLite database in table {table_name}.")
        elif output_format == 'mysql':
            db_details = {
                "username": input("Enter the MySQL username: "),
                "password": input("Enter the MySQL password: "),
                "host": input("Enter the MySQL host, e.g., localhost: "),
                "database": input("Enter the MySQL database name: ")
            }
            table_name = "google_ads_data"
            save_to_mysql(data_frame, table_name, db_details)
            print(f"Data saved to MySQL database in table {table_name}.")
        else:
            print("Unsupported format. Exiting.")
            sys.exit(1)
    except GoogleAdsException as e:
        print(f"Request failed with status {e.error.code().name}, includes failures: {e.failure}")
        sys.exit(1)

if __name__ == "__main__":
    main()
