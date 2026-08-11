from pathlib import Path

import pandas as pd


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "DATA" / "RAW"
CLEANED_DATA_DIR = PROJECT_ROOT / "DATA" / "CLEANED"

TRANSACTIONS_FILE = RAW_DATA_DIR / "HI-Small_Trans.csv"
CLEANED_ACCOUNTS_FILE = CLEANED_DATA_DIR / "accounts.csv"


# --------------------------------------------------
# CHUNK CONFIGURATION
# --------------------------------------------------

CHUNK_SIZE = 250_000


# --------------------------------------------------
# SCRIPT HEADER
# --------------------------------------------------

print("=" * 70)
print("BANKING FRAUD & FINANCIAL RISK INTELLIGENCE PLATFORM")
print("PHASE 2: CLEANING & STANDARDIZATION")
print("STEP 2: CLEAN TRANSACTIONS DATASET")
print("=" * 70)

print(f"\nProject Root             : {PROJECT_ROOT}")
print(f"Raw Transactions File    : {TRANSACTIONS_FILE}")
print(f"Cleaned Accounts File    : {CLEANED_ACCOUNTS_FILE}")
print(f"Cleaned Data Directory   : {CLEANED_DATA_DIR}")
print(f"Transaction Chunk Size   : {CHUNK_SIZE:,}")


# --------------------------------------------------
# VERIFY REQUIRED FILES
# --------------------------------------------------

if not TRANSACTIONS_FILE.exists():
    raise FileNotFoundError(
        f"Raw transactions file not found: {TRANSACTIONS_FILE}"
    )

if not CLEANED_ACCOUNTS_FILE.exists():
    raise FileNotFoundError(
        f"Cleaned accounts file not found: {CLEANED_ACCOUNTS_FILE}"
    )

print("\nAll required input files were found successfully.")


# --------------------------------------------------
# LOAD ACCOUNT MAPPING
# --------------------------------------------------

print("\nLoading cleaned account mapping...")

account_mapping_df = pd.read_csv(
    CLEANED_ACCOUNTS_FILE,
    usecols=[
        "account_id",
        "bank_id",
        "account_number"
    ],
    dtype={
        "account_id": "string",
        "bank_id": "int64",
        "account_number": "string"
    }
)


print("Cleaned account mapping loaded successfully.")

print(f"\nAccount Mapping Rows: {len(account_mapping_df):,}")

print(
    f"Unique Account IDs: "
    f"{account_mapping_df['account_id'].nunique():,}"
)

print(
    f"Unique Composite Account Keys: "
    f"{account_mapping_df[['bank_id', 'account_number']].drop_duplicates().shape[0]:,}"
)


# --------------------------------------------------
# VALIDATE ACCOUNT MAPPING
# --------------------------------------------------

if account_mapping_df["account_id"].duplicated().any():
    raise ValueError(
        "Account mapping contains duplicate account_id values."
    )


if account_mapping_df.duplicated(
    subset=["bank_id", "account_number"]
).any():

    raise ValueError(
        "Account mapping contains duplicate "
        "(bank_id, account_number) keys."
    )


print("\nAccount mapping validation passed successfully.")


# --------------------------------------------------
# LOAD TRANSACTION SAMPLE
# --------------------------------------------------

print("\nLoading transaction sample...")

transactions_sample_df = pd.read_csv(
    TRANSACTIONS_FILE,
    nrows=5
)

print("Transaction sample loaded successfully.")

print(f"\nSample Rows   : {len(transactions_sample_df):,}")
print(f"Sample Columns: {len(transactions_sample_df.columns):,}")

print("\nTransaction Columns:")

for column in transactions_sample_df.columns:
    print(f"  - {column}")

print("\nFirst 5 Transaction Records:")
print(transactions_sample_df)

# --------------------------------------------------
# PREPARE SENDER AND RECEIVER ACCOUNT MAPPINGS
# --------------------------------------------------

print("\n" + "=" * 70)
print("PREPARING TRANSACTION ACCOUNT MAPPINGS")
print("=" * 70)


# Sender mapping:
# (From Bank, Account) -> sender_account_id

sender_account_mapping_df = (
    account_mapping_df
    .rename(
        columns={
            "bank_id": "from_bank_id",
            "account_number": "sender_account_number",
            "account_id": "sender_account_id"
        }
    )
)


# Receiver mapping:
# (To Bank, Account.1) -> receiver_account_id

