from pathlib import Path

import pandas as pd
import numpy as np

# ==========================================================
# BANKING FRAUD & FINANCIAL RISK INTELLIGENCE PLATFORM
# PHASE 3: FEATURE DERIVATION & ANALYTICAL DATA CONSTRUCTION
# STEP 1: CONFIGURE AND VERIFY DERIVATION INPUTS
# ==========================================================

print("\n" + "=" * 70)

print(
    "BANKING FRAUD & FINANCIAL RISK INTELLIGENCE PLATFORM"
)

print(
    "PHASE 3: FEATURE DERIVATION & ANALYTICAL DATA CONSTRUCTION"
)

print(
    "STEP 1: CONFIGURE AND VERIFY DERIVATION INPUTS"
)

print("=" * 70)


# ----------------------------------------------------------
# PROJECT PATHS
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CLEANED_DATA_DIR = (
    PROJECT_ROOT
    / "DATA"
    / "CLEANED"
)

DERIVED_DATA_DIR = (
    PROJECT_ROOT
    / "DATA"
    / "DERIVED"
)

REPORTS_DIR = (
    PROJECT_ROOT
    / "REPORTS"
)


# ----------------------------------------------------------
# CLEANED INPUT FILES
# ----------------------------------------------------------

BANKS_FILE = (
    CLEANED_DATA_DIR
    / "banks.csv"
)

CUSTOMERS_FILE = (
    CLEANED_DATA_DIR
    / "customers.csv"
)

ACCOUNTS_FILE = (
    CLEANED_DATA_DIR
    / "accounts.csv"
)

TRANSACTIONS_FILE = (
    CLEANED_DATA_DIR
    / "transactions.csv"
)

AML_PATTERNS_FILE = (
    CLEANED_DATA_DIR
    / "aml_patterns.csv"
)

AML_PATTERN_TRANSACTIONS_FILE = (
    CLEANED_DATA_DIR
    / "aml_pattern_transactions.csv"
)


# ----------------------------------------------------------
# DERIVED OUTPUT FILES
# ----------------------------------------------------------

TRANSACTION_FEATURES_FILE = (
    DERIVED_DATA_DIR
    / "transaction_features.csv"
)


# ----------------------------------------------------------
# PROCESSING CONFIGURATION
# ----------------------------------------------------------

TRANSACTION_CHUNK_SIZE = 250_000


# ----------------------------------------------------------
# DISPLAY CONFIGURATION
# ----------------------------------------------------------

print(f"\nProject Root          : {PROJECT_ROOT}")

print(f"Cleaned Data Directory: {CLEANED_DATA_DIR}")

print(f"Derived Data Directory: {DERIVED_DATA_DIR}")

print(f"Reports Directory     : {REPORTS_DIR}")

print(f"Transaction Chunk Size: {TRANSACTION_CHUNK_SIZE:,}")


# ----------------------------------------------------------
# VERIFY CLEANED DATA DIRECTORY
# ----------------------------------------------------------

if not CLEANED_DATA_DIR.exists():

    raise FileNotFoundError(
        f"Cleaned data directory not found: "
        f"{CLEANED_DATA_DIR}"
    )


print(
    "\nCleaned data directory found successfully."
)


# ----------------------------------------------------------
# CREATE DERIVED DATA DIRECTORY
# ----------------------------------------------------------

DERIVED_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


print(
    "Derived data directory is ready."
)


# ----------------------------------------------------------
# VERIFY REQUIRED CLEANED INPUT FILES
# ----------------------------------------------------------

print("\n" + "=" * 70)

print("VERIFYING DERIVATION INPUT FILES")

print("=" * 70)


REQUIRED_INPUT_FILES = {

    "Banks": BANKS_FILE,

    "Customers": CUSTOMERS_FILE,

    "Accounts": ACCOUNTS_FILE,

    "Transactions": TRANSACTIONS_FILE,

    "AML Patterns": AML_PATTERNS_FILE,

    "AML Pattern Transactions":
        AML_PATTERN_TRANSACTIONS_FILE,

}


for dataset_name, file_path in REQUIRED_INPUT_FILES.items():

    if not file_path.exists():

        raise FileNotFoundError(
            f"Required cleaned dataset not found: "
            f"{file_path}"
        )


    file_size_mb = (
        file_path.stat().st_size
        / (1024 ** 2)
    )


    print(
        f"[FOUND] "
        f"{dataset_name:<25} "
        f"{file_path.name:<30} "
        f"{file_size_mb:>10.2f} MB"
    )


print(
    "\nAll required derivation input files were found successfully."
)


# ----------------------------------------------------------
# LOAD SMALLER CLEANED DATASETS
# ----------------------------------------------------------

print("\n" + "=" * 70)

print("LOADING DERIVATION REFERENCE DATASETS")

print("=" * 70)


banks_df = pd.read_csv(
    BANKS_FILE,
    dtype={
        "bank_id": "int64",
        "bank_name": "string",
    },
)


customers_df = pd.read_csv(
    CUSTOMERS_FILE,
    dtype={
        "customer_id": "string",
        "entity_id": "string",
        "entity_name": "string",
    },
)


accounts_df = pd.read_csv(
    ACCOUNTS_FILE,
    dtype={
        "account_id": "string",
        "customer_id": "string",
        "bank_id": "int64",
        "account_number": "string",
        "entity_id": "string",
    },
)


aml_patterns_df = pd.read_csv(
    AML_PATTERNS_FILE,
    dtype={
        "aml_pattern_id": "string",
        "typology": "string",
        "pattern_description": "string",
        "transaction_count": "int64",
    },
)


aml_pattern_transactions_df = pd.read_csv(
    AML_PATTERN_TRANSACTIONS_FILE,
    dtype={
        "pattern_transaction_occurrence_id": "string",
        "aml_pattern_id": "string",
        "transaction_id": "string",
        "pattern_transaction_sequence": "int64",
    },
)


print("\nReference datasets loaded successfully.")

print(
    f"Banks                    : "
    f"{len(banks_df):,}"
)

print(
    f"Customers                : "
    f"{len(customers_df):,}"
)

print(
    f"Accounts                 : "
    f"{len(accounts_df):,}"
)

print(
    f"AML Patterns             : "
    f"{len(aml_patterns_df):,}"
)

print(
    f"AML Pattern Transactions : "
    f"{len(aml_pattern_transactions_df):,}"
)


# ----------------------------------------------------------
# VERIFY EXPECTED REFERENCE ROW COUNTS
# ----------------------------------------------------------

EXPECTED_REFERENCE_ROW_COUNTS = {

    "banks": 30_470,

    "customers": 166_207,

    "accounts": 518_581,

    "aml_patterns": 370,

    "aml_pattern_transactions": 3_209,

}


actual_reference_row_counts = {

    "banks": len(banks_df),

    "customers": len(customers_df),

    "accounts": len(accounts_df),

    "aml_patterns": len(aml_patterns_df),

    "aml_pattern_transactions":
        len(aml_pattern_transactions_df),

}


for dataset_name, expected_count in (
    EXPECTED_REFERENCE_ROW_COUNTS.items()
):

    actual_count = (
        actual_reference_row_counts[
            dataset_name
        ]
    )


    status = (
        "PASS"
        if actual_count == expected_count
        else "FAIL"
    )


    print(
        f"{dataset_name:<25} "
        f"Expected: {expected_count:>9,} | "
        f"Actual: {actual_count:>9,} | "
        f"{status}"
    )


    if actual_count != expected_count:

        raise ValueError(
            f"Unexpected row count for "
            f"{dataset_name}."
        )


print(
    "\nAll derivation reference dataset row counts "
    "validated successfully."
)


print(
    "\nSTEP 1: DERIVATION INPUT CONFIGURATION "
    "COMPLETED SUCCESSFULLY."
)

# ==========================================================
# STEP 2: INSPECT AND VALIDATE TRANSACTION INPUT STRUCTURE
# ==========================================================

print("\n" + "=" * 70)
print("STEP 2: INSPECT AND VALIDATE TRANSACTION INPUT STRUCTURE")
print("=" * 70)


# ----------------------------------------------------------
# EXPECTED TRANSACTION INPUT SCHEMA
# ----------------------------------------------------------

EXPECTED_TRANSACTION_COLUMNS = [

    "transaction_id",

    "timestamp",

    "sender_account_id",

    "receiver_account_id",

    "from_bank_id",

    "to_bank_id",

    "sender_account_number",

    "receiver_account_number",

    "amount_received",

    "receiving_currency",

    "amount_paid",

    "payment_currency",

    "payment_format",

    "is_laundering",

]


