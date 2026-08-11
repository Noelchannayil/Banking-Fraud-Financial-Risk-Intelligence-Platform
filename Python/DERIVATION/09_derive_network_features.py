# ============================================================
# 09_DERIVE_NETWORK_FEATURES.PY
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

CLEANED_DIR = DATA_DIR / "CLEANED"

DERIVED_DIR = DATA_DIR / "DERIVED"


# ============================================================
# INPUT FILES
# ============================================================

TRANSACTION_FEATURES_FILE = (
    DERIVED_DIR / "transaction_features.csv"
)

ACCOUNT_FEATURES_FILE = (
    DERIVED_DIR / "account_features.csv"
)

CUSTOMER_FEATURES_FILE = (
    DERIVED_DIR / "customer_features.csv"
)


# ============================================================
# OUTPUT FILE
# ============================================================

NETWORK_FEATURES_FILE = (
    DERIVED_DIR / "network_features.csv"
)


# ============================================================
# CONSTANTS
# ============================================================

EXPECTED_TRANSACTION_COUNT = 3_000_000

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

    "transaction_features": TRANSACTION_FEATURES_FILE,

    "account_features": ACCOUNT_FEATURES_FILE,

    "customer_features": CUSTOMER_FEATURES_FILE

}


print("\nChecking required input files...\n")


for name, path in required_files.items():

    if not path.exists():

        raise FileNotFoundError(

            f"{name} file not found:\n{path}"

        )

    print(f"✓ {name}")


print("\nLoading datasets...\n")


transaction_features_sample_df = pd.read_csv(

    TRANSACTION_FEATURES_FILE,

    nrows=10

)

account_features_df = pd.read_csv(

    ACCOUNT_FEATURES_FILE

)

customer_features_df = pd.read_csv(

    CUSTOMER_FEATURES_FILE

)


print("Dataset Summary\n")


print(

    f"Transaction Sample : "

    f"{len(transaction_features_sample_df):,}"

)

print(

    f"Account Features   : "

    f"{len(account_features_df):,}"

)

print(

    f"Customer Features  : "

    f"{len(customer_features_df):,}"

)


assert len(transaction_features_sample_df) == 10
assert len(account_features_df) == EXPECTED_ACCOUNT_COUNT
assert len(customer_features_df) == EXPECTED_CUSTOMER_COUNT