receiver_account_mapping_df = (
    account_mapping_df
    .rename(
        columns={
            "bank_id": "to_bank_id",
            "account_number": "receiver_account_number",
            "account_id": "receiver_account_id"
        }
    )
)


# --------------------------------------------------
# VALIDATE MAPPING ROW COUNTS
# --------------------------------------------------

if len(sender_account_mapping_df) != len(account_mapping_df):
    raise ValueError(
        "Sender account mapping row count mismatch."
    )


if len(receiver_account_mapping_df) != len(account_mapping_df):
    raise ValueError(
        "Receiver account mapping row count mismatch."
    )


# --------------------------------------------------
# VALIDATE COMPOSITE KEY UNIQUENESS
# --------------------------------------------------

if sender_account_mapping_df.duplicated(
    subset=[
        "from_bank_id",
        "sender_account_number"
    ]
).any():

    raise ValueError(
        "Duplicate sender composite account keys detected."
    )


if receiver_account_mapping_df.duplicated(
    subset=[
        "to_bank_id",
        "receiver_account_number"
    ]
).any():

    raise ValueError(
        "Duplicate receiver composite account keys detected."
    )


print("\nTransaction account mappings prepared successfully.")

print(
    f"Sender Mapping Rows  : "
    f"{len(sender_account_mapping_df):,}"
)

print(
    f"Receiver Mapping Rows: "
    f"{len(receiver_account_mapping_df):,}"
)

print("\nSender Mapping Columns:")

for column in sender_account_mapping_df.columns:
    print(f"  - {column}")


print("\nReceiver Mapping Columns:")

for column in receiver_account_mapping_df.columns:
    print(f"  - {column}")


print("\nFirst 5 Sender Mapping Records:")
print(sender_account_mapping_df.head())


print("\nFirst 5 Receiver Mapping Records:")
print(receiver_account_mapping_df.head())

# --------------------------------------------------
# CLEANED TRANSACTION OUTPUT CONFIGURATION
# --------------------------------------------------

print("\n" + "=" * 70)
print("CONFIGURING CLEANED TRANSACTION PROCESSING")
print("=" * 70)


CLEANED_TRANSACTIONS_FILE = (
    CLEANED_DATA_DIR / "transactions.csv"
)


# Remove an old incomplete output file if the script
# was previously interrupted or executed.
if CLEANED_TRANSACTIONS_FILE.exists():

    CLEANED_TRANSACTIONS_FILE.unlink()

    print(
        "\nExisting transactions.csv removed "
        "before starting a new processing run."
    )


# --------------------------------------------------
# DEFINE RAW TRANSACTION COLUMN TYPES
# --------------------------------------------------

TRANSACTION_DTYPES = {

    "From Bank": "int64",

    "Account": "string",

    "To Bank": "int64",

    "Account.1": "string",

    "Amount Received": "float64",

    "Receiving Currency": "string",

    "Amount Paid": "float64",

    "Payment Currency": "string",

    "Payment Format": "string",

    "Is Laundering": "int64"
}


# --------------------------------------------------
# DEFINE STANDARDIZED COLUMN NAMES
# --------------------------------------------------

TRANSACTION_COLUMN_MAPPING = {

    "Timestamp": "timestamp",

    "From Bank": "from_bank_id",

    "Account": "sender_account_number",

    "To Bank": "to_bank_id",

    "Account.1": "receiver_account_number",

    "Amount Received": "amount_received",

    "Receiving Currency": "receiving_currency",

    "Amount Paid": "amount_paid",

    "Payment Currency": "payment_currency",

    "Payment Format": "payment_format",

    "Is Laundering": "is_laundering"
}


# --------------------------------------------------
# DEFINE FINAL CLEANED TRANSACTION SCHEMA
# --------------------------------------------------

FINAL_TRANSACTION_COLUMNS = [

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

    "is_laundering"
]


print("\nCleaned transaction processing configuration completed.")

print(f"\nOutput File: {CLEANED_TRANSACTIONS_FILE}")

print(f"Chunk Size : {CHUNK_SIZE:,}")

print("\nFinal Transaction Columns:")

for column in FINAL_TRANSACTION_COLUMNS:
    print(f"  - {column}")

# --------------------------------------------------
# PROCESS TRANSACTIONS IN CHUNKS
# --------------------------------------------------

print("\n" + "=" * 70)
print("PROCESSING TRANSACTIONS IN CHUNKS")
print("=" * 70)