# ----------------------------------------------------------
# LOAD TRANSACTION SAMPLE
# ----------------------------------------------------------

transaction_sample_df = pd.read_csv(

    TRANSACTIONS_FILE,

    nrows=10,

    dtype={
        "transaction_id": "string",
        "timestamp": "string",
        "sender_account_id": "string",
        "receiver_account_id": "string",
        "from_bank_id": "int64",
        "to_bank_id": "int64",
        "sender_account_number": "string",
        "receiver_account_number": "string",
        "amount_received": "float64",
        "receiving_currency": "string",
        "amount_paid": "float64",
        "payment_currency": "string",
        "payment_format": "string",
        "is_laundering": "int64",
    },

)


print("\nTransaction sample loaded successfully.")

print(
    f"Sample Rows    : "
    f"{len(transaction_sample_df):,}"
)

print(
    f"Sample Columns : "
    f"{len(transaction_sample_df.columns):,}"
)


# ----------------------------------------------------------
# VALIDATE TRANSACTION COLUMN STRUCTURE
# ----------------------------------------------------------

actual_transaction_columns = (
    transaction_sample_df.columns.tolist()
)


missing_transaction_columns = [

    column_name

    for column_name in EXPECTED_TRANSACTION_COLUMNS

    if column_name not in actual_transaction_columns

]


unexpected_transaction_columns = [

    column_name

    for column_name in actual_transaction_columns

    if column_name not in EXPECTED_TRANSACTION_COLUMNS

]


transaction_column_order_matches = (

    actual_transaction_columns

    ==

    EXPECTED_TRANSACTION_COLUMNS

)


print("\nTransaction Schema Results:")

print(
    f"  Expected Column Count : "
    f"{len(EXPECTED_TRANSACTION_COLUMNS)}"
)

print(
    f"  Actual Column Count   : "
    f"{len(actual_transaction_columns)}"
)

print(
    f"  Missing Columns       : "
    f"{missing_transaction_columns}"
)

print(
    f"  Unexpected Columns    : "
    f"{unexpected_transaction_columns}"
)

print(
    f"  Column Order Matches  : "
    f"{transaction_column_order_matches}"
)


transaction_schema_valid = (

    len(missing_transaction_columns) == 0

    and len(unexpected_transaction_columns) == 0

    and transaction_column_order_matches

)


print(
    f"  Transaction Schema Status: "
    f"{'PASS' if transaction_schema_valid else 'FAIL'}"
)


if not transaction_schema_valid:

    raise ValueError(
        "Transaction input schema validation failed."
    )


# ----------------------------------------------------------
# PARSE SAMPLE TIMESTAMPS
# ----------------------------------------------------------

transaction_sample_df[
    "timestamp"
] = pd.to_datetime(

    transaction_sample_df[
        "timestamp"
    ],

    errors="coerce",

)


invalid_sample_timestamps = int(

    transaction_sample_df[
        "timestamp"
    ]

    .isna()

    .sum()

)


print("\nTransaction Timestamp Sample Results:")

print(
    f"  Invalid Sample Timestamps : "
    f"{invalid_sample_timestamps:,}"
)

print(
    f"  Minimum Sample Timestamp  : "
    f"{transaction_sample_df['timestamp'].min()}"
)

print(
    f"  Maximum Sample Timestamp  : "
    f"{transaction_sample_df['timestamp'].max()}"
)


if invalid_sample_timestamps > 0:

    raise ValueError(
        "Invalid timestamps detected in transaction sample."
    )


# ----------------------------------------------------------
# VERIFY EXPECTED TRANSACTION ROW COUNT
# ----------------------------------------------------------

EXPECTED_TRANSACTION_ROW_COUNT = 5_078_336


print("\nExpected Transaction Rows:")

print(
    f"  {EXPECTED_TRANSACTION_ROW_COUNT:,}"
)


# ----------------------------------------------------------
# DISPLAY SAMPLE INPUT RECORDS
# ----------------------------------------------------------

print("\nFirst 10 Transaction Input Records:")

print(
    transaction_sample_df[
        [
            "transaction_id",
            "timestamp",
            "sender_account_id",
            "receiver_account_id",
            "from_bank_id",
            "to_bank_id",
            "amount_received",
            "amount_paid",
            "payment_format",
            "is_laundering",
        ]
    ]
)


print(
    "\nSTEP 2: TRANSACTION INPUT STRUCTURE "
    "VALIDATED SUCCESSFULLY."
)

# ==========================================================
# STEP 3: DEFINE AND VALIDATE TRANSACTION FEATURE CONTRACT
# ==========================================================

print("\n" + "=" * 70)
print("STEP 3: DEFINE AND VALIDATE TRANSACTION FEATURE CONTRACT")
print("=" * 70)


# ----------------------------------------------------------
# TRANSACTION IDENTIFIER AND SOURCE COLUMNS
# ----------------------------------------------------------

TRANSACTION_BASE_COLUMNS = [

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

]


# ----------------------------------------------------------
# DERIVED TRANSACTION FEATURE COLUMNS
# ----------------------------------------------------------

TRANSACTION_DERIVED_FEATURE_COLUMNS = [

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

]


# ----------------------------------------------------------
# TARGET / REFERENCE COLUMNS
# ----------------------------------------------------------

TRANSACTION_TARGET_COLUMNS = [

    "is_laundering",

]


# ----------------------------------------------------------
# FINAL TRANSACTION FEATURE OUTPUT SCHEMA
# ----------------------------------------------------------

TRANSACTION_FEATURE_COLUMNS = (

    TRANSACTION_BASE_COLUMNS

    + TRANSACTION_DERIVED_FEATURE_COLUMNS

    + TRANSACTION_TARGET_COLUMNS

)


# ----------------------------------------------------------
# VERIFY FEATURE CONTRACT HAS NO DUPLICATE COLUMN NAMES
# ----------------------------------------------------------

duplicate_feature_columns = [

    column_name

    for column_name in TRANSACTION_FEATURE_COLUMNS

    if TRANSACTION_FEATURE_COLUMNS.count(column_name) > 1

]


duplicate_feature_columns = sorted(

    set(duplicate_feature_columns)

)


print("\nTransaction Feature Contract:")

print(
    f"  Base Columns            : "
    f"{len(TRANSACTION_BASE_COLUMNS)}"
)

print(
    f"  Derived Feature Columns : "
    f"{len(TRANSACTION_DERIVED_FEATURE_COLUMNS)}"
)

print(
    f"  Target Columns          : "
    f"{len(TRANSACTION_TARGET_COLUMNS)}"
)

print(
    f"  Final Output Columns    : "
    f"{len(TRANSACTION_FEATURE_COLUMNS)}"
)

print(
    f"  Duplicate Column Names  : "
    f"{duplicate_feature_columns}"
)


if duplicate_feature_columns:

    raise ValueError(
        "Duplicate columns detected in transaction "
        "feature contract."
    )


# ----------------------------------------------------------
# VERIFY REQUIRED SOURCE COLUMNS EXIST
# ----------------------------------------------------------

required_feature_source_columns = [

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

    "is_laundering",

]


missing_feature_source_columns = [

    column_name

    for column_name in required_feature_source_columns

    if column_name not in actual_transaction_columns

]


print(
    f"  Missing Source Columns  : "
    f"{missing_feature_source_columns}"
)


if missing_feature_source_columns:

    raise ValueError(
        "Required source columns for transaction feature "
        "derivation are missing."
    )


# ----------------------------------------------------------
# VERIFY TARGET LEAKAGE CONTROL
# ----------------------------------------------------------

TARGET_COLUMN = "is_laundering"


target_present_in_derived_features = (

    TARGET_COLUMN

    in TRANSACTION_DERIVED_FEATURE_COLUMNS

)


print("\nTarget Leakage Contract:")

print(
    f"  Target Column                    : "
    f"{TARGET_COLUMN}"
)

print(
    f"  Target In Derived Feature List   : "
    f"{target_present_in_derived_features}"
)

print(
    f"  Target Leakage Contract Status   : "
    f"{'PASS' if not target_present_in_derived_features else 'FAIL'}"
)


if target_present_in_derived_features:

    raise ValueError(
        "Target column detected in derived feature list."
    )


# ----------------------------------------------------------
# VERIFY AML MEMBERSHIP FEATURE DEFINITION
# ----------------------------------------------------------