print("\nSTEP 1 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 2
# VALIDATE TRANSACTION FEATURE DATASET
# ============================================================

print("\n" + "=" * 70)
print("STEP 2: VALIDATE TRANSACTION FEATURE DATASET")
print("=" * 70)


# ------------------------------------------------------------
# EXPECTED TRANSACTION FEATURE COLUMNS
# ------------------------------------------------------------

EXPECTED_TRANSACTION_FEATURE_COLUMNS = [

    "transaction_id",
    "timestamp",
    "sender_account_id",
    "receiver_account_id",
    "from_bank_id",
    "to_bank_id",
    "amount_received",
    "receiving_currency",
    "amount_paid",
    "payment_currency",
    "payment_format",
    "transaction_date",
    "transaction_hour",
    "transaction_day_of_week",
    "transaction_day_of_month",
    "is_weekend",
    "is_night_transaction",
    "is_cross_bank_transaction",
    "is_self_transfer",
    "is_currency_mismatch",
    "amount_difference",
    "amount_ratio",
    "log_amount_paid",
    "log_amount_received",
    "is_known_aml_pattern_transaction",
    "is_laundering"

]


# ------------------------------------------------------------
# VALIDATE SCHEMA
# ------------------------------------------------------------

actual_columns = transaction_features_sample_df.columns.tolist()

missing_columns = [

    column

    for column in EXPECTED_TRANSACTION_FEATURE_COLUMNS

    if column not in actual_columns

]

unexpected_columns = [

    column

    for column in actual_columns

    if column not in EXPECTED_TRANSACTION_FEATURE_COLUMNS

]


print("\nSchema Validation\n")

print(f"Expected Columns : {len(EXPECTED_TRANSACTION_FEATURE_COLUMNS)}")

print(f"Actual Columns   : {len(actual_columns)}")

print(f"Missing Columns  : {missing_columns}")

print(f"Unexpected Columns : {unexpected_columns}")


if missing_columns:

    raise ValueError(

        "Missing columns detected in transaction_features.csv"

    )


# ------------------------------------------------------------
# VALIDATE TIMESTAMP
# ------------------------------------------------------------

transaction_features_sample_df["timestamp"] = pd.to_datetime(

    transaction_features_sample_df["timestamp"],

    errors="coerce"

)

assert transaction_features_sample_df["timestamp"].isna().sum() == 0


print("\nSTEP 2 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 3
# CONFIGURE NETWORK FEATURE CONTRACT
# ============================================================

print("\n" + "=" * 70)
print("STEP 3: CONFIGURE NETWORK FEATURE CONTRACT")
print("=" * 70)


# ------------------------------------------------------------
# ACCOUNT IDENTIFIER COLUMNS
# ------------------------------------------------------------

NETWORK_IDENTIFIER_COLUMNS = [

    "account_id"

]


# ------------------------------------------------------------
# CONNECTIVITY FEATURES
# ------------------------------------------------------------

NETWORK_CONNECTIVITY_COLUMNS = [

    "unique_receivers",

    "unique_senders",

    "out_degree",

    "in_degree",

    "total_degree"

]


# ------------------------------------------------------------
# TRANSACTION FEATURES
# ------------------------------------------------------------

NETWORK_TRANSACTION_COLUMNS = [

    "total_outgoing_transactions",

    "total_incoming_transactions"

]


# ------------------------------------------------------------
# RISK FEATURES
# ------------------------------------------------------------

NETWORK_RISK_COLUMNS = [

    "self_loop_transactions",

    "cross_bank_connections"

]


# ------------------------------------------------------------
# FINAL NETWORK FEATURE SCHEMA
# ------------------------------------------------------------

NETWORK_FEATURE_COLUMNS = (

    NETWORK_IDENTIFIER_COLUMNS

    +

    NETWORK_CONNECTIVITY_COLUMNS

    +

    NETWORK_TRANSACTION_COLUMNS

    +

    NETWORK_RISK_COLUMNS

)


# ------------------------------------------------------------
# VALIDATE DUPLICATE COLUMN NAMES
# ------------------------------------------------------------

duplicate_columns = [

    column

    for column in NETWORK_FEATURE_COLUMNS

    if NETWORK_FEATURE_COLUMNS.count(column) > 1

]

duplicate_columns = sorted(set(duplicate_columns))


print("\nNetwork Feature Contract\n")

print(f"Identifier Columns   : {len(NETWORK_IDENTIFIER_COLUMNS)}")

print(f"Connectivity Features: {len(NETWORK_CONNECTIVITY_COLUMNS)}")

print(f"Transaction Features : {len(NETWORK_TRANSACTION_COLUMNS)}")

print(f"Risk Features        : {len(NETWORK_RISK_COLUMNS)}")

print(f"Total Columns        : {len(NETWORK_FEATURE_COLUMNS)}")

print(f"Duplicate Columns    : {duplicate_columns}")


if duplicate_columns:

    raise ValueError(

        "Duplicate columns detected."

    )


print("\nSTEP 3 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 4
# BUILD NETWORK FEATURES
# ============================================================

print("\n" + "=" * 70)
print("STEP 4: BUILD NETWORK FEATURES")
print("=" * 70)


# ------------------------------------------------------------
# LOAD REQUIRED COLUMNS
# ------------------------------------------------------------

transactions_df = pd.read_csv(

    TRANSACTION_FEATURES_FILE,

    usecols=[

        "sender_account_id",

        "receiver_account_id",

        "is_self_transfer",

        "is_cross_bank_transaction"

    ]

)


# ------------------------------------------------------------
# OUTGOING NETWORK FEATURES
# ------------------------------------------------------------

outgoing_df = (

    transactions_df

    .groupby("sender_account_id")

    .agg(

        unique_receivers=(

            "receiver_account_id",

            "nunique"

        ),

        total_outgoing_transactions=(

            "receiver_account_id",

            "count"

        ),

        self_loop_transactions=(

            "is_self_transfer",

            "sum"

        ),

        cross_bank_connections=(

            "is_cross_bank_transaction",

            "sum"

        )

    )

    .reset_index()

    .rename(

        columns={

            "sender_account_id": "account_id"

        }

    )

)


# ------------------------------------------------------------
# INCOMING NETWORK FEATURES
# ------------------------------------------------------------

incoming_df = (

    transactions_df

    .groupby("receiver_account_id")

    .agg(

        unique_senders=(

            "sender_account_id",

            "nunique"

        ),

        total_incoming_transactions=(

            "sender_account_id",

            "count"

        )

    )

    .reset_index()

    .rename(

        columns={

            "receiver_account_id": "account_id"

        }

    )

)


# ------------------------------------------------------------
# MERGE NETWORK FEATURES
# ------------------------------------------------------------

network_features_df = account_features_df[["account_id"]].copy()

network_features_df = network_features_df.merge(

    outgoing_df,

    on="account_id",

    how="left"

)

network_features_df = network_features_df.merge(

    incoming_df,

    on="account_id",

    how="left"

)


# ------------------------------------------------------------
# REPLACE MISSING VALUES
# ------------------------------------------------------------

numeric_columns = network_features_df.select_dtypes(

    include=[np.number]

).columns

network_features_df[numeric_columns] = (

    network_features_df[numeric_columns]

    .fillna(0)

)


# ------------------------------------------------------------
# DERIVE DEGREE FEATURES
# ------------------------------------------------------------

network_features_df["out_degree"] = (

    network_features_df["unique_receivers"]

)

network_features_df["in_degree"] = (

    network_features_df["unique_senders"]

)

network_features_df["total_degree"] = (

    network_features_df["out_degree"]

    +

    network_features_df["in_degree"]

)


# ------------------------------------------------------------
# DISPLAY SUMMARY
# ------------------------------------------------------------

print("\nNetwork Feature Summary\n")

print(f"Rows    : {len(network_features_df):,}")

print(f"Columns : {len(network_features_df.columns)}")

print("\nSTEP 4 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 5
# VALIDATE NETWORK FEATURE DATASET
# ============================================================

print("\n" + "=" * 70)
print("STEP 5: VALIDATE NETWORK FEATURE DATASET")
print("=" * 70)


# ------------------------------------------------------------
# VALIDATE ROW COUNT
# ------------------------------------------------------------

assert len(network_features_df) == EXPECTED_ACCOUNT_COUNT


# ------------------------------------------------------------
# VALIDATE DUPLICATE ACCOUNT IDS
# ------------------------------------------------------------

duplicate_accounts = (

    network_features_df["account_id"]

    .duplicated()

    .sum()

)

assert duplicate_accounts == 0


# ------------------------------------------------------------
# VALIDATE MISSING ACCOUNT IDS
# ------------------------------------------------------------

missing_account_ids = (

    network_features_df["account_id"]

    .isna()

    .sum()

)

assert missing_account_ids == 0


# ------------------------------------------------------------
# VALIDATE MISSING NUMERIC VALUES
# ------------------------------------------------------------

numeric_columns = network_features_df.select_dtypes(

    include=[np.number]

).columns

missing_numeric_values = (

    network_features_df[numeric_columns]

    .isna()

    .sum()

    .sum()

)

assert missing_numeric_values == 0


# ------------------------------------------------------------
# DISPLAY VALIDATION SUMMARY
# ------------------------------------------------------------

print("\nValidation Summary\n")

print(f"Rows                   : {len(network_features_df):,}")

print(f"Duplicate Account IDs  : {duplicate_accounts}")

print(f"Missing Account IDs    : {missing_account_ids}")

print(f"Missing Numeric Values : {missing_numeric_values}")

print("\nAll validation checks passed.")

print("\nSTEP 5 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 6
# EXPORT NETWORK FEATURES DATASET
# ============================================================

print("\n" + "=" * 70)
print("STEP 6: EXPORT NETWORK FEATURES DATASET")
print("=" * 70)


# ------------------------------------------------------------
# CREATE OUTPUT DIRECTORY
# ------------------------------------------------------------

DERIVED_DIR.mkdir(

    parents=True,

    exist_ok=True

)


# ------------------------------------------------------------
# EXPORT DATASET
# ------------------------------------------------------------

network_features_df.to_csv(

    NETWORK_FEATURES_FILE,

    index=False

)


# ------------------------------------------------------------
# EXPORT SUMMARY
# ------------------------------------------------------------

print("\nExport Summary\n")

print(f"Output File : {NETWORK_FEATURES_FILE}")

print(f"Rows        : {len(network_features_df):,}")

print(f"Columns     : {len(network_features_df.columns)}")

print("\nNetwork feature dataset exported successfully.")

print("\nSTEP 6 COMPLETED SUCCESSFULLY.")

