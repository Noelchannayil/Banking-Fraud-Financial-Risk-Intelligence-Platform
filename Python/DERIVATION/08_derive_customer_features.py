# ============================================================
# 08_DERIVE_CUSTOMER_FEATURES.PY
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

CUSTOMERS_FILE = CLEANED_DIR / "customers.csv"

ACCOUNT_FEATURES_FILE = (
    DERIVED_DIR / "account_features.csv"
)


# ============================================================
# OUTPUT FILE
# ============================================================

CUSTOMER_FEATURES_FILE = (
    DERIVED_DIR / "customer_features.csv"
)


# ============================================================
# CONSTANTS
# ============================================================

EXPECTED_CUSTOMER_COUNT = 166_207

EXPECTED_ACCOUNT_FEATURE_COUNT = 518_581

# ============================================================
# STEP 1
# LOAD AND VALIDATE INPUTS
# ============================================================

print("\n" + "=" * 70)
print("STEP 1: LOAD AND VALIDATE INPUTS")
print("=" * 70)


required_files = {

    "customers": CUSTOMERS_FILE,

    "account_features": ACCOUNT_FEATURES_FILE

}


print("\nChecking required input files...\n")


for name, path in required_files.items():

    if not path.exists():

        raise FileNotFoundError(

            f"{name} file not found:\n{path}"

        )

    print(f"✓ {name}")


print("\nLoading datasets...\n")


customers_df = pd.read_csv(

    CUSTOMERS_FILE

)

account_features_df = pd.read_csv(

    ACCOUNT_FEATURES_FILE

)


print("Dataset Summary\n")


print(

    f"Customers          : "

    f"{len(customers_df):,}"

)

print(

    f"Account Features   : "

    f"{len(account_features_df):,}"

)


assert (

    len(customers_df)

    ==

    EXPECTED_CUSTOMER_COUNT

)

assert (

    len(account_features_df)

    ==

    EXPECTED_ACCOUNT_FEATURE_COUNT

)