aml_pattern_transaction_id_set = set(

    aml_pattern_transactions_df[
        "transaction_id"
    ]

)


print("\nAML Membership Feature Reference:")

print(
    f"  Unique AML Pattern Transaction IDs : "
    f"{len(aml_pattern_transaction_id_set):,}"
)


if (

    len(aml_pattern_transaction_id_set)

    != len(aml_pattern_transactions_df)

):

    raise ValueError(
        "AML pattern transaction IDs are not unique."
    )


# ----------------------------------------------------------
# DISPLAY FINAL OUTPUT SCHEMA
# ----------------------------------------------------------

print("\nFinal Transaction Feature Output Columns:")


for column_number, column_name in enumerate(

    TRANSACTION_FEATURE_COLUMNS,

    start=1,

):

    print(
        f"  {column_number:>2}. "
        f"{column_name}"
    )


print(
    "\nSTEP 3: TRANSACTION FEATURE CONTRACT "
    "VALIDATED SUCCESSFULLY."
)

# ==========================================================
# STEP 4: DERIVE AND VALIDATE SAMPLE TRANSACTION FEATURES
# ==========================================================

print("\n" + "=" * 70)
print("STEP 4: DERIVE AND VALIDATE SAMPLE TRANSACTION FEATURES")
print("=" * 70)


# ----------------------------------------------------------
# COPY TRANSACTION SAMPLE
# ----------------------------------------------------------

sample_feature_df = transaction_sample_df.copy()


# ----------------------------------------------------------
# DERIVE TEMPORAL FEATURES
# ----------------------------------------------------------

sample_feature_df["transaction_date"] = (

    sample_feature_df["timestamp"]

    .dt.strftime("%Y-%m-%d")

)


sample_feature_df["transaction_hour"] = (

    sample_feature_df["timestamp"]

    .dt.hour

    .astype("int64")

)


sample_feature_df["transaction_day_of_week"] = (

    sample_feature_df["timestamp"]

    .dt.dayofweek

    .astype("int64")

)


sample_feature_df["transaction_day_of_month"] = (

    sample_feature_df["timestamp"]

    .dt.day

    .astype("int64")

)


sample_feature_df["is_weekend"] = (

    sample_feature_df["transaction_day_of_week"]

    .isin([5, 6])

    .astype("int64")

)


# Night window definition:
# 00:00 through 05:59

sample_feature_df["is_night_transaction"] = (

    sample_feature_df["transaction_hour"]

    .between(
        0,
        5,
        inclusive="both",
    )

    .astype("int64")

)


# ----------------------------------------------------------
# DERIVE RELATIONSHIP FEATURES
# ----------------------------------------------------------

sample_feature_df["is_cross_bank_transaction"] = (

    sample_feature_df["from_bank_id"]

    .ne(
        sample_feature_df["to_bank_id"]
    )

    .astype("int64")

)


sample_feature_df["is_self_transfer"] = (

    sample_feature_df["sender_account_id"]

    .eq(
        sample_feature_df["receiver_account_id"]
    )

    .astype("int64")

)


# ----------------------------------------------------------
# DERIVE CURRENCY FEATURES
# ----------------------------------------------------------

sample_feature_df["is_currency_mismatch"] = (

    sample_feature_df["receiving_currency"]

    .ne(
        sample_feature_df["payment_currency"]
    )

    .astype("int64")

)


# ----------------------------------------------------------
# DERIVE AMOUNT FEATURES
# ----------------------------------------------------------

sample_feature_df["amount_difference"] = (

    sample_feature_df["amount_received"]

    -

    sample_feature_df["amount_paid"]

)


sample_feature_df["amount_ratio"] = (

    sample_feature_df["amount_received"]

    /

    sample_feature_df["amount_paid"]

)


sample_feature_df["log_amount_paid"] = (

    sample_feature_df["amount_paid"]

    .map(
        lambda value: __import__("math").log1p(value)
    )

)


sample_feature_df["log_amount_received"] = (

    sample_feature_df["amount_received"]

    .map(
        lambda value: __import__("math").log1p(value)
    )

)


# ----------------------------------------------------------
# DERIVE AML PATTERN MEMBERSHIP FEATURE
# ----------------------------------------------------------

sample_feature_df[
    "is_known_aml_pattern_transaction"
] = (

    sample_feature_df["transaction_id"]

    .isin(
        aml_pattern_transaction_id_set
    )

    .astype("int64")

)


# ----------------------------------------------------------
# APPLY FINAL FEATURE CONTRACT
# ----------------------------------------------------------

sample_feature_df = sample_feature_df[

    TRANSACTION_FEATURE_COLUMNS

].copy()


# ----------------------------------------------------------
# VALIDATE FINAL SAMPLE FEATURE SCHEMA
# ----------------------------------------------------------

sample_feature_columns = (

    sample_feature_df.columns.tolist()

)


sample_feature_schema_valid = (

    sample_feature_columns

    ==

    TRANSACTION_FEATURE_COLUMNS

)


print("\nSample Feature Schema Results:")

print(
    f"  Expected Columns     : "
    f"{len(TRANSACTION_FEATURE_COLUMNS)}"
)

print(
    f"  Actual Columns       : "
    f"{len(sample_feature_columns)}"
)

print(
    f"  Column Order Matches : "
    f"{sample_feature_schema_valid}"
)

print(
    f"  Sample Schema Status : "
    f"{'PASS' if sample_feature_schema_valid else 'FAIL'}"
)


if not sample_feature_schema_valid:

    raise ValueError(
        "Sample transaction feature schema validation failed."
    )


# ----------------------------------------------------------
# VALIDATE MISSING AND NON-FINITE FEATURE VALUES
# ----------------------------------------------------------

sample_missing_values = int(

    sample_feature_df

    .isna()

    .sum()

    .sum()

)


numeric_feature_columns = [

    "amount_difference",

    "amount_ratio",

    "log_amount_paid",

    "log_amount_received",

]


non_finite_numeric_values = 0


for column_name in numeric_feature_columns:

    non_finite_numeric_values += int(

        (

            ~sample_feature_df[column_name]

            .map(__import__("math").isfinite)

        ).sum()

    )


print("\nSample Feature Quality Results:")

print(
    f"  Missing Values             : "
    f"{sample_missing_values:,}"
)

print(
    f"  Non-Finite Numeric Values  : "
    f"{non_finite_numeric_values:,}"
)


if sample_missing_values > 0:

    raise ValueError(
        "Missing values detected in sample features."
    )


if non_finite_numeric_values > 0:

    raise ValueError(
        "Non-finite numeric values detected in sample features."
    )


# ----------------------------------------------------------
# VALIDATE BINARY FEATURE DOMAINS
# ----------------------------------------------------------

BINARY_TRANSACTION_FEATURE_COLUMNS = [

    "is_weekend",

    "is_night_transaction",

    "is_cross_bank_transaction",

    "is_self_transfer",

    "is_currency_mismatch",

    "is_known_aml_pattern_transaction",

]


invalid_binary_feature_values = 0


print("\nSample Binary Feature Domains:")


for column_name in BINARY_TRANSACTION_FEATURE_COLUMNS:

    observed_values = sorted(

        sample_feature_df[
            column_name
        ]

        .unique()

        .tolist()

    )


    invalid_values = [

        value

        for value in observed_values

        if value not in [0, 1]

    ]


    invalid_binary_feature_values += len(
        invalid_values
    )


    print(
        f"  {column_name:<35}: "
        f"{observed_values}"
    )


if invalid_binary_feature_values > 0:

    raise ValueError(
        "Invalid binary feature values detected."
    )


# ----------------------------------------------------------
# DISPLAY SAMPLE DERIVED FEATURES
# ----------------------------------------------------------

print("\nFirst 10 Derived Transaction Feature Records:")

print(

    sample_feature_df[

        [

            "transaction_id",

            "transaction_hour",

            "transaction_day_of_week",

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

            "is_laundering",

        ]

    ]

)


print(
    "\nSTEP 4: SAMPLE TRANSACTION FEATURE DERIVATION "
    "VALIDATED SUCCESSFULLY."
)

# ==========================================================
# STEP 5: DERIVE FULL TRANSACTION FEATURE DATASET
# ==========================================================

print("\n" + "=" * 70)
print("STEP 5: DERIVE FULL TRANSACTION FEATURE DATASET")
print("=" * 70)


