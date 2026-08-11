from pathlib import Path

import pandas as pd


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "DATA" / "RAW"
CLEANED_DATA_DIR = PROJECT_ROOT / "DATA" / "CLEANED"

ACCOUNTS_FILE = RAW_DATA_DIR / "HI-Small_accounts.csv"


# --------------------------------------------------
# CREATE OUTPUT DIRECTORY IF NEEDED
# --------------------------------------------------

CLEANED_DATA_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# SCRIPT HEADER
# --------------------------------------------------

print("=" * 70)
print("BANKING FRAUD & FINANCIAL RISK INTELLIGENCE PLATFORM")
print("PHASE 2: CLEANING & STANDARDIZATION")
print("STEP 1: CLEAN ACCOUNTS DATASET")
print("=" * 70)


print(f"\nProject Root          : {PROJECT_ROOT}")
print(f"Raw Accounts File     : {ACCOUNTS_FILE}")
print(f"Cleaned Data Directory: {CLEANED_DATA_DIR}")


# --------------------------------------------------
# VERIFY RAW ACCOUNTS FILE
# --------------------------------------------------

if not ACCOUNTS_FILE.exists():
    raise FileNotFoundError(
        f"Raw accounts file not found: {ACCOUNTS_FILE}"
    )

print("\nRaw accounts file found successfully.")


# --------------------------------------------------
# LOAD RAW ACCOUNTS DATASET
# --------------------------------------------------

print("\nLoading raw accounts dataset...")

raw_accounts_df = pd.read_csv(
    ACCOUNTS_FILE,
    dtype={
        "Bank ID": "int64",
        "Account Number": "string",
        "Entity ID": "string"
    }
)

print("Raw accounts dataset loaded successfully.")

print(f"\nRows   : {len(raw_accounts_df):,}")
print(f"Columns: {len(raw_accounts_df.columns):,}")

print("\nColumn Names:")

for column in raw_accounts_df.columns:
    print(f"  - {column}")

print("\nFirst 5 Records:")
print(raw_accounts_df.head())

# --------------------------------------------------
# STANDARDIZE COLUMN NAMES
# --------------------------------------------------

print("\n" + "=" * 70)
print("STANDARDIZING ACCOUNT COLUMN NAMES")
print("=" * 70)

accounts_standardized_df = raw_accounts_df.rename(
    columns={
        "Bank Name": "bank_name",
        "Bank ID": "bank_id",
        "Account Number": "account_number",
        "Entity ID": "entity_id",
        "Entity Name": "entity_name"
    }
).copy()

print("\nStandardized Column Names:")

for column in accounts_standardized_df.columns:
    print(f"  - {column}")


# --------------------------------------------------
# CREATE BANKS TABLE
# --------------------------------------------------

print("\n" + "=" * 70)
print("CREATING BANKS TABLE")
print("=" * 70)

banks_df = (
    accounts_standardized_df[
        ["bank_id", "bank_name"]
    ]
    .drop_duplicates(subset=["bank_id"])
    .sort_values("bank_id")
    .reset_index(drop=True)
)


# Validate one row per bank_id
if banks_df["bank_id"].duplicated().any():
    raise ValueError(
        "Banks table creation failed: duplicate bank_id detected."
    )


print("\nBanks table created successfully.")

print(f"Bank Rows: {len(banks_df):,}")

print("\nFirst 10 Bank Records:")
print(banks_df.head(10))

# --------------------------------------------------
# CREATE CUSTOMERS TABLE
# --------------------------------------------------

print("\n" + "=" * 70)
print("CREATING CUSTOMERS TABLE")
print("=" * 70)


# One row per unique IBM entity
customers_df = (
    accounts_standardized_df[
        ["entity_id", "entity_name"]
    ]
    .drop_duplicates(subset=["entity_id"])
    .sort_values("entity_id")
    .reset_index(drop=True)
)


# --------------------------------------------------
# VALIDATE ENTITY ID UNIQUENESS
# --------------------------------------------------

if customers_df["entity_id"].duplicated().any():
    raise ValueError(
        "Customers table creation failed: duplicate entity_id detected."
    )


# --------------------------------------------------
# CREATE STABLE CUSTOMER ID
# --------------------------------------------------

customers_df.insert(
    0,
    "customer_id",
    [
        f"CUST_{number:06d}"
        for number in range(1, len(customers_df) + 1)
    ]
)


# --------------------------------------------------
# VALIDATE CUSTOMER ID UNIQUENESS
# --------------------------------------------------

if customers_df["customer_id"].duplicated().any():
    raise ValueError(
        "Customers table creation failed: duplicate customer_id detected."
    )


print("\nCustomers table created successfully.")

print(f"Customer Rows: {len(customers_df):,}")

print(
    f"Unique Customer IDs: "
    f"{customers_df['customer_id'].nunique():,}"
)

print(
    f"Unique IBM Entity IDs: "
    f"{customers_df['entity_id'].nunique():,}"
)

print("\nCustomer Columns:")

for column in customers_df.columns:
    print(f"  - {column}")

print("\nFirst 10 Customer Records:")
print(customers_df.head(10))

# --------------------------------------------------
# CREATE CLEANED ACCOUNTS TABLE
# --------------------------------------------------

print("\n" + "=" * 70)
print("CREATING CLEANED ACCOUNTS TABLE")
print("=" * 70)


# Create entity_id -> customer_id mapping
customer_mapping_df = customers_df[
    ["entity_id", "customer_id"]
]


# Attach customer_id to every IBM account
cleaned_accounts_df = accounts_standardized_df.merge(
    customer_mapping_df,
    on="entity_id",
    how="left",
    validate="many_to_one"
)


