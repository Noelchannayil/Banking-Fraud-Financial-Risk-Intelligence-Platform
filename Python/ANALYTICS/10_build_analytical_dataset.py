# ============================================================
# 10_BUILD_ANALYTICAL_DATASET.PY
# Banking Fraud Detection & Financial Risk Intelligence Platform
# ============================================================

from pathlib import Path

import pandas as pd
import numpy as np


# ============================================================
# DIRECTORY CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "DATA"

DERIVED_DIR = DATA_DIR / "DERIVED"

ANALYTICS_DIR = DATA_DIR / "ANALYTICS"


# ============================================================
# INPUT FILES
# ============================================================

ACCOUNT_FEATURES_FILE = (
    DERIVED_DIR / "account_features.csv"
)

CUSTOMER_FEATURES_FILE = (
    DERIVED_DIR / "customer_features.csv"
)

NETWORK_FEATURES_FILE = (
    DERIVED_DIR / "network_features.csv"
)


# ============================================================
# OUTPUT FILE
# ============================================================

ANALYTICAL_DATASET_FILE = (
    ANALYTICS_DIR / "analytical_dataset.csv"
)


# ============================================================
# CONSTANTS
# ============================================================

EXPECTED_ACCOUNT_COUNT = 518_581

EXPECTED_CUSTOMER_COUNT = 166_207

# ============================================================
# STEP 1
# LOAD AND VALIDATE INPUTS
# ============================================================

print("\n" + "=" * 70)
print("STEP 1: LOAD AND VALIDATE INPUTS")
print("=" * 70)


required_files = {

    "account_features": ACCOUNT_FEATURES_FILE,

    "customer_features": CUSTOMER_FEATURES_FILE,

    "network_features": NETWORK_FEATURES_FILE

}


print("\nChecking required input files...\n")


for name, path in required_files.items():

    if not path.exists():

        raise FileNotFoundError(

            f"{name} file not found:\n{path}"

        )

    print(f"✓ {name}")


print("\nLoading datasets...\n")


account_features_df = pd.read_csv(

    ACCOUNT_FEATURES_FILE

)

customer_features_df = pd.read_csv(

    CUSTOMER_FEATURES_FILE

)

network_features_df = pd.read_csv(

    NETWORK_FEATURES_FILE

)


print("Dataset Summary\n")

print(
    f"Account Features   : "
    f"{len(account_features_df):,}"
)

print(
    f"Customer Features  : "
    f"{len(customer_features_df):,}"
)

print(
    f"Network Features   : "
    f"{len(network_features_df):,}"
)


assert len(account_features_df) == EXPECTED_ACCOUNT_COUNT
assert len(customer_features_df) == EXPECTED_CUSTOMER_COUNT
assert len(network_features_df) == EXPECTED_ACCOUNT_COUNT