# ----------------------------------------------------------
# REMOVE EXISTING OUTPUT FILE
# ----------------------------------------------------------

if TRANSACTION_FEATURES_FILE.exists():

    TRANSACTION_FEATURES_FILE.unlink()

    print(
        "\nExisting transaction feature output file removed."
    )


# ----------------------------------------------------------
# PROCESSING COUNTERS
# ----------------------------------------------------------

total_transaction_rows_read = 0

total_feature_rows_written = 0

invalid_timestamps_total = 0

missing_feature_values_total = 0

non_finite_numeric_values_total = 0

aml_pattern_membership_rows = 0

laundering_rows = 0


# ----------------------------------------------------------
# SOURCE COLUMN DTYPES
# ----------------------------------------------------------

TRANSACTION_INPUT_DTYPES = {

    "transaction_id": "string",

    "timestamp": "string",

    "sender_account_id": "string",

    "receiver_account_id": "string",

    "from_bank_id": "int64",

    "to_bank_id": "int64",

    "sender_account_number": "string",

    "receiver_account_number": "string",

    "amount_received": "float64",

    "receiving_currency": "string",

    "amount_paid": "float64",

    "payment_currency": "string",

    "payment_format": "string",

    "is_laundering": "int64",

}


# ----------------------------------------------------------
# PROCESS TRANSACTIONS IN CHUNKS
# ----------------------------------------------------------

for chunk_number, transaction_chunk in enumerate(

    pd.read_csv(

        TRANSACTIONS_FILE,

        dtype=TRANSACTION_INPUT_DTYPES,

        chunksize=TRANSACTION_CHUNK_SIZE,

    ),

    start=1,

):

    raw_chunk_rows = len(transaction_chunk)

    total_transaction_rows_read += raw_chunk_rows


    # ------------------------------------------------------
    # PARSE TIMESTAMP
    # ------------------------------------------------------

    transaction_chunk["timestamp"] = pd.to_datetime(

        transaction_chunk["timestamp"],

        errors="coerce",

    )


    invalid_timestamps_chunk = int(

        transaction_chunk["timestamp"]

        .isna()

        .sum()

    )


    invalid_timestamps_total += invalid_timestamps_chunk


    if invalid_timestamps_chunk > 0:

        raise ValueError(

            f"Chunk {chunk_number} contains "

            f"{invalid_timestamps_chunk:,} "

            "invalid timestamps."

        )


    # ------------------------------------------------------
    # DERIVE TEMPORAL FEATURES
    # ------------------------------------------------------

    transaction_chunk["transaction_date"] = (

        transaction_chunk["timestamp"]

        .dt.strftime("%Y-%m-%d")

    )


    transaction_chunk["transaction_hour"] = (

        transaction_chunk["timestamp"]

        .dt.hour

        .astype("int64")

    )


    transaction_chunk["transaction_day_of_week"] = (

        transaction_chunk["timestamp"]

        .dt.dayofweek

        .astype("int64")

    )


    transaction_chunk["transaction_day_of_month"] = (

        transaction_chunk["timestamp"]

        .dt.day

        .astype("int64")

    )


    transaction_chunk["is_weekend"] = (

        transaction_chunk["transaction_day_of_week"]

        .isin([5, 6])

        .astype("int64")

    )


    transaction_chunk["is_night_transaction"] = (

        transaction_chunk["transaction_hour"]

        .between(
            0,
            5,
            inclusive="both",
        )

        .astype("int64")

    )


    # ------------------------------------------------------
    # DERIVE RELATIONSHIP FEATURES
    # ------------------------------------------------------

    transaction_chunk["is_cross_bank_transaction"] = (

        transaction_chunk["from_bank_id"]

        .ne(transaction_chunk["to_bank_id"])

        .astype("int64")

    )


    transaction_chunk["is_self_transfer"] = (

        transaction_chunk["sender_account_id"]

        .eq(transaction_chunk["receiver_account_id"])

        .astype("int64")

    )


    # ------------------------------------------------------
    # DERIVE CURRENCY FEATURE
    # ------------------------------------------------------

    transaction_chunk["is_currency_mismatch"] = (

        transaction_chunk["receiving_currency"]

        .ne(transaction_chunk["payment_currency"])

        .astype("int64")

    )


    # ------------------------------------------------------
    # DERIVE AMOUNT FEATURES
    # ------------------------------------------------------

    transaction_chunk["amount_difference"] = (

        transaction_chunk["amount_received"]

        -

        transaction_chunk["amount_paid"]

    )


    transaction_chunk["amount_ratio"] = (

        transaction_chunk["amount_received"]

        /

        transaction_chunk["amount_paid"]

    )


    transaction_chunk["log_amount_paid"] = np.log1p(

        transaction_chunk["amount_paid"]

    )


    transaction_chunk["log_amount_received"] = np.log1p(

        transaction_chunk["amount_received"]

    )


    # ------------------------------------------------------
    # DERIVE AML PATTERN MEMBERSHIP FEATURE
    # ------------------------------------------------------

    transaction_chunk[

        "is_known_aml_pattern_transaction"

    ] = (

        transaction_chunk["transaction_id"]

        .isin(aml_pattern_transaction_id_set)

        .astype("int64")

    )


    # ------------------------------------------------------
    # APPLY FINAL OUTPUT CONTRACT
    # ------------------------------------------------------

    feature_chunk = transaction_chunk[

        TRANSACTION_FEATURE_COLUMNS

    ].copy()


    # ------------------------------------------------------
    # VALIDATE CHUNK SCHEMA
    # ------------------------------------------------------

    if (

        feature_chunk.columns.tolist()

        != TRANSACTION_FEATURE_COLUMNS

    ):

        raise ValueError(

            f"Feature schema mismatch in "

            f"chunk {chunk_number}."

        )


    # ------------------------------------------------------
    # VALIDATE MISSING VALUES
    # ------------------------------------------------------

    missing_feature_values_chunk = int(

        feature_chunk

        .isna()

        .sum()

        .sum()

    )


    missing_feature_values_total += (

        missing_feature_values_chunk

    )


    if missing_feature_values_chunk > 0:

        raise ValueError(

            f"Chunk {chunk_number} contains "

            f"{missing_feature_values_chunk:,} "

            "missing feature values."

        )


    # ------------------------------------------------------
    # VALIDATE NON-FINITE NUMERIC FEATURES
    # ------------------------------------------------------

    non_finite_numeric_values_chunk = 0


    for column_name in numeric_feature_columns:

        non_finite_numeric_values_chunk += int(

            (

                ~np.isfinite(

                    feature_chunk[column_name]

                )

            ).sum()

        )


    non_finite_numeric_values_total += (

        non_finite_numeric_values_chunk

    )


    if non_finite_numeric_values_chunk > 0:

        raise ValueError(

            f"Chunk {chunk_number} contains "

            f"{non_finite_numeric_values_chunk:,} "

            "non-finite numeric feature values."

        )


    # ------------------------------------------------------
    # VALIDATE BINARY FEATURE DOMAINS
    # ------------------------------------------------------

    for column_name in (

        BINARY_TRANSACTION_FEATURE_COLUMNS

        + ["is_laundering"]

    ):

        invalid_binary_rows = int(

            (

                ~feature_chunk[column_name]

                .isin([0, 1])

            ).sum()

        )


        if invalid_binary_rows > 0:

            raise ValueError(

                f"Chunk {chunk_number} contains "

                f"{invalid_binary_rows:,} invalid values "

                f"in {column_name}."

            )


    # ------------------------------------------------------
    # UPDATE FEATURE COUNTERS
    # ------------------------------------------------------

    aml_pattern_membership_rows += int(

        feature_chunk[

            "is_known_aml_pattern_transaction"

        ].sum()

    )


    laundering_rows += int(

        feature_chunk["is_laundering"].sum()

    )


    # ------------------------------------------------------
    # WRITE FEATURE CHUNK
    # ------------------------------------------------------

    feature_chunk.to_csv(

        TRANSACTION_FEATURES_FILE,

        mode="w" if chunk_number == 1 else "a",

        header=(chunk_number == 1),

        index=False,

    )


    total_feature_rows_written += len(feature_chunk)


    print(

        f"Processed Feature Chunk "

        f"{chunk_number:>2} | "

        f"Rows Read: "

        f"{total_transaction_rows_read:>9,} | "

        f"Rows Written: "

        f"{total_feature_rows_written:>9,}"

    )


# ----------------------------------------------------------
# FINAL PRODUCTION PROCESSING RESULTS
# ----------------------------------------------------------