# --------------------------------------------------
# PROCESSING COUNTERS
# --------------------------------------------------

total_raw_rows = 0
total_duplicate_rows_removed = 0
total_cleaned_rows = 0

total_invalid_timestamps = 0

total_orphan_sender_rows = 0
total_orphan_receiver_rows = 0

total_laundering_rows = 0

transaction_id_counter = 1

first_output_chunk = True


# --------------------------------------------------
# GLOBAL DUPLICATE TRACKING
# --------------------------------------------------

# Stores 64-bit hashes of complete raw transaction rows.
# This allows duplicate detection across different chunks.

seen_row_hashes = set()


# --------------------------------------------------
# READ RAW TRANSACTIONS IN CHUNKS
# --------------------------------------------------

transaction_reader = pd.read_csv(
    TRANSACTIONS_FILE,
    chunksize=CHUNK_SIZE,
    dtype=TRANSACTION_DTYPES
)


for chunk_number, chunk_df in enumerate(
    transaction_reader,
    start=1
):

    print(
        f"\nProcessing Chunk {chunk_number} "
        f"({len(chunk_df):,} raw rows)..."
    )


    # ----------------------------------------------
    # COUNT RAW ROWS
    # ----------------------------------------------

    total_raw_rows += len(chunk_df)


    # ----------------------------------------------
    # GLOBAL EXACT DUPLICATE DETECTION
    # ----------------------------------------------

    row_hashes = pd.util.hash_pandas_object(
        chunk_df,
        index=False
    )


    keep_mask = []

    for row_hash in row_hashes:

        hash_value = int(row_hash)

        if hash_value in seen_row_hashes:

            keep_mask.append(False)

        else:

            seen_row_hashes.add(hash_value)

            keep_mask.append(True)


    duplicate_rows_removed = (
        len(chunk_df) - sum(keep_mask)
    )

    total_duplicate_rows_removed += duplicate_rows_removed


    chunk_df = (
        chunk_df.loc[keep_mask]
        .copy()
        .reset_index(drop=True)
    )


    # ----------------------------------------------
    # STANDARDIZE COLUMN NAMES
    # ----------------------------------------------

    chunk_df = chunk_df.rename(
        columns=TRANSACTION_COLUMN_MAPPING
    )


    # ----------------------------------------------
    # PARSE AND VALIDATE TIMESTAMP
    # ----------------------------------------------

    chunk_df["timestamp"] = pd.to_datetime(
        chunk_df["timestamp"],
        format="%Y/%m/%d %H:%M",
        errors="coerce"
    )


    invalid_timestamps = (
        chunk_df["timestamp"]
        .isna()
        .sum()
    )

    total_invalid_timestamps += invalid_timestamps


    if invalid_timestamps > 0:

        raise ValueError(
            f"Chunk {chunk_number}: "
            f"{invalid_timestamps:,} invalid timestamps detected."
        )


    # ----------------------------------------------
    # MAP SENDER ACCOUNT ID
    # ----------------------------------------------

    chunk_df = chunk_df.merge(
        sender_account_mapping_df,
        on=[
            "from_bank_id",
            "sender_account_number"
        ],
        how="left",
        validate="many_to_one"
    )


    # ----------------------------------------------
    # MAP RECEIVER ACCOUNT ID
    # ----------------------------------------------

    chunk_df = chunk_df.merge(
        receiver_account_mapping_df,
        on=[
            "to_bank_id",
            "receiver_account_number"
        ],
        how="left",
        validate="many_to_one"
    )


    # ----------------------------------------------
    # VALIDATE ACCOUNT REFERENCES
    # ----------------------------------------------

    orphan_sender_rows = (
        chunk_df["sender_account_id"]
        .isna()
        .sum()
    )

    orphan_receiver_rows = (
        chunk_df["receiver_account_id"]
        .isna()
        .sum()
    )


    total_orphan_sender_rows += orphan_sender_rows
    total_orphan_receiver_rows += orphan_receiver_rows


    if orphan_sender_rows > 0:

        raise ValueError(
            f"Chunk {chunk_number}: "
            f"{orphan_sender_rows:,} orphan sender rows detected."
        )


    if orphan_receiver_rows > 0:

        raise ValueError(
            f"Chunk {chunk_number}: "
            f"{orphan_receiver_rows:,} orphan receiver rows detected."
        )


    # ----------------------------------------------
    # COUNT LAUNDERING TRANSACTIONS
    # ----------------------------------------------

    total_laundering_rows += int(
        chunk_df["is_laundering"].sum()
    )


    # ----------------------------------------------
    # CREATE STABLE TRANSACTION IDS
    # ----------------------------------------------

    number_of_clean_rows = len(chunk_df)

    transaction_ids = [

        f"TXN_{number:08d}"

        for number in range(
            transaction_id_counter,
            transaction_id_counter
            + number_of_clean_rows
        )
    ]


    chunk_df.insert(
        0,
        "transaction_id",
        transaction_ids
    )


    transaction_id_counter += number_of_clean_rows


    # ----------------------------------------------
    # SELECT FINAL TRANSACTION SCHEMA
    # ----------------------------------------------

    chunk_df = chunk_df[
        FINAL_TRANSACTION_COLUMNS
    ]


    # ----------------------------------------------
    # WRITE CLEANED CHUNK TO CSV
    # ----------------------------------------------

    chunk_df.to_csv(
        CLEANED_TRANSACTIONS_FILE,
        mode="w" if first_output_chunk else "a",
        header=first_output_chunk,
        index=False
    )


    first_output_chunk = False

    total_cleaned_rows += len(chunk_df)


    # ----------------------------------------------
    # PRINT CHUNK RESULTS
    # ----------------------------------------------

    print(
        f"  Raw Rows              : "
        f"{len(keep_mask):,}"
    )

    print(
        f"  Duplicates Removed    : "
        f"{duplicate_rows_removed:,}"
    )

    print(
        f"  Cleaned Rows Written  : "
        f"{len(chunk_df):,}"
    )

    print(
        f"  Orphan Sender Rows    : "
        f"{orphan_sender_rows:,}"
    )

    print(
        f"  Orphan Receiver Rows  : "
        f"{orphan_receiver_rows:,}"
    )


