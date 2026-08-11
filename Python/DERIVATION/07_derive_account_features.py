# ============================================================
# 07_DERIVE_ACCOUNT_FEATURES.PY
# Banking Fraud Detection & Financial Risk Intelligence Platform
# ============================================================

from pathlib import Path

import pandas as pd
import numpy as np
from collections import defaultdict

# ============================================================
# DIRECTORY CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "DATA"

CLEANED_DIR = DATA_DIR / "CLEANED"

DERIVED_DIR = DATA_DIR / "DERIVED"

REPORTS_DIR = PROJECT_ROOT / "REPORTS"


# ============================================================
# INPUT FILES
# ============================================================

BANKS_FILE = CLEANED_DIR / "banks.csv"

CUSTOMERS_FILE = CLEANED_DIR / "customers.csv"

ACCOUNTS_FILE = CLEANED_DIR / "accounts.csv"

TRANSACTION_FEATURES_FILE = (
    DERIVED_DIR / "transaction_features.csv"
)

AML_PATTERNS_FILE = (
    CLEANED_DIR / "aml_patterns.csv"
)

AML_PATTERN_TRANSACTIONS_FILE = (
    CLEANED_DIR /
    "aml_pattern_transactions.csv"
)


# ============================================================
# OUTPUT FILE
# ============================================================

ACCOUNT_FEATURES_FILE = (
    DERIVED_DIR / "account_features.csv"
)


# ============================================================
# CONSTANTS
# ============================================================

EXPECTED_ACCOUNT_COUNT = 518_581

EXPECTED_TRANSACTION_FEATURE_COUNT = 3_000_000

EXPECTED_AML_PATTERN_COUNT = 370

EXPECTED_PATTERN_TRANSACTION_COUNT = 3_209

TRANSACTION_CHUNK_SIZE = 250_000

# ============================================================
# STEP 1
# LOAD AND VALIDATE DERIVATION INPUTS
# ============================================================

print("\n" + "=" * 70)
print("STEP 1: LOAD AND VALIDATE DERIVATION INPUTS")
print("=" * 70)


# ------------------------------------------------------------
# VERIFY REQUIRED INPUT FILES
# ------------------------------------------------------------

required_files = {

    "banks": BANKS_FILE,

    "customers": CUSTOMERS_FILE,

    "accounts": ACCOUNTS_FILE,

    "transaction_features": TRANSACTION_FEATURES_FILE,

    "aml_patterns": AML_PATTERNS_FILE,

    "aml_pattern_transactions":
        AML_PATTERN_TRANSACTIONS_FILE,

}


print("\nChecking required input files...\n")


for dataset_name, dataset_path in required_files.items():

    if not dataset_path.exists():

        raise FileNotFoundError(

            f"{dataset_name} file not found:\n"

            f"{dataset_path}"

        )

    print(f"✓ {dataset_name}")


# ------------------------------------------------------------
# LOAD REFERENCE DATASETS
# ------------------------------------------------------------

print("\nLoading reference datasets...\n")


banks_df = pd.read_csv(BANKS_FILE)

customers_df = pd.read_csv(CUSTOMERS_FILE)

accounts_df = pd.read_csv(ACCOUNTS_FILE)

aml_patterns_df = pd.read_csv(AML_PATTERNS_FILE)

aml_pattern_transactions_df = pd.read_csv(
    AML_PATTERN_TRANSACTIONS_FILE
)


# ------------------------------------------------------------
# LOAD TRANSACTION FEATURE SAMPLE
# ------------------------------------------------------------

transaction_features_sample_df = pd.read_csv(

    TRANSACTION_FEATURES_FILE,

    nrows=10

)


# ------------------------------------------------------------
# DISPLAY DATASET SIZES
# ------------------------------------------------------------

print("Reference Dataset Summary\n")

print(
    f"Banks                         : "
    f"{len(banks_df):,}"
)

print(
    f"Customers                     : "
    f"{len(customers_df):,}"
)

print(
    f"Accounts                      : "
    f"{len(accounts_df):,}"
)

print(
    f"AML Patterns                  : "
    f"{len(aml_patterns_df):,}"
)