print("\n" + "=" * 70)

print("TRANSACTION FEATURE DERIVATION RESULTS")

print("=" * 70)


print(

    f"Total Transaction Rows Read        : "

    f"{total_transaction_rows_read:,}"

)


print(

    f"Total Feature Rows Written         : "

    f"{total_feature_rows_written:,}"

)


print(

    f"Invalid Timestamps                 : "

    f"{invalid_timestamps_total:,}"

)


print(

    f"Missing Feature Values             : "

    f"{missing_feature_values_total:,}"

)


print(

    f"Non-Finite Numeric Feature Values  : "

    f"{non_finite_numeric_values_total:,}"

)


print(

    f"AML Pattern Membership Rows        : "

    f"{aml_pattern_membership_rows:,}"

)


print(

    f"Laundering Rows                    : "

    f"{laundering_rows:,}"

)


# ----------------------------------------------------------
# VALIDATE FINAL PROCESSING COUNTS
# ----------------------------------------------------------

production_processing_valid = (

    total_transaction_rows_read

        == EXPECTED_TRANSACTION_ROW_COUNT

    and total_feature_rows_written

        == EXPECTED_TRANSACTION_ROW_COUNT

    and invalid_timestamps_total == 0

    and missing_feature_values_total == 0

    and non_finite_numeric_values_total == 0

    and aml_pattern_membership_rows

        == len(aml_pattern_transaction_id_set)

    and laundering_rows == 5_177

)


print(

    f"\nTransaction Feature Derivation Status: "

    f"{'PASS' if production_processing_valid else 'FAIL'}"

)


if not production_processing_valid:

    raise ValueError(

        "Full transaction feature derivation "

        "validation failed."

    )


# ----------------------------------------------------------
# VERIFY OUTPUT FILE
# ----------------------------------------------------------

if not TRANSACTION_FEATURES_FILE.exists():

    raise FileNotFoundError(

        "Transaction feature output file "

        "was not created."

    )


if TRANSACTION_FEATURES_FILE.stat().st_size == 0:

    raise ValueError(

        "Transaction feature output file is empty."

    )


feature_file_size_mb = (

    TRANSACTION_FEATURES_FILE.stat().st_size

    / (1024 ** 2)

)


print(

    f"Transaction Feature File Size      : "

    f"{feature_file_size_mb:.2f} MB"

)


print(

    "\nSTEP 5: FULL TRANSACTION FEATURE DATASET "

    "DERIVED SUCCESSFULLY."

)

# ==========================================================
# STEP 5: DERIVE FULL TRANSACTION FEATURE DATASET
# ==========================================================

print("\n" + "=" * 70)
print("STEP 5: DERIVE FULL TRANSACTION FEATURE DATASET")
print("=" * 70)


# ----------------------------------------------------------
# REMOVE EXISTING OUTPUT FILE
# ----------------------------------------------------------

if TRANSACTION_FEATURES_FILE.exists():

    TRANSACTION_FEATURES_FILE.unlink()

    print(
        "\nExisting transaction feature output file removed."
    )


# ----------------------------------------------------------
# PROCESSING COUNTERS
# ----------------------------------------------------------

total_transaction_rows_read = 0

total_feature_rows_written = 0

invalid_timestamps_total = 0

missing_feature_values_total = 0

non_finite_numeric_values_total = 0

aml_pattern_membership_rows = 0

laundering_rows = 0


# ----------------------------------------------------------
# SOURCE COLUMN DTYPES
# ----------------------------------------------------------

TRANSACTION_INPUT_DTYPES = {

    "transaction_id": "string",

    "timestamp": "string",

    "sender_account_id": "string",

    "receiver_account_id": "string",

    "from_bank_id": "int64",

    "to_bank_id": "int64",

    "sender_account_number": "string",

    "receiver_account_number": "string",

    "amount_received": "float64",

    "receiving_currency": "string",

    "amount_paid": "float64",

    "payment_currency": "string",

    "payment_format": "string",

    "is_laundering": "int64",

}


# ----------------------------------------------------------
# PROCESS TRANSACTIONS IN CHUNKS
# ----------------------------------------------------------

for chunk_number, transaction_chunk in enumerate(

    pd.read_csv(

        TRANSACTIONS_FILE,

        dtype=TRANSACTION_INPUT_DTYPES,

        chunksize=TRANSACTION_CHUNK_SIZE,

    ),

    start=1,

):

    raw_chunk_rows = len(transaction_chunk)

    total_transaction_rows_read += raw_chunk_rows


    # ------------------------------------------------------
    # PARSE TIMESTAMP
    # ------------------------------------------------------

    transaction_chunk["timestamp"] = pd.to_datetime(

        transaction_chunk["timestamp"],

        errors="coerce",

    )


    invalid_timestamps_chunk = int(

        transaction_chunk["timestamp"]

        .isna()

        .sum()

    )


    invalid_timestamps_total += invalid_timestamps_chunk


    if invalid_timestamps_chunk > 0:

        raise ValueError(

            f"Chunk {chunk_number} contains "

            f"{invalid_timestamps_chunk:,} "

            "invalid timestamps."

        )


    # ------------------------------------------------------
    # DERIVE TEMPORAL FEATURES
    # ------------------------------------------------------

    transaction_chunk["transaction_date"] = (

        transaction_chunk["timestamp"]

        .dt.strftime("%Y-%m-%d")

    )


    transaction_chunk["transaction_hour"] = (

        transaction_chunk["timestamp"]

        .dt.hour

        .astype("int64")

    )


    transaction_chunk["transaction_day_of_week"] = (

        transaction_chunk["timestamp"]

        .dt.dayofweek

        .astype("int64")

    )


    transaction_chunk["transaction_day_of_month"] = (

        transaction_chunk["timestamp"]

        .dt.day

        .astype("int64")

    )


    transaction_chunk["is_weekend"] = (

        transaction_chunk["transaction_day_of_week"]

        .isin([5, 6])

        .astype("int64")

    )


    transaction_chunk["is_night_transaction"] = (

        transaction_chunk["transaction_hour"]

        .between(
            0,
            5,
            inclusive="both",
        )

        .astype("int64")

    )


    # ------------------------------------------------------
    # DERIVE RELATIONSHIP FEATURES
    # ------------------------------------------------------

    transaction_chunk["is_cross_bank_transaction"] = (

        transaction_chunk["from_bank_id"]

        .ne(transaction_chunk["to_bank_id"])

        .astype("int64")

    )


    transaction_chunk["is_self_transfer"] = (

        transaction_chunk["sender_account_id"]

        .eq(transaction_chunk["receiver_account_id"])

        .astype("int64")

    )


    # ------------------------------------------------------
    # DERIVE CURRENCY FEATURE
    # ------------------------------------------------------

    transaction_chunk["is_currency_mismatch"] = (

        transaction_chunk["receiving_currency"]

        .ne(transaction_chunk["payment_currency"])

        .astype("int64")

    )


    # ------------------------------------------------------
    # DERIVE AMOUNT FEATURES
    # ------------------------------------------------------

    transaction_chunk["amount_difference"] = (

        transaction_chunk["amount_received"]

        -

        transaction_chunk["amount_paid"]

    )


    transaction_chunk["amount_ratio"] = (

        transaction_chunk["amount_received"]

        /

        transaction_chunk["amount_paid"]

    )


    transaction_chunk["log_amount_paid"] = np.log1p(

        transaction_chunk["amount_paid"]

    )


    transaction_chunk["log_amount_received"] = np.log1p(

        transaction_chunk["amount_received"]

    )


    # ------------------------------------------------------
    # DERIVE AML PATTERN MEMBERSHIP FEATURE
    # ------------------------------------------------------

    transaction_chunk[

        "is_known_aml_pattern_transaction"

    ] = (

        transaction_chunk["transaction_id"]

        .isin(aml_pattern_transaction_id_set)

        .astype("int64")

    )


    # ------------------------------------------------------
    # APPLY FINAL OUTPUT CONTRACT
    # ------------------------------------------------------

    feature_chunk = transaction_chunk[

        TRANSACTION_FEATURE_COLUMNS

    ].copy()


    # ------------------------------------------------------
    # VALIDATE CHUNK SCHEMA
    # ------------------------------------------------------

    if (

        feature_chunk.columns.tolist()

        != TRANSACTION_FEATURE_COLUMNS

    ):

        raise ValueError(

            f"Feature schema mismatch in "

            f"chunk {chunk_number}."

        )


    # ------------------------------------------------------
    # VALIDATE MISSING VALUES
    # ------------------------------------------------------

    missing_feature_values_chunk = int(

        feature_chunk

        .isna()

        .sum()

        .sum()

    )


    missing_feature_values_total += (

        missing_feature_values_chunk

    )


    if missing_feature_values_chunk > 0:

        raise ValueError(

            f"Chunk {chunk_number} contains "

            f"{missing_feature_values_chunk:,} "

            "missing feature values."

        )


    # ------------------------------------------------------
    # VALIDATE NON-FINITE NUMERIC FEATURES
    # ------------------------------------------------------

    non_finite_numeric_values_chunk = 0


    for column_name in numeric_feature_columns:

        non_finite_numeric_values_chunk += int(

            (

                ~np.isfinite(

                    feature_chunk[column_name]

                )

            ).sum()

        )


    non_finite_numeric_values_total += (

        non_finite_numeric_values_chunk

    )


    if non_finite_numeric_values_chunk > 0:

        raise ValueError(

            f"Chunk {chunk_number} contains "

            f"{non_finite_numeric_values_chunk:,} "

            "non-finite numeric feature values."

        )


    # ------------------------------------------------------
    # VALIDATE BINARY FEATURE DOMAINS
    # ------------------------------------------------------

    for column_name in (

        BINARY_TRANSACTION_FEATURE_COLUMNS

        + ["is_laundering"]

    ):

        invalid_binary_rows = int(

            (

                ~feature_chunk[column_name]

                .isin([0, 1])

            ).sum()

        )


        if invalid_binary_rows > 0:

            raise ValueError(

                f"Chunk {chunk_number} contains "

                f"{invalid_binary_rows:,} invalid values "

                f"in {column_name}."

            )


    # ------------------------------------------------------
    # UPDATE FEATURE COUNTERS
    # ------------------------------------------------------

    aml_pattern_membership_rows += int(

        feature_chunk[

            "is_known_aml_pattern_transaction"

        ].sum()

    )


    laundering_rows += int(

        feature_chunk["is_laundering"].sum()

    )


    # ------------------------------------------------------
    # WRITE FEATURE CHUNK
    # ------------------------------------------------------

    feature_chunk.to_csv(

        TRANSACTION_FEATURES_FILE,

        mode="w" if chunk_number == 1 else "a",

        header=(chunk_number == 1),

        index=False,

    )


    total_feature_rows_written += len(feature_chunk)


    print(

        f"Processed Feature Chunk "

        f"{chunk_number:>2} | "

        f"Rows Read: "

        f"{total_transaction_rows_read:>9,} | "

        f"Rows Written: "

        f"{total_feature_rows_written:>9,}"

    )


