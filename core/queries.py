CREATE_SCHEMA_QUERY = """
-- Create the schema 'X' if it doesn't exist
CREATE SCHEMA IF NOT EXISTS `X`;
"""

USE_X_QUERY = "USE X;"

CREATE_USERS_TABLE_QUERY = """
-- Create the users table if it doesn't exist
CREATE TABLE IF NOT EXISTS `X`.`users` (
    username VARCHAR(100) NOT NULL,
    phone_number VARCHAR(50) PRIMARY KEY,
    account_balance DECIMAL(10, 2),
    password VARCHAR(500),
    national_identification_number VARCHAR(30),
    address VARCHAR(50),
    date_of_registration DATE,
    time_of_registration TIME,
    agent_number_of_agent_who_registered VARCHAR(100)
);
"""

CREATE_AGENTS_TABLE_QUERY = """
-- Create the agents table if it doesn't exist
CREATE TABLE IF NOT EXISTS agents (
    agent_number VARCHAR(100) PRIMARY KEY,
    registered_user_phone_number VARCHAR(100),    
    agent_name VARCHAR(100),
    float_balance DECIMAL(10, 2),
    date_of_creation DATE,
    time_of_registration TIME,
    agent_number_of_superagent_who_registered VARCHAR(100),
    agent_location VARCHAR(100)
);
"""

CREATE_BUSINESSES_QUERY = """
-- Create the businesses table if it doesn't exist
CREATE TABLE IF NOT EXISTS businesses (
    till_number VARCHAR(100) PRIMARY KEY,
    business_name VARCHAR(100) NOT NULL,
    business_owner_phone_number VARCHAR(50),
    account_balance DECIMAL(10, 2),
    date_of_registration DATE,
    time_of_registration TIME,
    agent_number_of_agent_who_registered VARCHAR(100)
);
"""

CREATE_POCHI_LA_BIASHARA_QUERY = """
-- Create the pochi_la_biashara table if it does not exist
CREATE TABLE IF NOT EXISTS pochi_la_biashara (
    registered_user_phone_number VARCHAR(100) PRIMARY KEY,
    account_balance DECIMAL(10, 2)
)
"""

CREATE_PAY_BILL_SERVICE_MERCHANTS_QUERY = """
-- Create pay_bill_merchants table if it does not exist
CREATE TABLE IF NOT EXISTS pay_bill_merchants (
    service_name VARCHAR(100) NOT NULL,
    business_number VARCHAR(100) PRIMARY KEY,
    admin_passkey VARCHAR(100) NOT NULL,
    account_balance DECIMAL(10, 2)
)
"""

CREATE_TRANSACTIONS_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_code VARCHAR(100),
    transaction_type VARCHAR(100),
    amount DECIMAL(10, 2),
    transaction_cost DOUBLE(10, 2),
    date_of_transaction DATE,
    time_of_transaction TIME
)
"""

CREATE_TRANSACTION_RECORD_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS transaction_record (
    transaction_id INT PRIMARY KEY,
    sender_id VARCHAR(100),
    receiver_id VARCHAR(100)

)
"""

CREATE_PAY_BILL_API_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS pay_bill_api_database (
    transaction_code VARCHAR(100) PRIMARY KEY,
    business_number VARCHAR(100),
    account_number VARCHAR(100),
    amount DOUBLE(10, 2)
)
"""

INSERT_USER_QUERY = "INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
INSERT_AGENT_QUERY = "INSERT INTO agents VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
INSERT_NEW_BUSINESS_QUERY = "INSERT INTO businesses VALUES(%s, %s, %s, %s, %s, %s, %s)"
INSERT_POCHI_LA_BIASHARA_QUERY = "INSERT INTO pochi_la_biashara VALUES(%s, %s)"
INSERT_PAY_BILL_SERVICE_MERCHANTS_QUERY = "INSERT INTO pay_bill_merchants VALUES(%s, %s, %s, %s)"
INSERT_INTO_TRANSACTIONS_QUERY = "INSERT INTO transactions (transaction_code, transaction_type, amount, transaction_cost, date_of_transaction, time_of_transaction) VALUES(%s, %s, %s, %s, %s, %s)"
INSERT_TRANSACTION_RECORD_QUERY = "INSERT INTO transaction_record (sender_id, receiver_id) VALUES(%s, %s)"
INSERT_PAY_BILL_API_QUERY = "INSERT INTO pay_bill_api_database VALUES(%s, %s, %s, %s)"


FETCH_USER_QUERY = 'SELECT * FROM users WHERE phone_number = "%s"'
FETCH_AGENT_QUERY = "SELECT * FROM agents WHERE agent_number = %s"
FETCH_BUSINESS_QUERY = "SELECT * FROM businesses WHERE till_number = %s"
FETCH_POCHI_LA_BIASHARA_QUERY = "SELECT * FROM pochi_la_biashara WHERE registered_user_phone_number = %s"
FETCH_PAY_BILL_SERVICE_MERCHANT_QUERY = "SELECT * FROM pay_bill_merchants WHERE business_number = %s"
FETCH_PAY_BILL_API_QUERY = "SELECT * FROM pay_bill_api_database WHERE transaction_code = %s"

UPDATE_QUERY = "UPDATE `%s` SET `%s` = '%s' WHERE (`%s` = '%s');"

SETUP_QUERIES = (
    CREATE_SCHEMA_QUERY,
    USE_X_QUERY,
    CREATE_BUSINESSES_QUERY,
    CREATE_POCHI_LA_BIASHARA_QUERY,
    CREATE_USERS_TABLE_QUERY,
    CREATE_AGENTS_TABLE_QUERY,
    CREATE_PAY_BILL_SERVICE_MERCHANTS_QUERY,
    CREATE_TRANSACTIONS_TABLE_QUERY,
    CREATE_TRANSACTION_RECORD_TABLE_QUERY,
    CREATE_PAY_BILL_API_TABLE_QUERY
)
