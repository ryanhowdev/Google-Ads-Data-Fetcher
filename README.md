# Google Ads Data Fetcher

## Description

This Python application connects to the Google Ads API to download campaign data for a specified account and time period. It supports output in various formats, including CSV, JSON, SQLite, and MySQL, with enhanced security measures for handling credentials and sensitive information.

## Features

- Fetches Google Ads campaign data using the Google Ads API.
- Outputs data in CSV, JSON, SQLite, or MySQL format.
- Uses secure password prompts and encryption for database credentials.
- Implements robust error handling and validation.

## Prerequisites

- Python 3.x
- Google Ads API access with OAuth2 credentials
- MySQL or SQLite (if using database output options)
- Required Python libraries: `google-ads`, `pandas`, `sqlalchemy`, `pymysql` (for MySQL), `cryptography`

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourrepository/google-ads-data-fetcher.git
   cd google-ads-data-fetcher
   ```

2. **Install the required Python packages:**

   ```bash
   pip install `google-ads`, `pandas`, `sqlalchemy`, `pymysql` , `cryptography`
   ```

3. **Configure Google Ads API access:**

   - Follow Google's documentation to set up your Google Ads API client library and OAuth2 credentials. Save your `google-ads.yaml` configuration file in the project root.

4. **Encryption Key for Database Credentials (Optional):**

   - If you plan to use the MySQL output option and want to encrypt your database credentials, generate an encryption key using the `cryptography` library and store it securely.

## Usage

1. **Run the application:**

   ```bash
   python google_ads_data_fetcher.py
   ```

2. **Follow the on-screen prompts to enter:**

   - Customer ID for the Google Ads account.
   - Start and end dates for the data fetching period.
   - Output format (csv, json, sqlite, mysql).
   - If using MySQL, enter the database credentials as prompted. Password input will be securely handled.

## Functions Overview

- `download_report`: Fetches campaign data from Google Ads.
- `save_to_csv`: Saves data to a CSV file.
- `save_to_json`: Saves data to a JSON file.
- `save_to_sqlite`: Saves data to an SQLite database.
- `save_to_mysql`: Saves data to a MySQL database, with encrypted password handling.
- `encrypt_password`: Encrypts database passwords.
- `decrypt_password`: Decrypts database passwords for use in database connections.

## Security Measures

The application uses `getpass` for secure password input and `cryptography` for password encryption, ensuring sensitive information is handled securely. It's recommended to manage encryption keys securely and avoid hardcoding sensitive information.

## Contributing

Contributions to improve the application are welcome. Please follow the existing code style and submit pull requests for any enhancements or bug fixes.

## License

GNU License