# ----------------------------------------------------------
# FINAL PRODUCTION PROCESSING RESULTS
# ----------------------------------------------------------

print("\n" + "=" * 70)

print("TRANSACTION FEATURE DERIVATION RESULTS")

print("=" * 70)


print(

    f"Total Transaction Rows Read        : "

    f"{total_transaction_rows_read:,}"

)


print(

    f"Total Feature Rows Written         : "

    f"{total_feature_rows_written:,}"

)


print(

    f"Invalid Timestamps                 : "

    f"{invalid_timestamps_total:,}"

)


print(

    f"Missing Feature Values             : "

    f"{missing_feature_values_total:,}"

)


print(

    f"Non-Finite Numeric Feature Values  : "

    f"{non_finite_numeric_values_total:,}"

)


print(

    f"AML Pattern Membership Rows        : "

    f"{aml_pattern_membership_rows:,}"

)


print(

    f"Laundering Rows                    : "

    f"{laundering_rows:,}"

)


# ----------------------------------------------------------
# VALIDATE FINAL PROCESSING COUNTS
# ----------------------------------------------------------

production_processing_valid = (

    total_transaction_rows_read

        == EXPECTED_TRANSACTION_ROW_COUNT

    and total_feature_rows_written

        == EXPECTED_TRANSACTION_ROW_COUNT

    and invalid_timestamps_total == 0

    and missing_feature_values_total == 0

    and non_finite_numeric_values_total == 0

    and aml_pattern_membership_rows

        == len(aml_pattern_transaction_id_set)

    and laundering_rows == 5_177

)


print(

    f"\nTransaction Feature Derivation Status: "

    f"{'PASS' if production_processing_valid else 'FAIL'}"

)


if not production_processing_valid:

    raise ValueError(

        "Full transaction feature derivation "

        "validation failed."

    )


# ----------------------------------------------------------
# VERIFY OUTPUT FILE
# ----------------------------------------------------------

if not TRANSACTION_FEATURES_FILE.exists():

    raise FileNotFoundError(

        "Transaction feature output file "

        "was not created."

    )


if TRANSACTION_FEATURES_FILE.stat().st_size == 0:

    raise ValueError(

        "Transaction feature output file is empty."

    )


feature_file_size_mb = (

    TRANSACTION_FEATURES_FILE.stat().st_size

    / (1024 ** 2)

)


print(

    f"Transaction Feature File Size      : "

    f"{feature_file_size_mb:.2f} MB"

)


print(

    "\nSTEP 5: FULL TRANSACTION FEATURE DATASET "

    "DERIVED SUCCESSFULLY."

)

# ==========================================================
# STEP 6: INDEPENDENT TRANSACTION FEATURE DATASET VALIDATION
# ==========================================================

print("\n" + "=" * 70)
print("STEP 6: INDEPENDENT TRANSACTION FEATURE DATASET VALIDATION")
print("=" * 70)


# ----------------------------------------------------------
# VERIFY OUTPUT FILE EXISTS
# ----------------------------------------------------------

if not TRANSACTION_FEATURES_FILE.exists():

    raise FileNotFoundError(

        "Transaction feature dataset does not exist."

    )


if TRANSACTION_FEATURES_FILE.stat().st_size == 0:

    raise ValueError(

        "Transaction feature dataset is empty."

    )


print("\nTransaction feature dataset found successfully.")

print(
    f"Feature File: {TRANSACTION_FEATURES_FILE}"
)


# ----------------------------------------------------------
# INDEPENDENT VALIDATION COUNTERS
# ----------------------------------------------------------

validated_feature_rows = 0

duplicate_transaction_ids = 0

missing_values = 0

non_finite_values = 0

invalid_binary_values = 0

invalid_timestamp_values = 0

aml_pattern_membership_count = 0

laundering_count = 0


# Used for independent transaction ID uniqueness validation.

seen_transaction_ids = set()


# ----------------------------------------------------------
# FEATURE DATASET DTYPES
# ----------------------------------------------------------

FEATURE_VALIDATION_DTYPES = {

    "transaction_id": "string",

    "timestamp": "string",

    "sender_account_id": "string",

    "receiver_account_id": "string",

    "from_bank_id": "int64",

    "to_bank_id": "int64",

    "amount_received": "float64",

    "receiving_currency": "string",

    "amount_paid": "float64",

    "payment_currency": "string",

    "payment_format": "string",

    "transaction_date": "string",

    "transaction_hour": "int64",

    "transaction_day_of_week": "int64",

    "transaction_day_of_month": "int64",

    "is_weekend": "int64",

    "is_night_transaction": "int64",

    "is_cross_bank_transaction": "int64",

    "is_self_transfer": "int64",

    "is_currency_mismatch": "int64",

    "amount_difference": "float64",

    "amount_ratio": "float64",

    "log_amount_paid": "float64",

    "log_amount_received": "float64",

    "is_known_aml_pattern_transaction": "int64",

    "is_laundering": "int64",

}


# ----------------------------------------------------------
# VALIDATION FEATURE GROUPS
# ----------------------------------------------------------

VALIDATION_BINARY_COLUMNS = [

    "is_weekend",

    "is_night_transaction",

    "is_cross_bank_transaction",

    "is_self_transfer",

    "is_currency_mismatch",

    "is_known_aml_pattern_transaction",

    "is_laundering",

]


VALIDATION_FINITE_NUMERIC_COLUMNS = [

    "amount_difference",

    "amount_ratio",

    "log_amount_paid",

    "log_amount_received",

]


# ----------------------------------------------------------
# PROCESS PERSISTED FEATURE FILE INDEPENDENTLY
# ----------------------------------------------------------