# --------------------------------------------------
# VALIDATE CUSTOMER REFERENCES
# --------------------------------------------------

missing_customer_ids = (
    cleaned_accounts_df["customer_id"]
    .isna()
    .sum()
)

if missing_customer_ids > 0:
    raise ValueError(
        f"Accounts table creation failed: "
        f"{missing_customer_ids:,} accounts have no customer_id."
    )


# --------------------------------------------------
# SORT BY ORIGINAL IBM COMPOSITE ACCOUNT KEY
# --------------------------------------------------

cleaned_accounts_df = (
    cleaned_accounts_df
    .sort_values(
        ["bank_id", "account_number"]
    )
    .reset_index(drop=True)
)


# --------------------------------------------------
# CREATE STABLE ACCOUNT ID
# --------------------------------------------------

cleaned_accounts_df.insert(
    0,
    "account_id",
    [
        f"ACC_{number:07d}"
        for number in range(
            1,
            len(cleaned_accounts_df) + 1
        )
    ]
)


# --------------------------------------------------
# SELECT FINAL CLEANED ACCOUNT COLUMNS
# --------------------------------------------------

cleaned_accounts_df = cleaned_accounts_df[
    [
        "account_id",
        "customer_id",
        "bank_id",
        "account_number",
        "entity_id"
    ]
]


# --------------------------------------------------
# VALIDATE ACCOUNT TABLE
# --------------------------------------------------

if cleaned_accounts_df["account_id"].duplicated().any():
    raise ValueError(
        "Duplicate account_id detected."
    )


duplicate_composite_keys = (
    cleaned_accounts_df
    .duplicated(
        subset=["bank_id", "account_number"]
    )
    .sum()
)

if duplicate_composite_keys > 0:
    raise ValueError(
        f"{duplicate_composite_keys:,} duplicate "
        f"(bank_id, account_number) keys detected."
    )


print("\nCleaned accounts table created successfully.")

print(f"Account Rows: {len(cleaned_accounts_df):,}")

print(
    f"Unique Account IDs: "
    f"{cleaned_accounts_df['account_id'].nunique():,}"
)

print(
    f"Unique Composite Account Keys: "
    f"{cleaned_accounts_df[['bank_id', 'account_number']].drop_duplicates().shape[0]:,}"
)

print(
    f"Missing Customer References: "
    f"{cleaned_accounts_df['customer_id'].isna().sum():,}"
)

print("\nCleaned Account Columns:")

for column in cleaned_accounts_df.columns:
    print(f"  - {column}")

print("\nFirst 10 Cleaned Account Records:")
print(cleaned_accounts_df.head(10))

# --------------------------------------------------
# FINAL VALIDATION AND SAVE CLEANED TABLES
# --------------------------------------------------

print("\n" + "=" * 70)
print("FINAL VALIDATION AND SAVING CLEANED ACCOUNT TABLES")
print("=" * 70)


# Validate expected row counts
assert len(banks_df) == 30_470, "Unexpected banks row count."
assert len(customers_df) == 166_207, "Unexpected customers row count."
assert len(cleaned_accounts_df) == 518_581, "Unexpected accounts row count."


# Validate primary keys
assert banks_df["bank_id"].is_unique, "bank_id is not unique."
assert customers_df["customer_id"].is_unique, "customer_id is not unique."
assert customers_df["entity_id"].is_unique, "entity_id is not unique."
assert cleaned_accounts_df["account_id"].is_unique, "account_id is not unique."


# Validate foreign key: accounts -> customers
invalid_customer_refs = (
    ~cleaned_accounts_df["customer_id"]
    .isin(customers_df["customer_id"])
).sum()


# Validate foreign key: accounts -> banks
invalid_bank_refs = (
    ~cleaned_accounts_df["bank_id"]
    .isin(banks_df["bank_id"])
).sum()


if invalid_customer_refs > 0:
    raise ValueError(
        f"{invalid_customer_refs:,} invalid customer references detected."
    )

if invalid_bank_refs > 0:
    raise ValueError(
        f"{invalid_bank_refs:,} invalid bank references detected."
    )


# Define output files
BANKS_OUTPUT_FILE = CLEANED_DATA_DIR / "banks.csv"
CUSTOMERS_OUTPUT_FILE = CLEANED_DATA_DIR / "customers.csv"
ACCOUNTS_OUTPUT_FILE = CLEANED_DATA_DIR / "accounts.csv"


# Save cleaned tables
banks_df.to_csv(
    BANKS_OUTPUT_FILE,
    index=False
)

customers_df.to_csv(
    CUSTOMERS_OUTPUT_FILE,
    index=False
)

cleaned_accounts_df.to_csv(
    ACCOUNTS_OUTPUT_FILE,
    index=False
)


print("\nAll final validations passed successfully.")

print(f"\nInvalid Customer References: {invalid_customer_refs:,}")
print(f"Invalid Bank References    : {invalid_bank_refs:,}")

print("\nCleaned Files Created:")

print(f"  - {BANKS_OUTPUT_FILE}")
print(f"  - {CUSTOMERS_OUTPUT_FILE}")
print(f"  - {ACCOUNTS_OUTPUT_FILE}")

print("\nFinal Row Counts:")

print(f"  Banks    : {len(banks_df):,}")
print(f"  Customers: {len(customers_df):,}")
print(f"  Accounts : {len(cleaned_accounts_df):,}")

print("\nSTEP 1: CLEAN ACCOUNTS DATASET COMPLETED SUCCESSFULLY.")