print("\n" + "=" * 70)
print("TRANSACTION CHUNK PROCESSING COMPLETED")
print("=" * 70)

print(f"\nTotal Raw Rows                : {total_raw_rows:,}")
print(f"Total Duplicate Rows Removed  : {total_duplicate_rows_removed:,}")
print(f"Total Cleaned Rows Written    : {total_cleaned_rows:,}")

print(f"\nInvalid Timestamps            : {total_invalid_timestamps:,}")
print(f"Orphan Sender Rows            : {total_orphan_sender_rows:,}")
print(f"Orphan Receiver Rows          : {total_orphan_receiver_rows:,}")

print(f"\nLaundering Transactions       : {total_laundering_rows:,}")

print(
    f"Final Transaction ID Counter  : "
    f"{transaction_id_counter - 1:,}"
)

# --------------------------------------------------
# VALIDATE CLEANED TRANSACTIONS FILE FROM DISK
# --------------------------------------------------

print("\n" + "=" * 70)
print("VALIDATING CLEANED TRANSACTIONS FILE FROM DISK")
print("=" * 70)


EXPECTED_RAW_ROWS = 5_078_345
EXPECTED_DUPLICATE_ROWS = 9
EXPECTED_CLEANED_ROWS = 5_078_336
EXPECTED_LAUNDERING_ROWS = 5_177


# --------------------------------------------------
# VALIDATION COUNTERS
# --------------------------------------------------

validated_rows = 0
validated_laundering_rows = 0

missing_values_by_column = {
    column: 0
    for column in FINAL_TRANSACTION_COLUMNS
}

unique_transaction_ids = set()

duplicate_transaction_id_count = 0

invalid_sender_account_ids = 0
invalid_receiver_account_ids = 0


# Valid account IDs for foreign-key validation
valid_account_ids = set(
    account_mapping_df["account_id"]
)


# --------------------------------------------------
# READ CLEANED FILE IN CHUNKS
# --------------------------------------------------

validation_reader = pd.read_csv(
    CLEANED_TRANSACTIONS_FILE,
    chunksize=CHUNK_SIZE,
    dtype={
        "transaction_id": "string",
        "sender_account_id": "string",
        "receiver_account_id": "string",
        "sender_account_number": "string",
        "receiver_account_number": "string"
    }
)