for validation_chunk_number, feature_validation_chunk in enumerate(

    pd.read_csv(

        TRANSACTION_FEATURES_FILE,

        dtype=FEATURE_VALIDATION_DTYPES,

        chunksize=TRANSACTION_CHUNK_SIZE,

    ),

    start=1,

):

    chunk_rows = len(feature_validation_chunk)

    validated_feature_rows += chunk_rows


    # ------------------------------------------------------
    # VALIDATE EXACT SCHEMA AND COLUMN ORDER
    # ------------------------------------------------------

    if (

        feature_validation_chunk.columns.tolist()

        != TRANSACTION_FEATURE_COLUMNS

    ):

        raise ValueError(

            f"Persisted feature schema mismatch in "

            f"validation chunk {validation_chunk_number}."

        )


    # ------------------------------------------------------
    # VALIDATE MISSING VALUES
    # ------------------------------------------------------

    missing_values_chunk = int(

        feature_validation_chunk

        .isna()

        .sum()

        .sum()

    )


    missing_values += missing_values_chunk


    # ------------------------------------------------------
    # VALIDATE TIMESTAMPS
    # ------------------------------------------------------

    parsed_timestamps = pd.to_datetime(

        feature_validation_chunk["timestamp"],

        errors="coerce",

    )


    invalid_timestamp_values_chunk = int(

        parsed_timestamps

        .isna()

        .sum()

    )


    invalid_timestamp_values += (

        invalid_timestamp_values_chunk

    )


    # ------------------------------------------------------
    # VALIDATE TRANSACTION ID UNIQUENESS
    # ------------------------------------------------------

    transaction_ids = (

        feature_validation_chunk["transaction_id"]

        .tolist()

    )


    duplicate_transaction_ids += (

        len(transaction_ids)

        -

        len(set(transaction_ids))

    )


    duplicate_transaction_ids += sum(

        transaction_id in seen_transaction_ids

        for transaction_id in set(transaction_ids)

    )


    seen_transaction_ids.update(transaction_ids)


    # ------------------------------------------------------
    # VALIDATE NON-FINITE NUMERIC VALUES
    # ------------------------------------------------------

    for column_name in VALIDATION_FINITE_NUMERIC_COLUMNS:

        non_finite_values += int(

            (

                ~np.isfinite(

                    feature_validation_chunk[column_name]

                )

            ).sum()

        )


    # ------------------------------------------------------
    # VALIDATE BINARY DOMAINS
    # ------------------------------------------------------

    for column_name in VALIDATION_BINARY_COLUMNS:

        invalid_binary_values += int(

            (

                ~feature_validation_chunk[column_name]

                .isin([0, 1])

            ).sum()

        )


    # ------------------------------------------------------
    # COUNT AML MEMBERSHIP AND LAUNDERING ROWS
    # ------------------------------------------------------

    aml_pattern_membership_count += int(

        feature_validation_chunk[

            "is_known_aml_pattern_transaction"

        ].sum()

    )


    laundering_count += int(

        feature_validation_chunk[

            "is_laundering"

        ].sum()

    )


    print(

        f"Validated Feature Chunk "

        f"{validation_chunk_number:>2} | "

        f"Rows Validated: "

        f"{validated_feature_rows:>9,}"

    )


# ----------------------------------------------------------
# RELEASE LARGE UNIQUENESS SET
# ----------------------------------------------------------

unique_transaction_ids = len(seen_transaction_ids)

del seen_transaction_ids


# ----------------------------------------------------------
# DISPLAY INDEPENDENT VALIDATION RESULTS
# ----------------------------------------------------------

print("\n" + "=" * 70)

print("INDEPENDENT TRANSACTION FEATURE VALIDATION RESULTS")

print("=" * 70)


print(

    f"Validated Feature Rows             : "

    f"{validated_feature_rows:,}"

)


print(

    f"Unique Transaction IDs             : "

    f"{unique_transaction_ids:,}"

)


print(

    f"Duplicate Transaction IDs          : "

    f"{duplicate_transaction_ids:,}"

)


print(

    f"Missing Values                     : "

    f"{missing_values:,}"

)


print(

    f"Invalid Timestamps                 : "

    f"{invalid_timestamp_values:,}"

)


print(

    f"Non-Finite Numeric Values          : "

    f"{non_finite_values:,}"

)


print(

    f"Invalid Binary Values              : "

    f"{invalid_binary_values:,}"

)


print(

    f"AML Pattern Membership Rows        : "

    f"{aml_pattern_membership_count:,}"

)


print(

    f"Laundering Rows                    : "

    f"{laundering_count:,}"

)


# ----------------------------------------------------------
# FINAL INDEPENDENT VALIDATION STATUS
# ----------------------------------------------------------

independent_validation_valid = (

    validated_feature_rows

        == EXPECTED_TRANSACTION_ROW_COUNT

    and unique_transaction_ids

        == EXPECTED_TRANSACTION_ROW_COUNT

    and duplicate_transaction_ids == 0

    and missing_values == 0

    and invalid_timestamp_values == 0

    and non_finite_values == 0

    and invalid_binary_values == 0

    and aml_pattern_membership_count

        == len(aml_pattern_transaction_id_set)

    and laundering_count == 5_177

)


print(

    f"\nIndependent Feature Validation Status: "

    f"{'PASS' if independent_validation_valid else 'FAIL'}"

)


if not independent_validation_valid:

    raise ValueError(

        "Independent transaction feature dataset "

        "validation failed."

    )


print(

    "\nSTEP 6: INDEPENDENT TRANSACTION FEATURE DATASET "

    "VALIDATION COMPLETED SUCCESSFULLY."

)

# ==========================================================
# STEP 7: FEATURE FORMULA AND SEMANTIC VALIDATION
# ==========================================================

print("\n" + "=" * 70)
print("STEP 7: FEATURE FORMULA AND SEMANTIC VALIDATION")
print("=" * 70)


# ----------------------------------------------------------
# FORMULA VALIDATION COUNTERS
# ----------------------------------------------------------

formula_rows_validated = 0

formula_mismatch_counts = {

    "transaction_date": 0,

    "transaction_hour": 0,

    "transaction_day_of_week": 0,

    "transaction_day_of_month": 0,

    "is_weekend": 0,

    "is_night_transaction": 0,

    "is_cross_bank_transaction": 0,

    "is_self_transfer": 0,

    "is_currency_mismatch": 0,

    "amount_difference": 0,

    "amount_ratio": 0,

    "log_amount_paid": 0,

    "log_amount_received": 0,

    "is_known_aml_pattern_transaction": 0,

}


aml_pattern_rows_found = 0

aml_pattern_non_laundering_rows = 0


# ----------------------------------------------------------
# FLOAT COMPARISON TOLERANCES
# ----------------------------------------------------------

FLOAT_RELATIVE_TOLERANCE = 1e-9

FLOAT_ABSOLUTE_TOLERANCE = 1e-9


# ----------------------------------------------------------
# PROCESS PERSISTED FEATURE DATASET
# ----------------------------------------------------------