print("\nSTEP 1 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 2
# VALIDATE ACCOUNT FEATURE DATASET
# ============================================================

print("\n" + "=" * 70)
print("STEP 2: VALIDATE ACCOUNT FEATURE DATASET")
print("=" * 70)


# ------------------------------------------------------------
# EXPECTED ACCOUNT FEATURE COLUMNS
# ------------------------------------------------------------

EXPECTED_ACCOUNT_FEATURE_COLUMNS = [

    "account_id",

    "customer_id",

    "bank_id",

    "sent_transaction_count",

    "received_transaction_count",

    "total_transactions",

    "total_amount_sent",

    "total_amount_received",

    "average_amount_sent",

    "average_amount_received",

    "maximum_amount_sent",

    "maximum_amount_received",

    "minimum_amount_sent",

    "minimum_amount_received",

    "night_transaction_count",

    "weekend_transaction_count",

    "cross_bank_transaction_count",

    "self_transfer_count",

    "currency_mismatch_count",

    "known_aml_pattern_transaction_count",

    "laundering_transaction_count",

    "first_transaction_timestamp",

    "last_transaction_timestamp"

]


# ------------------------------------------------------------
# VALIDATE SCHEMA
# ------------------------------------------------------------

actual_columns = account_features_df.columns.tolist()

missing_columns = [

    column

    for column in EXPECTED_ACCOUNT_FEATURE_COLUMNS

    if column not in actual_columns

]


unexpected_columns = [

    column

    for column in actual_columns

    if column not in EXPECTED_ACCOUNT_FEATURE_COLUMNS

]


print("\nSchema Validation\n")

print(f"Expected Columns : {len(EXPECTED_ACCOUNT_FEATURE_COLUMNS)}")

print(f"Actual Columns   : {len(actual_columns)}")

print(f"Missing Columns  : {missing_columns}")

print(f"Unexpected Columns : {unexpected_columns}")


if missing_columns:

    raise ValueError(

        "Missing columns detected in account_features.csv"

    )


print("\nSTEP 2 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 3
# CONFIGURE CUSTOMER FEATURE CONTRACT
# ============================================================

print("\n" + "=" * 70)
print("STEP 3: CONFIGURE CUSTOMER FEATURE CONTRACT")
print("=" * 70)


# ------------------------------------------------------------
# CUSTOMER IDENTIFIER COLUMNS
# ------------------------------------------------------------

CUSTOMER_IDENTIFIER_COLUMNS = [

    "customer_id"

]


# ------------------------------------------------------------
# ACCOUNT FEATURES
# ------------------------------------------------------------

CUSTOMER_ACCOUNT_FEATURE_COLUMNS = [

    "total_accounts"

]


# ------------------------------------------------------------
# TRANSACTION FEATURES
# ------------------------------------------------------------

CUSTOMER_TRANSACTION_FEATURE_COLUMNS = [

    "total_sent_transactions",

    "total_received_transactions",

    "total_transactions"

]


# ------------------------------------------------------------
# MONETARY FEATURES
# ------------------------------------------------------------

CUSTOMER_MONETARY_FEATURE_COLUMNS = [

    "total_amount_sent",

    "total_amount_received",

    "average_amount_sent",

    "average_amount_received"

]


# ------------------------------------------------------------
# AML FEATURES
# ------------------------------------------------------------

CUSTOMER_AML_FEATURE_COLUMNS = [

    "known_aml_pattern_transaction_count",

    "laundering_transaction_count"

]


# ------------------------------------------------------------
# FINAL CUSTOMER FEATURE SCHEMA
# ------------------------------------------------------------

CUSTOMER_FEATURE_COLUMNS = (

    CUSTOMER_IDENTIFIER_COLUMNS

    +

    CUSTOMER_ACCOUNT_FEATURE_COLUMNS

    +

    CUSTOMER_TRANSACTION_FEATURE_COLUMNS

    +

    CUSTOMER_MONETARY_FEATURE_COLUMNS

    +

    CUSTOMER_AML_FEATURE_COLUMNS

)


# ------------------------------------------------------------
# VALIDATE DUPLICATE COLUMN NAMES
# ------------------------------------------------------------

duplicate_columns = [

    column

    for column in CUSTOMER_FEATURE_COLUMNS

    if CUSTOMER_FEATURE_COLUMNS.count(column) > 1

]

duplicate_columns = sorted(set(duplicate_columns))


print("\nCustomer Feature Contract\n")

print(

    f"Identifier Columns : "

    f"{len(CUSTOMER_IDENTIFIER_COLUMNS)}"

)

print(

    f"Account Features   : "

    f"{len(CUSTOMER_ACCOUNT_FEATURE_COLUMNS)}"

)

print(

    f"Transaction Features : "

    f"{len(CUSTOMER_TRANSACTION_FEATURE_COLUMNS)}"

)

print(

    f"Monetary Features  : "

    f"{len(CUSTOMER_MONETARY_FEATURE_COLUMNS)}"

)

print(

    f"AML Features       : "

    f"{len(CUSTOMER_AML_FEATURE_COLUMNS)}"

)

print(

    f"Total Columns      : "

    f"{len(CUSTOMER_FEATURE_COLUMNS)}"

)

print(

    f"Duplicate Columns  : "

    f"{duplicate_columns}"

)


if duplicate_columns:

    raise ValueError(

        "Duplicate columns detected."

    )


print("\nSTEP 3 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 4
# AGGREGATE CUSTOMER STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("STEP 4: AGGREGATE CUSTOMER STATISTICS")
print("=" * 70)


# ------------------------------------------------------------
# AGGREGATE CUSTOMER FEATURES
# ------------------------------------------------------------

customer_features_df = (

    account_features_df

    .groupby("customer_id")

    .agg(

        total_accounts=(

            "account_id",

            "count"

        ),

        total_sent_transactions=(

            "sent_transaction_count",

            "sum"

        ),

        total_received_transactions=(

            "received_transaction_count",

            "sum"

        ),

        total_transactions=(

            "total_transactions",

            "sum"

        ),

        total_amount_sent=(

            "total_amount_sent",

            "sum"

        ),

        total_amount_received=(

            "total_amount_received",

            "sum"

        ),

        average_amount_sent=(

            "average_amount_sent",

            "mean"

        ),

        average_amount_received=(

            "average_amount_received",

            "mean"

        ),

        known_aml_pattern_transaction_count=(

            "known_aml_pattern_transaction_count",

            "sum"

        ),

        laundering_transaction_count=(

            "laundering_transaction_count",

            "sum"

        )

    )

    .reset_index()

)


# ------------------------------------------------------------
# DISPLAY SUMMARY
# ------------------------------------------------------------

print("\nCustomer Aggregation Summary\n")

print(
    f"Customers Aggregated : "
    f"{len(customer_features_df):,}"
)

print(
    f"Expected Customers   : "
    f"{EXPECTED_CUSTOMER_COUNT:,}"
)


assert (

    len(customer_features_df)

    ==

    EXPECTED_CUSTOMER_COUNT

)


print("\nSTEP 4 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 5
# VALIDATE CUSTOMER FEATURE DATASET
# ============================================================

print("\n" + "=" * 70)
print("STEP 5: VALIDATE CUSTOMER FEATURE DATASET")
print("=" * 70)


# ------------------------------------------------------------
# VALIDATE ROW COUNT
# ------------------------------------------------------------

assert len(customer_features_df) == EXPECTED_CUSTOMER_COUNT


# ------------------------------------------------------------
# VALIDATE DUPLICATE CUSTOMER IDS
# ------------------------------------------------------------

duplicate_customers = (

    customer_features_df["customer_id"]

    .duplicated()

    .sum()

)

assert duplicate_customers == 0


# ------------------------------------------------------------
# VALIDATE MISSING CUSTOMER IDS
# ------------------------------------------------------------

missing_customer_ids = (

    customer_features_df["customer_id"]

    .isna()

    .sum()

)

assert missing_customer_ids == 0


# ------------------------------------------------------------
# VALIDATE MISSING NUMERIC VALUES
# ------------------------------------------------------------

numeric_columns = customer_features_df.select_dtypes(

    include=[np.number]

).columns

missing_numeric_values = (

    customer_features_df[numeric_columns]

    .isna()

    .sum()

    .sum()

)

assert missing_numeric_values == 0


# ------------------------------------------------------------
# DISPLAY VALIDATION SUMMARY
# ------------------------------------------------------------

print("\nValidation Summary\n")

print(f"Rows                     : {len(customer_features_df):,}")

print(f"Duplicate Customer IDs   : {duplicate_customers}")

print(f"Missing Customer IDs     : {missing_customer_ids}")

print(f"Missing Numeric Values   : {missing_numeric_values}")

print("\nAll validation checks passed.")

print("\nSTEP 5 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 6
# EXPORT CUSTOMER FEATURES DATASET
# ============================================================

print("\n" + "=" * 70)
print("STEP 6: EXPORT CUSTOMER FEATURES DATASET")
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

customer_features_df.to_csv(

    CUSTOMER_FEATURES_FILE,

    index=False

)


# ------------------------------------------------------------
# EXPORT SUMMARY
# ------------------------------------------------------------

print("\nExport Summary\n")

print(f"Output File : {CUSTOMER_FEATURES_FILE}")

print(f"Rows        : {len(customer_features_df):,}")

print(f"Columns     : {len(customer_features_df.columns)}")

print("\nCustomer feature dataset exported successfully.")

print("\nSTEP 6 COMPLETED SUCCESSFULLY.")