print(
    f"AML Pattern Transactions      : "
    f"{len(aml_pattern_transactions_df):,}"
)

print(
    f"Transaction Feature Sample    : "
    f"{len(transaction_features_sample_df):,}"
)


# ------------------------------------------------------------
# VALIDATE EXPECTED ROW COUNTS
# ------------------------------------------------------------

print("\nValidating dataset sizes...\n")


assert len(accounts_df) == EXPECTED_ACCOUNT_COUNT

assert len(aml_patterns_df) == EXPECTED_AML_PATTERN_COUNT

assert (
    len(aml_pattern_transactions_df)
    ==
    EXPECTED_PATTERN_TRANSACTION_COUNT
)

assert len(transaction_features_sample_df) == 10


print("All dataset size checks passed.")


# ------------------------------------------------------------
# STEP COMPLETION
# ------------------------------------------------------------

print("\nSTEP 1 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 2
# VALIDATE TRANSACTION FEATURE DATASET
# ============================================================

print("\n" + "=" * 70)
print("STEP 2: VALIDATE TRANSACTION FEATURE DATASET")
print("=" * 70)


# ------------------------------------------------------------
# EXPECTED TRANSACTION FEATURE SCHEMA
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
# ACTUAL SCHEMA
# ------------------------------------------------------------

actual_columns = (
    transaction_features_sample_df.columns.tolist()
)


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


column_order_matches = (

    actual_columns

    ==

    EXPECTED_TRANSACTION_FEATURE_COLUMNS

)


# ------------------------------------------------------------
# DISPLAY SCHEMA VALIDATION RESULTS
# ------------------------------------------------------------

print("\nTransaction Feature Schema Results\n")


print(
    f"Expected Column Count : "
    f"{len(EXPECTED_TRANSACTION_FEATURE_COLUMNS)}"
)

print(
    f"Actual Column Count   : "
    f"{len(actual_columns)}"
)

print(
    f"Missing Columns       : "
    f"{missing_columns}"
)

print(
    f"Unexpected Columns    : "
    f"{unexpected_columns}"
)

print(
    f"Column Order Matches  : "
    f"{column_order_matches}"
)


schema_valid = (

    len(missing_columns) == 0

    and

    len(unexpected_columns) == 0

    and

    column_order_matches

)


print(
    f"\nSchema Status : "
    f"{'PASS' if schema_valid else 'FAIL'}"
)


if not schema_valid:

    raise ValueError(
        "Transaction feature schema validation failed."
    )


# ------------------------------------------------------------
# VALIDATE SAMPLE TIMESTAMPS
# ------------------------------------------------------------

transaction_features_sample_df["timestamp"] = pd.to_datetime(

    transaction_features_sample_df["timestamp"],

    errors="coerce"

)


invalid_timestamps = int(

    transaction_features_sample_df["timestamp"]

    .isna()

    .sum()

)


print("\nTimestamp Validation\n")


print(
    f"Invalid Sample Timestamps : "
    f"{invalid_timestamps:,}"
)

print(
    f"Minimum Timestamp         : "
    f"{transaction_features_sample_df['timestamp'].min()}"
)

print(
    f"Maximum Timestamp         : "
    f"{transaction_features_sample_df['timestamp'].max()}"
)


if invalid_timestamps > 0:

    raise ValueError(
        "Invalid timestamps detected."
    )


# ------------------------------------------------------------
# DISPLAY SAMPLE DATA
# ------------------------------------------------------------

print("\nFirst 10 Transaction Feature Records\n")

print(transaction_features_sample_df)


# ------------------------------------------------------------
# STEP COMPLETION
# ------------------------------------------------------------

print("\nSTEP 2 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 3
# CONFIGURE ACCOUNT FEATURE CONTRACT
# ============================================================

print("\n" + "=" * 70)
print("STEP 3: CONFIGURE ACCOUNT FEATURE CONTRACT")
print("=" * 70)


# ------------------------------------------------------------
# ACCOUNT IDENTIFICATION COLUMNS
# ------------------------------------------------------------

ACCOUNT_IDENTIFIER_COLUMNS = [

    "account_id",

    "customer_id",

    "bank_id"

]


# ------------------------------------------------------------
# TRANSACTION VOLUME FEATURES
# ------------------------------------------------------------

ACCOUNT_VOLUME_FEATURE_COLUMNS = [

    "total_sent_transactions",

    "total_received_transactions",

    "total_transactions"

]


# ------------------------------------------------------------
# MONETARY FEATURES
# ------------------------------------------------------------

ACCOUNT_MONETARY_FEATURE_COLUMNS = [

    "total_amount_sent",

    "total_amount_received",

    "average_amount_sent",

    "average_amount_received",

    "maximum_amount_sent",

    "maximum_amount_received",

    "minimum_amount_sent",

    "minimum_amount_received"

]


# ------------------------------------------------------------
# BEHAVIOURAL FEATURES
# ------------------------------------------------------------

ACCOUNT_BEHAVIOURAL_FEATURE_COLUMNS = [

    "night_transaction_count",

    "weekend_transaction_count",

    "cross_bank_transaction_count",

    "self_transfer_count",

    "currency_mismatch_count"

]


# ------------------------------------------------------------
# AML FEATURES
# ------------------------------------------------------------

ACCOUNT_AML_FEATURE_COLUMNS = [

    "known_aml_pattern_transaction_count",

    "laundering_transaction_count"

]


# ------------------------------------------------------------
# TEMPORAL FEATURES
# ------------------------------------------------------------

ACCOUNT_TEMPORAL_FEATURE_COLUMNS = [

    "first_transaction_timestamp",

    "last_transaction_timestamp"

]


# ------------------------------------------------------------
# FINAL ACCOUNT FEATURE SCHEMA
# ------------------------------------------------------------

ACCOUNT_FEATURE_COLUMNS = (

    ACCOUNT_IDENTIFIER_COLUMNS

    + ACCOUNT_VOLUME_FEATURE_COLUMNS

    + ACCOUNT_MONETARY_FEATURE_COLUMNS

    + ACCOUNT_BEHAVIOURAL_FEATURE_COLUMNS

    + ACCOUNT_AML_FEATURE_COLUMNS

    + ACCOUNT_TEMPORAL_FEATURE_COLUMNS

)


# ------------------------------------------------------------
# VERIFY DUPLICATE COLUMN NAMES
# ------------------------------------------------------------

duplicate_columns = [

    column

    for column in ACCOUNT_FEATURE_COLUMNS

    if ACCOUNT_FEATURE_COLUMNS.count(column) > 1

]

duplicate_columns = sorted(set(duplicate_columns))


print("\nAccount Feature Contract\n")


print(
    f"Identifier Columns : "
    f"{len(ACCOUNT_IDENTIFIER_COLUMNS)}"
)

print(
    f"Volume Features    : "
    f"{len(ACCOUNT_VOLUME_FEATURE_COLUMNS)}"
)

print(
    f"Monetary Features  : "
    f"{len(ACCOUNT_MONETARY_FEATURE_COLUMNS)}"
)

print(
    f"Behaviour Features : "
    f"{len(ACCOUNT_BEHAVIOURAL_FEATURE_COLUMNS)}"
)

print(
    f"AML Features       : "
    f"{len(ACCOUNT_AML_FEATURE_COLUMNS)}"
)

print(
    f"Temporal Features  : "
    f"{len(ACCOUNT_TEMPORAL_FEATURE_COLUMNS)}"
)

print(
    f"Total Columns      : "
    f"{len(ACCOUNT_FEATURE_COLUMNS)}"
)

print(
    f"Duplicate Columns  : "
    f"{duplicate_columns}"
)


if duplicate_columns:

    raise ValueError(
        "Duplicate columns detected in account feature contract."
    )


print("\nSTEP 3 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 4
# INITIALIZE ACCOUNT AGGREGATION STRUCTURES
# ============================================================

print("\n" + "=" * 70)
print("STEP 4: INITIALIZE ACCOUNT AGGREGATION STRUCTURES")
print("=" * 70)


# ------------------------------------------------------------
# ACCOUNT AGGREGATION TEMPLATE
# ------------------------------------------------------------

account_statistics = defaultdict(

    lambda: {

        "sent_transaction_count": 0,

        "received_transaction_count": 0,

        "total_amount_sent": 0.0,

        "total_amount_received": 0.0,

        "maximum_amount_sent": 0.0,

        "maximum_amount_received": 0.0,

        "minimum_amount_sent": np.inf,

        "minimum_amount_received": np.inf,

        "night_transaction_count": 0,

        "weekend_transaction_count": 0,

        "cross_bank_transaction_count": 0,

        "self_transfer_count": 0,

        "currency_mismatch_count": 0,

        "known_aml_pattern_transaction_count": 0,

        "laundering_transaction_count": 0,

        "first_transaction_timestamp": None,

        "last_transaction_timestamp": None

    }

)


# ------------------------------------------------------------
# DISPLAY INITIALIZATION SUMMARY
# ------------------------------------------------------------

print("\nAggregation structures initialized successfully.\n")

print(f"Initial Accounts Loaded : {len(account_statistics):,}")

print(f"Expected Accounts       : {EXPECTED_ACCOUNT_COUNT:,}")


print("\nSTEP 4 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 5
# PROCESS TRANSACTION FEATURE CHUNKS
# ============================================================

print("\n" + "=" * 70)
print("STEP 5: PROCESS TRANSACTION FEATURE CHUNKS")
print("=" * 70)


# ------------------------------------------------------------
# INITIALIZE PROCESSING VARIABLES
# ------------------------------------------------------------

total_processed_rows = 0

processed_chunks = 0


print("\nReading transaction feature dataset in chunks...\n")


# ------------------------------------------------------------
# PROCESS EACH CHUNK
# ------------------------------------------------------------

transaction_feature_chunks = pd.read_csv(

    TRANSACTION_FEATURES_FILE,

    chunksize=TRANSACTION_CHUNK_SIZE

)


for chunk in transaction_feature_chunks:

    processed_chunks += 1

    print(
        f"Processing Chunk "
        f"{processed_chunks:>2} "
        f"({len(chunk):,} rows)"
    )


    # --------------------------------------------------------
    # VALIDATE COLUMN STRUCTURE
    # --------------------------------------------------------

    if list(chunk.columns) != EXPECTED_TRANSACTION_FEATURE_COLUMNS:

        raise ValueError(

            f"Schema mismatch detected in "

            f"Chunk {processed_chunks}."

        )


    # --------------------------------------------------------
    # CONVERT TIMESTAMP COLUMN
    # --------------------------------------------------------

    chunk["timestamp"] = pd.to_datetime(

        chunk["timestamp"],

        errors="coerce"

    )


    if chunk["timestamp"].isna().any():

        raise ValueError(

            f"Invalid timestamps found in "

            f"Chunk {processed_chunks}."

        )


    # --------------------------------------------------------
    # CONVERT NUMERIC COLUMNS
    # --------------------------------------------------------

    numeric_columns = [

        "amount_paid",

        "amount_received",

        "amount_difference",

        "amount_ratio",

        "log_amount_paid",

        "log_amount_received"

    ]


    for column in numeric_columns:

        chunk[column] = pd.to_numeric(

            chunk[column],

            errors="coerce"

        )


    if chunk[numeric_columns].isna().any().any():

        raise ValueError(

            f"Invalid numeric values found "

            f"in Chunk {processed_chunks}."

        )


    total_processed_rows += len(chunk)


# ------------------------------------------------------------
# VALIDATE FINAL ROW COUNT
# ------------------------------------------------------------

print("\nChunk Processing Summary\n")


print(
    f"Chunks Processed : "
    f"{processed_chunks}"
)

print(
    f"Rows Processed   : "
    f"{total_processed_rows:,}"
)


assert (

    total_processed_rows

    ==

    EXPECTED_TRANSACTION_FEATURE_COUNT

), (

    "Unexpected transaction feature row count."

)


print("\nSTEP 5 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 6
# AGGREGATE SENDER STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("STEP 6: AGGREGATE SENDER STATISTICS")
print("=" * 70)


processed_chunks = 0

total_processed_rows = 0


for chunk in pd.read_csv(

    TRANSACTION_FEATURES_FILE,

    chunksize=TRANSACTION_CHUNK_SIZE

):

    processed_chunks += 1

    print(
        f"Processing Chunk {processed_chunks}"
    )


    chunk["timestamp"] = pd.to_datetime(
        chunk["timestamp"]
    )


    sender_summary = (

        chunk

        .groupby("sender_account_id")

        .agg(

            sent_transaction_count=(
                "transaction_id",
                "count"
            ),

            total_amount_sent=(
                "amount_paid",
                "sum"
            ),

            average_amount_sent=(
                "amount_paid",
                "mean"
            ),

            maximum_amount_sent=(
                "amount_paid",
                "max"
            ),

            minimum_amount_sent=(
                "amount_paid",
                "min"
            ),

            first_transaction_timestamp=(
                "timestamp",
                "min"
            ),

            last_transaction_timestamp=(
                "timestamp",
                "max"
            )

        )

        .reset_index()

    )


    for row in sender_summary.itertuples(index=False):

        account = account_statistics[
            row.sender_account_id
        ]

        account["sent_transaction_count"] += (
            row.sent_transaction_count
        )

        account["total_amount_sent"] += (
            row.total_amount_sent
        )

        account["maximum_amount_sent"] = max(

            account["maximum_amount_sent"],

            row.maximum_amount_sent

        )

        account["minimum_amount_sent"] = min(

            account["minimum_amount_sent"],

            row.minimum_amount_sent

        )


        if (

            account["first_transaction_timestamp"] is None

            or

            row.first_transaction_timestamp
            <
            account["first_transaction_timestamp"]

        ):

            account["first_transaction_timestamp"] = (
                row.first_transaction_timestamp
            )


        if (

            account["last_transaction_timestamp"] is None

            or

            row.last_transaction_timestamp
            >
            account["last_transaction_timestamp"]

        ):

            account["last_transaction_timestamp"] = (
                row.last_transaction_timestamp
            )


    total_processed_rows += len(chunk)


print("\nSender Aggregation Summary\n")

print(f"Chunks Processed : {processed_chunks}")

print(f"Rows Processed   : {total_processed_rows:,}")

print(
    f"Sender Accounts Aggregated : "
    f"{len(account_statistics):,}"
)

print("\nSTEP 6 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 7
# AGGREGATE RECEIVER STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("STEP 7: AGGREGATE RECEIVER STATISTICS")
print("=" * 70)


processed_chunks = 0
total_processed_rows = 0


for chunk in pd.read_csv(
    TRANSACTION_FEATURES_FILE,
    chunksize=TRANSACTION_CHUNK_SIZE
):

    processed_chunks += 1

    print(f"Processing Chunk {processed_chunks}")

    chunk["timestamp"] = pd.to_datetime(chunk["timestamp"])


    receiver_summary = (

        chunk

        .groupby("receiver_account_id")

        .agg(

            received_transaction_count=(
                "transaction_id",
                "count"
            ),

            total_amount_received=(
                "amount_received",
                "sum"
            ),

            average_amount_received=(
                "amount_received",
                "mean"
            ),

            maximum_amount_received=(
                "amount_received",
                "max"
            ),

            minimum_amount_received=(
                "amount_received",
                "min"
            )

        )

        .reset_index()

    )


    for row in receiver_summary.itertuples(index=False):

        account = account_statistics[
            row.receiver_account_id
        ]

        account["received_transaction_count"] += (
            row.received_transaction_count
        )

        account["total_amount_received"] += (
            row.total_amount_received
        )

        account["maximum_amount_received"] = max(

            account["maximum_amount_received"],

            row.maximum_amount_received

        )

        account["minimum_amount_received"] = min(

            account["minimum_amount_received"],

            row.minimum_amount_received

        )


    total_processed_rows += len(chunk)


print("\nReceiver Aggregation Summary\n")

print(f"Chunks Processed : {processed_chunks}")

print(f"Rows Processed   : {total_processed_rows:,}")

print(
    f"Total Accounts Aggregated : "
    f"{len(account_statistics):,}"
)

print("\nSTEP 7 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 8
# BUILD ACCOUNT FEATURES DATASET
# ============================================================

print("\n" + "=" * 70)
print("STEP 8: BUILD ACCOUNT FEATURES DATASET")
print("=" * 70)


# ------------------------------------------------------------
# CREATE ACCOUNT FEATURES DATAFRAME
# ------------------------------------------------------------

account_features_df = accounts_df.copy()


# ------------------------------------------------------------
# ADD AGGREGATED FEATURES
# ------------------------------------------------------------

aggregation_df = (

    pd.DataFrame

    .from_dict(

        account_statistics,

        orient="index"

    )

    .reset_index()

    .rename(

        columns={

            "index": "account_id"

        }

    )

)


account_features_df = account_features_df.merge(

    aggregation_df,

    on="account_id",

    how="left"

)


# ------------------------------------------------------------
# REPLACE MISSING VALUES
# ------------------------------------------------------------

numeric_columns = account_features_df.select_dtypes(

    include=[np.number]

).columns


account_features_df[numeric_columns] = (

    account_features_df[numeric_columns]

    .fillna(0)

)


# ------------------------------------------------------------
# DERIVE ACCOUNT FEATURES
# ------------------------------------------------------------

account_features_df["total_transactions"] = (

    account_features_df["sent_transaction_count"]

    +

    account_features_df["received_transaction_count"]

)


account_features_df["average_amount_sent"] = np.where(

    account_features_df["sent_transaction_count"] > 0,

    account_features_df["total_amount_sent"]

    /

    account_features_df["sent_transaction_count"],

    0

)


account_features_df["average_amount_received"] = np.where(

    account_features_df["received_transaction_count"] > 0,

    account_features_df["total_amount_received"]

    /

    account_features_df["received_transaction_count"],

    0

)


# ------------------------------------------------------------
# DISPLAY SUMMARY
# ------------------------------------------------------------

print("\nAccount Feature Dataset Summary\n")

print(

    f"Rows    : "

    f"{len(account_features_df):,}"

)

print(

    f"Columns : "

    f"{len(account_features_df.columns):,}"

)


print("\nSTEP 8 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 9
# FINAL ACCOUNT FEATURE VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("STEP 9: FINAL ACCOUNT FEATURE VALIDATION")
print("=" * 70)


# ------------------------------------------------------------
# VALIDATE ROW COUNT
# ------------------------------------------------------------

assert len(account_features_df) == EXPECTED_ACCOUNT_COUNT


# ------------------------------------------------------------
# VALIDATE DUPLICATE ACCOUNT IDS
# ------------------------------------------------------------

duplicate_accounts = (

    account_features_df["account_id"]

    .duplicated()

    .sum()

)

assert duplicate_accounts == 0


# ------------------------------------------------------------
# VALIDATE MISSING ACCOUNT IDS
# ------------------------------------------------------------

missing_account_ids = (

    account_features_df["account_id"]

    .isna()

    .sum()

)

assert missing_account_ids == 0


# ------------------------------------------------------------
# DISPLAY VALIDATION SUMMARY
# ------------------------------------------------------------

print("\nValidation Summary\n")

print(f"Rows                 : {len(account_features_df):,}")

print(f"Duplicate Accounts   : {duplicate_accounts}")

print(f"Missing Account IDs  : {missing_account_ids}")

print("\nAll validation checks passed.")

print("\nSTEP 9 COMPLETED SUCCESSFULLY.")

# ============================================================
# STEP 10
# EXPORT ACCOUNT FEATURES DATASET
# ============================================================

print("\n" + "=" * 70)
print("STEP 10: EXPORT ACCOUNT FEATURES DATASET")
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

account_features_df.to_csv(

    ACCOUNT_FEATURES_FILE,

    index=False

)


# ------------------------------------------------------------
# EXPORT SUMMARY
# ------------------------------------------------------------

print("\nExport Summary\n")

print(f"Output File : {ACCOUNT_FEATURES_FILE}")

print(f"Rows        : {len(account_features_df):,}")

print(f"Columns     : {len(account_features_df.columns)}")

print("\nAccount feature dataset exported successfully.")

print("\nSTEP 10 COMPLETED SUCCESSFULLY.")