for semantic_chunk_number, semantic_chunk in enumerate(

    pd.read_csv(

        TRANSACTION_FEATURES_FILE,

        dtype=FEATURE_VALIDATION_DTYPES,

        chunksize=TRANSACTION_CHUNK_SIZE,

    ),

    start=1,

):

    chunk_rows = len(semantic_chunk)

    formula_rows_validated += chunk_rows


    # ------------------------------------------------------
    # PARSE SOURCE TIMESTAMPS
    # ------------------------------------------------------

    parsed_timestamp = pd.to_datetime(

        semantic_chunk["timestamp"],

        errors="coerce",

    )


    if parsed_timestamp.isna().any():

        raise ValueError(

            f"Invalid timestamps detected in "

            f"semantic chunk {semantic_chunk_number}."

        )


    # ------------------------------------------------------
    # RECOMPUTE TEMPORAL FEATURES
    # ------------------------------------------------------

    expected_transaction_date = (

        parsed_timestamp

        .dt.strftime("%Y-%m-%d")

    )


    expected_transaction_hour = (

        parsed_timestamp

        .dt.hour

        .astype("int64")

    )


    expected_transaction_day_of_week = (

        parsed_timestamp

        .dt.dayofweek

        .astype("int64")

    )


    expected_transaction_day_of_month = (

        parsed_timestamp

        .dt.day

        .astype("int64")

    )


    expected_is_weekend = (

        expected_transaction_day_of_week

        .isin([5, 6])

        .astype("int64")

    )


    expected_is_night_transaction = (

        expected_transaction_hour

        .between(
            0,
            5,
            inclusive="both",
        )

        .astype("int64")

    )


    # ------------------------------------------------------
    # RECOMPUTE RELATIONSHIP FEATURES
    # ------------------------------------------------------

    expected_is_cross_bank_transaction = (

        semantic_chunk["from_bank_id"]

        .ne(semantic_chunk["to_bank_id"])

        .astype("int64")

    )


    expected_is_self_transfer = (

        semantic_chunk["sender_account_id"]

        .eq(semantic_chunk["receiver_account_id"])

        .astype("int64")

    )


    # ------------------------------------------------------
    # RECOMPUTE CURRENCY FEATURE
    # ------------------------------------------------------

    expected_is_currency_mismatch = (

        semantic_chunk["receiving_currency"]

        .ne(semantic_chunk["payment_currency"])

        .astype("int64")

    )


    # ------------------------------------------------------
    # RECOMPUTE AMOUNT FEATURES
    # ------------------------------------------------------

    expected_amount_difference = (

        semantic_chunk["amount_received"]

        -

        semantic_chunk["amount_paid"]

    )


    expected_amount_ratio = (

        semantic_chunk["amount_received"]

        /

        semantic_chunk["amount_paid"]

    )


    expected_log_amount_paid = np.log1p(

        semantic_chunk["amount_paid"]

    )


    expected_log_amount_received = np.log1p(

        semantic_chunk["amount_received"]

    )


    # ------------------------------------------------------
    # RECOMPUTE AML PATTERN MEMBERSHIP
    # ------------------------------------------------------

    expected_is_known_aml_pattern_transaction = (

        semantic_chunk["transaction_id"]

        .isin(aml_pattern_transaction_id_set)

        .astype("int64")

    )


    # ------------------------------------------------------
    # VALIDATE EXACT TEMPORAL FEATURES
    # ------------------------------------------------------

    formula_mismatch_counts["transaction_date"] += int(

        (

            semantic_chunk["transaction_date"]

            != expected_transaction_date

        ).sum()

    )


    formula_mismatch_counts["transaction_hour"] += int(

        (

            semantic_chunk["transaction_hour"]

            != expected_transaction_hour

        ).sum()

    )


    formula_mismatch_counts[

        "transaction_day_of_week"

    ] += int(

        (

            semantic_chunk["transaction_day_of_week"]

            != expected_transaction_day_of_week

        ).sum()

    )


    formula_mismatch_counts[

        "transaction_day_of_month"

    ] += int(

        (

            semantic_chunk["transaction_day_of_month"]

            != expected_transaction_day_of_month

        ).sum()

    )


    formula_mismatch_counts["is_weekend"] += int(

        (

            semantic_chunk["is_weekend"]

            != expected_is_weekend

        ).sum()

    )


    formula_mismatch_counts[

        "is_night_transaction"

    ] += int(

        (

            semantic_chunk["is_night_transaction"]

            != expected_is_night_transaction

        ).sum()

    )


    # ------------------------------------------------------
    # VALIDATE EXACT RELATIONSHIP FEATURES
    # ------------------------------------------------------

    formula_mismatch_counts[

        "is_cross_bank_transaction"

    ] += int(

        (

            semantic_chunk["is_cross_bank_transaction"]

            != expected_is_cross_bank_transaction

        ).sum()

    )


    formula_mismatch_counts["is_self_transfer"] += int(

        (

            semantic_chunk["is_self_transfer"]

            != expected_is_self_transfer

        ).sum()

    )


    formula_mismatch_counts[

        "is_currency_mismatch"

    ] += int(

        (

            semantic_chunk["is_currency_mismatch"]

            != expected_is_currency_mismatch

        ).sum()

    )


    # ------------------------------------------------------
    # VALIDATE FLOATING-POINT FEATURES
    # ------------------------------------------------------

    formula_mismatch_counts["amount_difference"] += int(

        (

            ~np.isclose(

                semantic_chunk["amount_difference"],

                expected_amount_difference,

                rtol=FLOAT_RELATIVE_TOLERANCE,

                atol=FLOAT_ABSOLUTE_TOLERANCE,

                equal_nan=False,

            )

        ).sum()

    )


    formula_mismatch_counts["amount_ratio"] += int(

        (

            ~np.isclose(

                semantic_chunk["amount_ratio"],

                expected_amount_ratio,

                rtol=FLOAT_RELATIVE_TOLERANCE,

                atol=FLOAT_ABSOLUTE_TOLERANCE,

                equal_nan=False,

            )

        ).sum()

    )


    formula_mismatch_counts["log_amount_paid"] += int(

        (

            ~np.isclose(

                semantic_chunk["log_amount_paid"],

                expected_log_amount_paid,

                rtol=FLOAT_RELATIVE_TOLERANCE,

                atol=FLOAT_ABSOLUTE_TOLERANCE,

                equal_nan=False,

            )

        ).sum()

    )


    formula_mismatch_counts["log_amount_received"] += int(

        (

            ~np.isclose(

                semantic_chunk["log_amount_received"],

                expected_log_amount_received,

                rtol=FLOAT_RELATIVE_TOLERANCE,

                atol=FLOAT_ABSOLUTE_TOLERANCE,

                equal_nan=False,

            )

        ).sum()

    )


    # ------------------------------------------------------
    # VALIDATE AML MEMBERSHIP FEATURE
    # ------------------------------------------------------

    formula_mismatch_counts[

        "is_known_aml_pattern_transaction"

    ] += int(

        (

            semantic_chunk[

                "is_known_aml_pattern_transaction"

            ]

            != expected_is_known_aml_pattern_transaction

        ).sum()

    )


    # ------------------------------------------------------
    # VALIDATE AML SEMANTIC RELATIONSHIP
    # ------------------------------------------------------

    known_aml_mask = (

        semantic_chunk[

            "is_known_aml_pattern_transaction"

        ]

        == 1

    )


    aml_pattern_rows_found += int(

        known_aml_mask.sum()

    )


    aml_pattern_non_laundering_rows += int(

        (

            known_aml_mask

            &

            (

                semantic_chunk["is_laundering"]

                != 1

            )

        ).sum()

    )


    print(

        f"Validated Formula Chunk "

        f"{semantic_chunk_number:>2} | "

        f"Rows Validated: "

        f"{formula_rows_validated:>9,}"

    )


# ----------------------------------------------------------
# DISPLAY FEATURE FORMULA RESULTS
# ----------------------------------------------------------

print("\n" + "=" * 70)

print("FEATURE FORMULA VALIDATION RESULTS")

print("=" * 70)


print(

    f"Total Feature Rows Validated       : "

    f"{formula_rows_validated:,}"

)


print("\nFeature Formula Mismatch Counts:")


for feature_name, mismatch_count in (

    formula_mismatch_counts.items()

):

    print(

        f"  {feature_name:<40}: "

        f"{mismatch_count:,}"

    )


total_formula_mismatches = sum(

    formula_mismatch_counts.values()

)


print(

    f"\nTotal Feature Formula Mismatches   : "

    f"{total_formula_mismatches:,}"

)


# ----------------------------------------------------------
# DISPLAY AML SEMANTIC RESULTS
# ----------------------------------------------------------

print("\nAML Pattern Semantic Results:")


print(

    f"  Expected AML Pattern Rows        : "

    f"{len(aml_pattern_transaction_id_set):,}"

)


print(

    f"  AML Pattern Rows Found           : "

    f"{aml_pattern_rows_found:,}"

)


print(

    f"  AML Pattern Non-Laundering Rows  : "

    f"{aml_pattern_non_laundering_rows:,}"

)


# ----------------------------------------------------------
# FINAL STEP 7 VALIDATION STATUS
# ----------------------------------------------------------

feature_formula_semantic_valid = (

    formula_rows_validated

        == EXPECTED_TRANSACTION_ROW_COUNT

    and total_formula_mismatches == 0

    and aml_pattern_rows_found

        == len(aml_pattern_transaction_id_set)

    and aml_pattern_non_laundering_rows == 0

)


print(

    f"\nFeature Formula and Semantic Validation Status: "

    f"{'PASS' if feature_formula_semantic_valid else 'FAIL'}"

)


if not feature_formula_semantic_valid:

    raise ValueError(

        "Transaction feature formula and semantic "

        "validation failed."

    )


print(

    "\nSTEP 7: FEATURE FORMULA AND SEMANTIC "

    "VALIDATION COMPLETED SUCCESSFULLY."

)