print("\nSTEP 1 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 2
# VALIDATE FEATURE DATASETS
# ============================================================

print("\n" + "=" * 70)
print("STEP 2: VALIDATE FEATURE DATASETS")
print("=" * 70)


# ------------------------------------------------------------
# REQUIRED KEY COLUMNS
# ------------------------------------------------------------

required_account_columns = [

    "account_id",

    "customer_id"

]

required_customer_columns = [

    "customer_id"

]

required_network_columns = [

    "account_id"

]


# ------------------------------------------------------------
# VALIDATE ACCOUNT FEATURES
# ------------------------------------------------------------

missing_account_columns = [

    column

    for column in required_account_columns

    if column not in account_features_df.columns

]


# ------------------------------------------------------------
# VALIDATE CUSTOMER FEATURES
# ------------------------------------------------------------

missing_customer_columns = [

    column

    for column in required_customer_columns

    if column not in customer_features_df.columns

]


# ------------------------------------------------------------
# VALIDATE NETWORK FEATURES
# ------------------------------------------------------------

missing_network_columns = [

    column

    for column in required_network_columns

    if column not in network_features_df.columns

]


print("\nValidation Summary\n")

print(f"Missing Account Columns  : {missing_account_columns}")

print(f"Missing Customer Columns : {missing_customer_columns}")

print(f"Missing Network Columns  : {missing_network_columns}")


if missing_account_columns:

    raise ValueError("Missing columns in account_features.csv")

if missing_customer_columns:

    raise ValueError("Missing columns in customer_features.csv")

if missing_network_columns:

    raise ValueError("Missing columns in network_features.csv")


print("\nSTEP 2 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 3
# CONFIGURE ANALYTICAL DATASET SCHEMA
# ============================================================

print("\n" + "=" * 70)
print("STEP 3: CONFIGURE ANALYTICAL DATASET SCHEMA")
print("=" * 70)


# ------------------------------------------------------------
# PRIMARY KEY COLUMNS
# ------------------------------------------------------------

PRIMARY_COLUMNS = [

    "account_id",

    "customer_id",

    "bank_id"

]


# ------------------------------------------------------------
# ACCOUNT FEATURE COLUMNS
# ------------------------------------------------------------

ACCOUNT_COLUMNS = [

    "sent_transaction_count",

    "received_transaction_count",

    "total_transactions",

    "total_amount_sent",

    "total_amount_received",

    "average_amount_sent",

    "average_amount_received"

]


# ------------------------------------------------------------
# CUSTOMER FEATURE COLUMNS
# ------------------------------------------------------------

CUSTOMER_COLUMNS = [

    "total_accounts"

]


# ------------------------------------------------------------
# NETWORK FEATURE COLUMNS
# ------------------------------------------------------------

NETWORK_COLUMNS = [

    "unique_receivers",

    "unique_senders",

    "out_degree",

    "in_degree",

    "total_degree",

    "total_outgoing_transactions",

    "total_incoming_transactions",

    "self_loop_transactions",

    "cross_bank_connections"

]


# ------------------------------------------------------------
# FINAL ANALYTICAL SCHEMA
# ------------------------------------------------------------

ANALYTICAL_COLUMNS = (

    PRIMARY_COLUMNS

    +

    ACCOUNT_COLUMNS

    +

    CUSTOMER_COLUMNS

    +

    NETWORK_COLUMNS

)


duplicate_columns = [

    column

    for column in ANALYTICAL_COLUMNS

    if ANALYTICAL_COLUMNS.count(column) > 1

]

duplicate_columns = sorted(set(duplicate_columns))


print("\nAnalytical Dataset Schema\n")

print(f"Primary Columns  : {len(PRIMARY_COLUMNS)}")

print(f"Account Features : {len(ACCOUNT_COLUMNS)}")

print(f"Customer Features: {len(CUSTOMER_COLUMNS)}")

print(f"Network Features : {len(NETWORK_COLUMNS)}")

print(f"Total Columns    : {len(ANALYTICAL_COLUMNS)}")

print(f"Duplicate Columns: {duplicate_columns}")


if duplicate_columns:

    raise ValueError(

        "Duplicate columns detected."

    )


print("\nSTEP 3 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 4
# BUILD ANALYTICAL DATASET
# ============================================================

print("\n" + "=" * 70)
print("STEP 4: BUILD ANALYTICAL DATASET")
print("=" * 70)


# ------------------------------------------------------------
# SELECT REQUIRED ACCOUNT COLUMNS
# ------------------------------------------------------------

account_dataset = account_features_df[[
    "account_id",
    "customer_id",
    "bank_id",
    "sent_transaction_count",
    "received_transaction_count",
    "total_transactions",
    "total_amount_sent",
    "total_amount_received",
    "average_amount_sent",
    "average_amount_received"
]].copy()


# ------------------------------------------------------------
# SELECT REQUIRED CUSTOMER COLUMNS
# ------------------------------------------------------------

customer_dataset = customer_features_df[[
    "customer_id",
    "total_accounts"
]].copy()


# ------------------------------------------------------------
# SELECT REQUIRED NETWORK COLUMNS
# ------------------------------------------------------------

network_dataset = network_features_df[[
    "account_id",
    "unique_receivers",
    "unique_senders",
    "out_degree",
    "in_degree",
    "total_degree",
    "total_outgoing_transactions",
    "total_incoming_transactions",
    "self_loop_transactions",
    "cross_bank_connections"
]].copy()


# ------------------------------------------------------------
# MERGE CUSTOMER FEATURES
# ------------------------------------------------------------

analytical_dataset_df = account_dataset.merge(

    customer_dataset,

    on="customer_id",

    how="left"

)


# ------------------------------------------------------------
# MERGE NETWORK FEATURES
# ------------------------------------------------------------

analytical_dataset_df = analytical_dataset_df.merge(

    network_dataset,

    on="account_id",

    how="left"

)


# ------------------------------------------------------------
# REPLACE MISSING VALUES
# ------------------------------------------------------------

numeric_columns = analytical_dataset_df.select_dtypes(

    include=[np.number]

).columns

analytical_dataset_df[numeric_columns] = (

    analytical_dataset_df[numeric_columns]

    .fillna(0)

)


# ------------------------------------------------------------
# DISPLAY SUMMARY
# ------------------------------------------------------------

print("\nAnalytical Dataset Summary\n")

print(f"Rows    : {len(analytical_dataset_df):,}")

print(f"Columns : {len(analytical_dataset_df.columns)}")

print("\nSTEP 4 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 5
# VALIDATE ANALYTICAL DATASET
# ============================================================

print("\n" + "=" * 70)
print("STEP 5: VALIDATE ANALYTICAL DATASET")
print("=" * 70)


# ------------------------------------------------------------
# VALIDATE ROW COUNT
# ------------------------------------------------------------

assert len(analytical_dataset_df) == EXPECTED_ACCOUNT_COUNT


# ------------------------------------------------------------
# VALIDATE DUPLICATE ACCOUNT IDS
# ------------------------------------------------------------

duplicate_accounts = (

    analytical_dataset_df["account_id"]

    .duplicated()

    .sum()

)

assert duplicate_accounts == 0


# ------------------------------------------------------------
# VALIDATE MISSING ACCOUNT IDS
# ------------------------------------------------------------

missing_account_ids = (

    analytical_dataset_df["account_id"]

    .isna()

    .sum()

)

assert missing_account_ids == 0


# ------------------------------------------------------------
# VALIDATE MISSING NUMERIC VALUES
# ------------------------------------------------------------

numeric_columns = analytical_dataset_df.select_dtypes(

    include=[np.number]

).columns

missing_numeric_values = (

    analytical_dataset_df[numeric_columns]

    .isna()

    .sum()

    .sum()

)

assert missing_numeric_values == 0


# ------------------------------------------------------------
# DISPLAY VALIDATION SUMMARY
# ------------------------------------------------------------

print("\nValidation Summary\n")

print(f"Rows                   : {len(analytical_dataset_df):,}")

print(f"Duplicate Account IDs  : {duplicate_accounts}")

print(f"Missing Account IDs    : {missing_account_ids}")

print(f"Missing Numeric Values : {missing_numeric_values}")

print("\nAll validation checks passed.")

print("\nSTEP 5 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 6
# EXPORT ANALYTICAL DATASET
# ============================================================

print("\n" + "=" * 70)
print("STEP 6: EXPORT ANALYTICAL DATASET")
print("=" * 70)


# ------------------------------------------------------------
# CREATE OUTPUT DIRECTORY
# ------------------------------------------------------------

ANALYTICS_DIR.mkdir(

    parents=True,

    exist_ok=True

)


# ------------------------------------------------------------
# EXPORT DATASET
# ------------------------------------------------------------

analytical_dataset_df.to_csv(

    ANALYTICAL_DATASET_FILE,

    index=False

)


# ------------------------------------------------------------
# EXPORT SUMMARY
# ------------------------------------------------------------

print("\nExport Summary\n")

print(f"Output File : {ANALYTICAL_DATASET_FILE}")

print(f"Rows        : {len(analytical_dataset_df):,}")

print(f"Columns     : {len(analytical_dataset_df.columns)}")

print("\nAnalytical dataset exported successfully.")

print("\nSTEP 6 COMPLETED SUCCESSFULLY.")