for validation_chunk_number, validation_chunk_df in enumerate(
    validation_reader,
    start=1
):

    print(
        f"Validating Chunk "
        f"{validation_chunk_number} "
        f"({len(validation_chunk_df):,} rows)..."
    )


    # ----------------------------------------------
    # VALIDATE EXACT COLUMN ORDER
    # ----------------------------------------------

    if list(validation_chunk_df.columns) != FINAL_TRANSACTION_COLUMNS:

        raise ValueError(
            "Cleaned transactions file schema mismatch."
        )


    # ----------------------------------------------
    # COUNT ROWS
    # ----------------------------------------------

    validated_rows += len(validation_chunk_df)


    # ----------------------------------------------
    # COUNT MISSING VALUES
    # ----------------------------------------------

    chunk_missing_values = (
        validation_chunk_df
        .isna()
        .sum()
    )


    for column in FINAL_TRANSACTION_COLUMNS:

        missing_values_by_column[column] += int(
            chunk_missing_values[column]
        )


    # ----------------------------------------------
    # VALIDATE TRANSACTION ID UNIQUENESS
    # ----------------------------------------------

    for transaction_id in validation_chunk_df["transaction_id"]:

        if transaction_id in unique_transaction_ids:

            duplicate_transaction_id_count += 1

        else:

            unique_transaction_ids.add(transaction_id)


    # ----------------------------------------------
    # VALIDATE ACCOUNT FOREIGN KEYS
    # ----------------------------------------------

    invalid_sender_account_ids += int(
        (
            ~validation_chunk_df[
                "sender_account_id"
            ].isin(valid_account_ids)
        ).sum()
    )


    invalid_receiver_account_ids += int(
        (
            ~validation_chunk_df[
                "receiver_account_id"
            ].isin(valid_account_ids)
        ).sum()
    )


    # ----------------------------------------------
    # COUNT LAUNDERING TRANSACTIONS
    # ----------------------------------------------

    validated_laundering_rows += int(
        validation_chunk_df[
            "is_laundering"
        ].sum()
    )


# --------------------------------------------------
# FINAL VALIDATION ASSERTIONS
# --------------------------------------------------

if total_raw_rows != EXPECTED_RAW_ROWS:

    raise ValueError(
        "Unexpected raw transaction row count."
    )


if total_duplicate_rows_removed != EXPECTED_DUPLICATE_ROWS:

    raise ValueError(
        "Unexpected duplicate transaction count."
    )


if validated_rows != EXPECTED_CLEANED_ROWS:

    raise ValueError(
        "Unexpected cleaned transaction row count."
    )


if len(unique_transaction_ids) != EXPECTED_CLEANED_ROWS:

    raise ValueError(
        "Unique transaction ID count mismatch."
    )


if duplicate_transaction_id_count != 0:

    raise ValueError(
        f"{duplicate_transaction_id_count:,} "
        "duplicate transaction IDs detected."
    )


if sum(missing_values_by_column.values()) != 0:

    raise ValueError(
        "Missing values detected in cleaned transactions."
    )


if invalid_sender_account_ids != 0:

    raise ValueError(
        f"{invalid_sender_account_ids:,} "
        "invalid sender account references detected."
    )


if invalid_receiver_account_ids != 0:

    raise ValueError(
        f"{invalid_receiver_account_ids:,} "
        "invalid receiver account references detected."
    )


if validated_laundering_rows != EXPECTED_LAUNDERING_ROWS:

    raise ValueError(
        "Laundering transaction count mismatch."
    )


# --------------------------------------------------
# PRINT VALIDATION RESULTS
# --------------------------------------------------

print("\n" + "=" * 70)
print("CLEANED TRANSACTION VALIDATION RESULTS")
print("=" * 70)

print(f"\nValidated Rows                 : {validated_rows:,}")

print(
    f"Unique Transaction IDs         : "
    f"{len(unique_transaction_ids):,}"
)

print(
    f"Duplicate Transaction IDs      : "
    f"{duplicate_transaction_id_count:,}"
)

print(
    f"Total Missing Values            : "
    f"{sum(missing_values_by_column.values()):,}"
)

print(
    f"Invalid Sender Account IDs      : "
    f"{invalid_sender_account_ids:,}"
)

print(
    f"Invalid Receiver Account IDs    : "
    f"{invalid_receiver_account_ids:,}"
)

print(
    f"Validated Laundering Transactions: "
    f"{validated_laundering_rows:,}"
)

print("\nAll cleaned transaction validations passed successfully.")

print("\nSTEP 2: CLEAN TRANSACTIONS DATASET COMPLETED SUCCESSFULLY.")

