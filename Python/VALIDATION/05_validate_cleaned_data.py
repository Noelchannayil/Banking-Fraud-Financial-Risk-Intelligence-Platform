from pathlib import Path
import pandas as pd

# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CLEANED_DATA_DIR = PROJECT_ROOT / "DATA" / "CLEANED"
REPORTS_DIR = PROJECT_ROOT / "REPORTS"

BANKS_FILE = CLEANED_DATA_DIR / "banks.csv"
CUSTOMERS_FILE = CLEANED_DATA_DIR / "customers.csv"
ACCOUNTS_FILE = CLEANED_DATA_DIR / "accounts.csv"
TRANSACTIONS_FILE = CLEANED_DATA_DIR / "transactions.csv"
AML_PATTERNS_FILE = CLEANED_DATA_DIR / "aml_patterns.csv"
AML_PATTERN_TRANSACTIONS_FILE = (
    CLEANED_DATA_DIR / "aml_pattern_transactions.csv"
)

print("=" * 70)
print("BANKING FRAUD & FINANCIAL RISK INTELLIGENCE PLATFORM")
print("PHASE 2 : CLEANED DATA VALIDATION")
print("STEP 1 : VERIFY CLEANED DATASETS")
print("=" * 70)

print(f"\nProject Root : {PROJECT_ROOT}")
print(f"Cleaned Data : {CLEANED_DATA_DIR}")
print(f"Reports      : {REPORTS_DIR}")

required_files = {
    "Banks": BANKS_FILE,
    "Customers": CUSTOMERS_FILE,
    "Accounts": ACCOUNTS_FILE,
    "Transactions": TRANSACTIONS_FILE,
    "AML Patterns": AML_PATTERNS_FILE,
    "AML Pattern Transactions": AML_PATTERN_TRANSACTIONS_FILE,
}

print("\n" + "=" * 70)
print("VERIFYING CLEANED DATA FILES")
print("=" * 70)

for name, path in required_files.items():

    if path.exists():

        size_mb = path.stat().st_size / (1024 * 1024)

        print(
            f"[FOUND] {name:<28}"
            f"{path.name:<35}"
            f"{size_mb:8.2f} MB"
        )

    else:

        raise FileNotFoundError(
            f"{name} file missing:\n{path}"
        )

print("\nAll cleaned datasets were found successfully.")

# ==========================================================
# STEP 2: LOAD CLEANED DATASETS AND VALIDATE ROW COUNTS
# ==========================================================

print("\n" + "=" * 70)
print("LOADING CLEANED DATASETS AND VALIDATING ROW COUNTS")
print("=" * 70)


# ----------------------------------------------------------
# EXPECTED CLEANED ROW COUNTS
# ----------------------------------------------------------

EXPECTED_ROW_COUNTS = {
    "banks": 30_470,
    "customers": 166_207,
    "accounts": 518_581,
    "transactions": 5_078_336,
    "aml_patterns": 370,
    "aml_pattern_transactions": 3_209,
}


# ----------------------------------------------------------
# LOAD SMALL AND MEDIUM TABLES
# ----------------------------------------------------------

print("\nLoading banks.csv...")

banks_df = pd.read_csv(
    BANKS_FILE,
    dtype={
        "bank_id": "int64",
        "bank_name": "string",
    }
)

print("banks.csv loaded successfully.")


print("\nLoading customers.csv...")

customers_df = pd.read_csv(
    CUSTOMERS_FILE,
    dtype={
        "customer_id": "string",
        "entity_id": "string",
        "entity_name": "string",
    }
)

print("customers.csv loaded successfully.")


print("\nLoading accounts.csv...")

accounts_df = pd.read_csv(
    ACCOUNTS_FILE,
    dtype={
        "account_id": "string",
        "customer_id": "string",
        "bank_id": "int64",
        "account_number": "string",
        "entity_id": "string",
    }
)

print("accounts.csv loaded successfully.")


print("\nLoading aml_patterns.csv...")

aml_patterns_df = pd.read_csv(
    AML_PATTERNS_FILE,
    dtype={
        "aml_pattern_id": "string",
        "typology": "string",
        "pattern_description": "string",
        "transaction_count": "int64",
    }
)

print("aml_patterns.csv loaded successfully.")


print("\nLoading aml_pattern_transactions.csv...")

aml_pattern_transactions_df = pd.read_csv(
    AML_PATTERN_TRANSACTIONS_FILE,
    dtype={
        "pattern_transaction_occurrence_id": "string",
        "aml_pattern_id": "string",
        "transaction_id": "string",
        "pattern_transaction_sequence": "int64",
    }
)

print("aml_pattern_transactions.csv loaded successfully.")


# ----------------------------------------------------------
# COUNT TRANSACTIONS USING CHUNKED READING
# ----------------------------------------------------------

print("\nCounting transactions.csv rows in chunks...")


TRANSACTION_CHUNK_SIZE = 250_000

transaction_row_count = 0


for chunk_number, transaction_chunk in enumerate(

    pd.read_csv(
        TRANSACTIONS_FILE,
        usecols=["transaction_id"],
        dtype={
            "transaction_id": "string"
        },
        chunksize=TRANSACTION_CHUNK_SIZE,
    ),

    start=1,
):

    transaction_row_count += len(
        transaction_chunk
    )

    print(
        f"Processed Transaction Chunk "
        f"{chunk_number:>2} | "
        f"Rows Counted: "
        f"{transaction_row_count:>9,}"
    )


# ----------------------------------------------------------
# COLLECT ACTUAL ROW COUNTS
# ----------------------------------------------------------

ACTUAL_ROW_COUNTS = {
    "banks": len(banks_df),
    "customers": len(customers_df),
    "accounts": len(accounts_df),
    "transactions": transaction_row_count,
    "aml_patterns": len(aml_patterns_df),
    "aml_pattern_transactions":
        len(aml_pattern_transactions_df),
}


# ----------------------------------------------------------
# VALIDATE ROW COUNTS
# ----------------------------------------------------------

print("\n" + "=" * 70)
print("CLEANED DATASET ROW COUNT RESULTS")
print("=" * 70)


row_count_mismatches = 0


for dataset_name, expected_count in (
    EXPECTED_ROW_COUNTS.items()
):

    actual_count = ACTUAL_ROW_COUNTS[
        dataset_name
    ]

    status = (
        "PASS"
        if actual_count == expected_count
        else "FAIL"
    )


    print(
        f"{dataset_name:<28}"
        f"Expected: {expected_count:>10,} | "
        f"Actual: {actual_count:>10,} | "
        f"{status}"
    )


    if actual_count != expected_count:

        row_count_mismatches += 1


# ----------------------------------------------------------
# FINAL STEP VALIDATION
# ----------------------------------------------------------

if row_count_mismatches > 0:

    raise ValueError(
        f"{row_count_mismatches:,} cleaned datasets "
        "have unexpected row counts."
    )


print(
    "\nAll cleaned dataset row counts "
    "validated successfully."
)

# ==========================================================
# STEP 3: VALIDATE CLEANED DATASET SCHEMAS
# ==========================================================

print("\n" + "=" * 70)
print("CLEANED DATASET SCHEMA VALIDATION")
print("=" * 70)


# ----------------------------------------------------------
# EXPECTED SCHEMAS
# ----------------------------------------------------------

EXPECTED_SCHEMAS = {

    "banks": [
        "bank_id",
        "bank_name",
    ],

    "customers": [
        "customer_id",
        "entity_id",
        "entity_name",
    ],

    "accounts": [
        "account_id",
        "customer_id",
        "bank_id",
        "account_number",
        "entity_id",
    ],

    "transactions": [
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
    ],

    "aml_patterns": [
        "aml_pattern_id",
        "typology",
        "pattern_description",
        "transaction_count",
    ],

    "aml_pattern_transactions": [
        "pattern_transaction_occurrence_id",
        "aml_pattern_id",
        "transaction_id",
        "pattern_transaction_sequence",
    ],
}


# ----------------------------------------------------------
# GET TRANSACTION SCHEMA WITHOUT LOADING FULL DATASET
# ----------------------------------------------------------

transaction_columns = pd.read_csv(
    TRANSACTIONS_FILE,
    nrows=0
).columns.tolist()


# ----------------------------------------------------------
# COLLECT ACTUAL SCHEMAS
# ----------------------------------------------------------

ACTUAL_SCHEMAS = {

    "banks":
        banks_df.columns.tolist(),

    "customers":
        customers_df.columns.tolist(),

    "accounts":
        accounts_df.columns.tolist(),

    "transactions":
        transaction_columns,

    "aml_patterns":
        aml_patterns_df.columns.tolist(),

    "aml_pattern_transactions":
        aml_pattern_transactions_df.columns.tolist(),
}


# ----------------------------------------------------------
# VALIDATE EACH SCHEMA
# ----------------------------------------------------------

schema_mismatches = 0


for dataset_name, expected_columns in (
    EXPECTED_SCHEMAS.items()
):

    actual_columns = ACTUAL_SCHEMAS[
        dataset_name
    ]


    missing_columns = [

        column

        for column in expected_columns

        if column not in actual_columns
    ]


    unexpected_columns = [

        column

        for column in actual_columns

        if column not in expected_columns
    ]


    column_order_matches = (

        actual_columns == expected_columns

    )


    schema_valid = (

        len(missing_columns) == 0

        and len(unexpected_columns) == 0

        and column_order_matches

    )


    status = (

        "PASS"

        if schema_valid

        else "FAIL"

    )


    print(f"\nDataset: {dataset_name}")

    print(
        f"  Expected Column Count : "
        f"{len(expected_columns):,}"
    )

    print(
        f"  Actual Column Count   : "
        f"{len(actual_columns):,}"
    )

    print(
        f"  Missing Columns       : "
        f"{missing_columns}"
    )

    print(
        f"  Unexpected Columns    : "
        f"{unexpected_columns}"
    )

    print(
        f"  Column Order Matches  : "
        f"{column_order_matches}"
    )

    print(
        f"  Schema Status         : "
        f"{status}"
    )


    if not schema_valid:

        schema_mismatches += 1


# ----------------------------------------------------------
# FINAL SCHEMA VALIDATION
# ----------------------------------------------------------

if schema_mismatches > 0:

    raise ValueError(
        f"{schema_mismatches:,} cleaned dataset "
        "schemas failed validation."
    )


print(
    "\nAll cleaned dataset schemas "
    "validated successfully."
)

# ==========================================================
# STEP 4: VALIDATE PRIMARY KEYS
# ==========================================================

print("\n" + "=" * 70)
print("CLEANED DATASET PRIMARY KEY VALIDATION")
print("=" * 70)


# ----------------------------------------------------------
# PRIMARY KEY CONFIGURATION
# ----------------------------------------------------------

PRIMARY_KEYS = {

    "banks": (
        banks_df,
        "bank_id",
    ),

    "customers": (
        customers_df,
        "customer_id",
    ),

    "accounts": (
        accounts_df,
        "account_id",
    ),

    "aml_patterns": (
        aml_patterns_df,
        "aml_pattern_id",
    ),

    "aml_pattern_transactions": (
        aml_pattern_transactions_df,
        "pattern_transaction_occurrence_id",
    ),
}


# ----------------------------------------------------------
# VALIDATE SMALL AND MEDIUM TABLE PRIMARY KEYS
# ----------------------------------------------------------

primary_key_failures = 0


for dataset_name, (
    dataframe,
    primary_key_column,
) in PRIMARY_KEYS.items():

    total_rows = len(dataframe)

    null_primary_keys = (
        dataframe[
            primary_key_column
        ]
        .isna()
        .sum()
    )

    unique_primary_keys = (
        dataframe[
            primary_key_column
        ]
        .nunique(dropna=True)
    )

    duplicate_primary_key_rows = (
        dataframe[
            primary_key_column
        ]
        .duplicated(keep=False)
        .sum()
    )


    primary_key_valid = (

        null_primary_keys == 0

        and unique_primary_keys == total_rows

        and duplicate_primary_key_rows == 0

    )


    status = (

        "PASS"

        if primary_key_valid

        else "FAIL"

    )


    print(f"\nDataset: {dataset_name}")

    print(
        f"  Primary Key           : "
        f"{primary_key_column}"
    )

    print(
        f"  Total Rows            : "
        f"{total_rows:,}"
    )

    print(
        f"  Null Primary Keys     : "
        f"{null_primary_keys:,}"
    )

    print(
        f"  Unique Primary Keys   : "
        f"{unique_primary_keys:,}"
    )

    print(
        f"  Duplicate PK Rows     : "
        f"{duplicate_primary_key_rows:,}"
    )

    print(
        f"  Primary Key Status    : "
        f"{status}"
    )


    if not primary_key_valid:

        primary_key_failures += 1


# ----------------------------------------------------------
# VALIDATE TRANSACTION PRIMARY KEY IN CHUNKS
# ----------------------------------------------------------

print("\n" + "-" * 70)
print("VALIDATING TRANSACTION PRIMARY KEY")
print("-" * 70)


transaction_id_values = set()

transaction_pk_total_rows = 0

transaction_pk_null_count = 0

transaction_pk_duplicate_rows = 0


for chunk_number, transaction_chunk in enumerate(

    pd.read_csv(
        TRANSACTIONS_FILE,
        usecols=["transaction_id"],
        dtype={
            "transaction_id": "string"
        },
        chunksize=TRANSACTION_CHUNK_SIZE,
    ),

    start=1,
):

    transaction_ids = transaction_chunk[
        "transaction_id"
    ]


    transaction_pk_total_rows += len(
        transaction_ids
    )


    chunk_null_count = (
        transaction_ids
        .isna()
        .sum()
    )


    transaction_pk_null_count += (
        chunk_null_count
    )


    non_null_transaction_ids = (

        transaction_ids

        .dropna()

    )


    # Detect duplicates occurring inside this chunk.

    duplicate_inside_chunk_count = (

        non_null_transaction_ids

        .duplicated()

        .sum()

    )


    # Keep only one copy of each ID from this chunk
    # before comparing with IDs from earlier chunks.

    unique_chunk_ids = set(

        non_null_transaction_ids.unique()

    )


    # Detect IDs already seen in previous chunks.

    duplicate_across_chunks_count = len(

        transaction_id_values.intersection(
            unique_chunk_ids
        )

    )


    transaction_pk_duplicate_rows += (

        duplicate_inside_chunk_count

        +

        duplicate_across_chunks_count

    )


    transaction_id_values.update(
        unique_chunk_ids
    )


    print(
        f"Processed Transaction PK Chunk "
        f"{chunk_number:>2} | "
        f"Rows Validated: "
        f"{transaction_pk_total_rows:>9,}"
    )


transaction_pk_unique_count = len(
    transaction_id_values
)


transaction_pk_valid = (

    transaction_pk_null_count == 0

    and transaction_pk_unique_count
        == transaction_pk_total_rows

    and transaction_pk_duplicate_rows == 0

)


transaction_pk_status = (

    "PASS"

    if transaction_pk_valid

    else "FAIL"

)


print("\nDataset: transactions")

print(
    "  Primary Key           : "
    "transaction_id"
)

print(
    f"  Total Rows            : "
    f"{transaction_pk_total_rows:,}"
)

print(
    f"  Null Primary Keys     : "
    f"{transaction_pk_null_count:,}"
)

print(
    f"  Unique Primary Keys   : "
    f"{transaction_pk_unique_count:,}"
)

print(
    f"  Duplicate PK Rows     : "
    f"{transaction_pk_duplicate_rows:,}"
)

print(
    f"  Primary Key Status    : "
    f"{transaction_pk_status}"
)


if not transaction_pk_valid:

    primary_key_failures += 1


# ----------------------------------------------------------
# FINAL PRIMARY KEY VALIDATION
# ----------------------------------------------------------

if primary_key_failures > 0:

    raise ValueError(
        f"{primary_key_failures:,} cleaned datasets "
        "failed primary key validation."
    )


print(
    "\nAll cleaned dataset primary keys "
    "validated successfully."
)

# ==========================================================
# STEP 5: VALIDATE FOREIGN KEYS AND REFERENTIAL INTEGRITY
# ==========================================================

print("\n" + "=" * 70)
print("CLEANED DATASET FOREIGN KEY VALIDATION")
print("=" * 70)


# ----------------------------------------------------------
# PREPARE REFERENCE KEY SETS
# ----------------------------------------------------------

customer_id_set = set(
    customers_df["customer_id"]
)

account_id_set = set(
    accounts_df["account_id"]
)

bank_id_set = set(
    banks_df["bank_id"]
)

aml_pattern_id_set = set(
    aml_patterns_df["aml_pattern_id"]
)


foreign_key_failures = 0


# ----------------------------------------------------------
# VALIDATE ACCOUNTS -> CUSTOMERS
# ----------------------------------------------------------

invalid_account_customer_rows = (

    ~accounts_df[
        "customer_id"
    ].isin(
        customer_id_set
    )

).sum()


# ----------------------------------------------------------
# VALIDATE ACCOUNTS -> BANKS
# ----------------------------------------------------------

invalid_account_bank_rows = (

    ~accounts_df[
        "bank_id"
    ].isin(
        bank_id_set
    )

).sum()


print("\nDataset: accounts")

print(
    "  customer_id -> customers.customer_id"
    f" : Invalid Rows = "
    f"{invalid_account_customer_rows:,}"
)

print(
    "  bank_id -> banks.bank_id"
    f"               : Invalid Rows = "
    f"{invalid_account_bank_rows:,}"
)


accounts_fk_valid = (

    invalid_account_customer_rows == 0

    and invalid_account_bank_rows == 0

)


print(
    f"  Foreign Key Status"
    f"                         : "
    f"{'PASS' if accounts_fk_valid else 'FAIL'}"
)


if not accounts_fk_valid:

    foreign_key_failures += 1


# ----------------------------------------------------------
# VALIDATE AML PATTERN TRANSACTION RELATIONSHIPS
# ----------------------------------------------------------

invalid_bridge_pattern_rows = (

    ~aml_pattern_transactions_df[
        "aml_pattern_id"
    ].isin(
        aml_pattern_id_set
    )

).sum()


print("\nDataset: aml_pattern_transactions")

print(
    "  aml_pattern_id -> aml_patterns.aml_pattern_id"
    f" : Invalid Rows = "
    f"{invalid_bridge_pattern_rows:,}"
)


# ----------------------------------------------------------
# VALIDATE TRANSACTION FOREIGN KEYS IN CHUNKS
# ----------------------------------------------------------

print("\n" + "-" * 70)
print("VALIDATING TRANSACTION FOREIGN KEYS")
print("-" * 70)


transaction_fk_total_rows = 0

invalid_sender_account_rows = 0
invalid_receiver_account_rows = 0

invalid_from_bank_rows = 0
invalid_to_bank_rows = 0


for chunk_number, transaction_chunk in enumerate(

    pd.read_csv(

        TRANSACTIONS_FILE,

        usecols=[
            "sender_account_id",
            "receiver_account_id",
            "from_bank_id",
            "to_bank_id",
        ],

        dtype={
            "sender_account_id": "string",
            "receiver_account_id": "string",
            "from_bank_id": "int64",
            "to_bank_id": "int64",
        },

        chunksize=TRANSACTION_CHUNK_SIZE,

    ),

    start=1,

):

    transaction_fk_total_rows += len(
        transaction_chunk
    )


    invalid_sender_account_rows += (

        ~transaction_chunk[
            "sender_account_id"
        ].isin(
            account_id_set
        )

    ).sum()


    invalid_receiver_account_rows += (

        ~transaction_chunk[
            "receiver_account_id"
        ].isin(
            account_id_set
        )

    ).sum()


    invalid_from_bank_rows += (

        ~transaction_chunk[
            "from_bank_id"
        ].isin(
            bank_id_set
        )

    ).sum()


    invalid_to_bank_rows += (

        ~transaction_chunk[
            "to_bank_id"
        ].isin(
            bank_id_set
        )

    ).sum()


    print(
        f"Processed Transaction FK Chunk "
        f"{chunk_number:>2} | "
        f"Rows Validated: "
        f"{transaction_fk_total_rows:>9,}"
    )


transaction_fk_valid = (

    invalid_sender_account_rows == 0

    and invalid_receiver_account_rows == 0

    and invalid_from_bank_rows == 0

    and invalid_to_bank_rows == 0

)


print("\nDataset: transactions")

print(
    "  sender_account_id -> accounts.account_id"
    f"   : Invalid Rows = "
    f"{invalid_sender_account_rows:,}"
)

print(
    "  receiver_account_id -> accounts.account_id"
    f" : Invalid Rows = "
    f"{invalid_receiver_account_rows:,}"
)

print(
    "  from_bank_id -> banks.bank_id"
    f"               : Invalid Rows = "
    f"{invalid_from_bank_rows:,}"
)

print(
    "  to_bank_id -> banks.bank_id"
    f"                 : Invalid Rows = "
    f"{invalid_to_bank_rows:,}"
)

print(
    f"  Foreign Key Status"
    f"                         : "
    f"{'PASS' if transaction_fk_valid else 'FAIL'}"
)


if not transaction_fk_valid:

    foreign_key_failures += 1


# ----------------------------------------------------------
# VALIDATE AML BRIDGE TRANSACTION IDS
#
# transaction_id_values was created during Step 4 while
# validating the transaction primary key.
# ----------------------------------------------------------

invalid_bridge_transaction_rows = (

    ~aml_pattern_transactions_df[
        "transaction_id"
    ].isin(
        transaction_id_values
    )

).sum()


bridge_fk_valid = (

    invalid_bridge_pattern_rows == 0

    and invalid_bridge_transaction_rows == 0

)


print(
    "\n  transaction_id -> transactions.transaction_id"
    f"     : Invalid Rows = "
    f"{invalid_bridge_transaction_rows:,}"
)

print(
    f"  Foreign Key Status"
    f"                         : "
    f"{'PASS' if bridge_fk_valid else 'FAIL'}"
)


if not bridge_fk_valid:

    foreign_key_failures += 1


# ----------------------------------------------------------
# FINAL FOREIGN KEY VALIDATION
# ----------------------------------------------------------

if foreign_key_failures > 0:

    raise ValueError(
        f"{foreign_key_failures:,} cleaned datasets "
        "failed foreign key validation."
    )


print(
    "\nAll cleaned dataset foreign keys and "
    "referential relationships validated successfully."
)

# ==========================================================
# STEP 6: NULL AND TRANSACTION BUSINESS-RULE VALIDATION
# ==========================================================

print("\n" + "=" * 70)
print("NULL AND TRANSACTION BUSINESS-RULE VALIDATION")
print("=" * 70)


# ----------------------------------------------------------
# VALIDATE NULLS IN SMALL AND MEDIUM TABLES
# ----------------------------------------------------------

NON_TRANSACTION_TABLES = {
    "banks": banks_df,
    "customers": customers_df,
    "accounts": accounts_df,
    "aml_patterns": aml_patterns_df,
    "aml_pattern_transactions": aml_pattern_transactions_df,
}


null_validation_failures = 0


for dataset_name, dataframe in NON_TRANSACTION_TABLES.items():

    null_counts = dataframe.isna().sum()

    total_null_values = int(
        null_counts.sum()
    )

    columns_with_nulls = (
        null_counts[
            null_counts > 0
        ]
        .to_dict()
    )

    status = (
        "PASS"
        if total_null_values == 0
        else "FAIL"
    )


    print(f"\nDataset: {dataset_name}")

    print(
        f"  Total Missing Values : "
        f"{total_null_values:,}"
    )

    print(
        f"  Columns With Nulls   : "
        f"{columns_with_nulls}"
    )

    print(
        f"  Null Validation      : "
        f"{status}"
    )


    if total_null_values > 0:

        null_validation_failures += 1


# ----------------------------------------------------------
# CONFIGURE VALID TRANSACTION DOMAIN VALUES
# ----------------------------------------------------------

VALID_LAUNDERING_LABELS = {
    0,
    1,
}


VALID_PAYMENT_FORMATS = {
    "ACH",
    "Bitcoin",
    "Cash",
    "Cheque",
    "Credit Card",
    "Reinvestment",
    "Wire",
}


VALID_CURRENCIES = {
    "Australian Dollar",
    "Bitcoin",
    "Brazil Real",
    "Canadian Dollar",
    "Euro",
    "Mexican Peso",
    "Ruble",
    "Rupee",
    "Saudi Riyal",
    "Shekel",
    "Swiss Franc",
    "UK Pound",
    "US Dollar",
    "Yen",
    "Yuan",
}


# ----------------------------------------------------------
# VALIDATE TRANSACTIONS IN CHUNKS
# ----------------------------------------------------------

print("\n" + "-" * 70)
print("VALIDATING TRANSACTION NULLS AND BUSINESS RULES")
print("-" * 70)


transaction_business_total_rows = 0
transaction_total_null_values = 0

invalid_timestamp_rows = 0

non_positive_amount_received_rows = 0
non_positive_amount_paid_rows = 0

invalid_laundering_label_rows = 0

invalid_payment_format_rows = 0

invalid_receiving_currency_rows = 0
invalid_payment_currency_rows = 0


for chunk_number, transaction_chunk in enumerate(

    pd.read_csv(

        TRANSACTIONS_FILE,

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

        chunksize=TRANSACTION_CHUNK_SIZE,

    ),

    start=1,

):

    transaction_business_total_rows += len(
        transaction_chunk
    )


    # ------------------------------------------------------
    # COMPLETE NULL VALIDATION
    # ------------------------------------------------------

    transaction_total_null_values += int(

        transaction_chunk

        .isna()

        .sum()

        .sum()

    )


    # ------------------------------------------------------
    # TIMESTAMP VALIDATION
    # ------------------------------------------------------

    parsed_timestamps = pd.to_datetime(

        transaction_chunk["timestamp"],

        errors="coerce",

    )


    invalid_timestamp_rows += int(

        parsed_timestamps

        .isna()

        .sum()

    )


    # ------------------------------------------------------
    # AMOUNT VALIDATION
    # ------------------------------------------------------

    non_positive_amount_received_rows += int(

        (
            transaction_chunk[
                "amount_received"
            ]
            <= 0
        ).sum()

    )


    non_positive_amount_paid_rows += int(

        (
            transaction_chunk[
                "amount_paid"
            ]
            <= 0
        ).sum()

    )


    # ------------------------------------------------------
    # LAUNDERING LABEL VALIDATION
    # ------------------------------------------------------

    invalid_laundering_label_rows += int(

        (
            ~transaction_chunk[
                "is_laundering"
            ].isin(
                VALID_LAUNDERING_LABELS
            )
        ).sum()

    )


    # ------------------------------------------------------
    # PAYMENT FORMAT VALIDATION
    # ------------------------------------------------------

    invalid_payment_format_rows += int(

        (
            ~transaction_chunk[
                "payment_format"
            ].isin(
                VALID_PAYMENT_FORMATS
            )
        ).sum()

    )


    # ------------------------------------------------------
    # CURRENCY VALIDATION
    # ------------------------------------------------------

    invalid_receiving_currency_rows += int(

        (
            ~transaction_chunk[
                "receiving_currency"
            ].isin(
                VALID_CURRENCIES
            )
        ).sum()

    )


    invalid_payment_currency_rows += int(

        (
            ~transaction_chunk[
                "payment_currency"
            ].isin(
                VALID_CURRENCIES
            )
        ).sum()

    )


    print(
        f"Processed Transaction Rule Chunk "
        f"{chunk_number:>2} | "
        f"Rows Validated: "
        f"{transaction_business_total_rows:>9,}"
    )


# ----------------------------------------------------------
# TRANSACTION BUSINESS-RULE RESULTS
# ----------------------------------------------------------

transaction_business_rules_valid = (

    transaction_business_total_rows
        == EXPECTED_ROW_COUNTS["transactions"]

    and transaction_total_null_values == 0

    and invalid_timestamp_rows == 0

    and non_positive_amount_received_rows == 0

    and non_positive_amount_paid_rows == 0

    and invalid_laundering_label_rows == 0

    and invalid_payment_format_rows == 0

    and invalid_receiving_currency_rows == 0

    and invalid_payment_currency_rows == 0

)


print("\nDataset: transactions")

print(
    f"  Total Rows Validated              : "
    f"{transaction_business_total_rows:,}"
)

print(
    f"  Total Missing Values              : "
    f"{transaction_total_null_values:,}"
)

print(
    f"  Invalid Timestamps                : "
    f"{invalid_timestamp_rows:,}"
)

print(
    f"  Non-Positive Amount Received Rows : "
    f"{non_positive_amount_received_rows:,}"
)

print(
    f"  Non-Positive Amount Paid Rows     : "
    f"{non_positive_amount_paid_rows:,}"
)

print(
    f"  Invalid Laundering Labels         : "
    f"{invalid_laundering_label_rows:,}"
)

print(
    f"  Invalid Payment Formats           : "
    f"{invalid_payment_format_rows:,}"
)

print(
    f"  Invalid Receiving Currencies      : "
    f"{invalid_receiving_currency_rows:,}"
)

print(
    f"  Invalid Payment Currencies        : "
    f"{invalid_payment_currency_rows:,}"
)

print(
    f"  Transaction Rule Status           : "
    f"{'PASS' if transaction_business_rules_valid else 'FAIL'}"
)


if not transaction_business_rules_valid:

    null_validation_failures += 1


# ----------------------------------------------------------
# FINAL STEP VALIDATION
# ----------------------------------------------------------

if null_validation_failures > 0:

    raise ValueError(
        f"{null_validation_failures:,} cleaned datasets "
        "failed null or business-rule validation."
    )


print(
    "\nAll cleaned dataset null checks and transaction "
    "business rules validated successfully."
)

# ==========================================================
# STEP 7: CROSS-TABLE SEMANTIC CONSISTENCY VALIDATION
# ==========================================================

print("\n" + "=" * 70)
print("CROSS-TABLE SEMANTIC CONSISTENCY VALIDATION")
print("=" * 70)


semantic_validation_failures = 0


# ----------------------------------------------------------
# PREPARE ACCOUNT -> BANK MAPPING
# ----------------------------------------------------------

print("\nPreparing account-to-bank mapping...")


account_bank_mapping = (

    accounts_df

    .set_index("account_id")

    ["bank_id"]

)


print(
    f"Account-to-bank mappings prepared: "
    f"{len(account_bank_mapping):,}"
)


# ----------------------------------------------------------
# PREPARE AML PATTERN TRANSACTION ID SET
# ----------------------------------------------------------

aml_bridge_transaction_id_set = set(

    aml_pattern_transactions_df[
        "transaction_id"
    ]

)


print(
    f"AML bridge transaction IDs prepared: "
    f"{len(aml_bridge_transaction_id_set):,}"
)


# ----------------------------------------------------------
# VALIDATE TRANSACTION ACCOUNT-BANK CONSISTENCY
# AND AML TRANSACTION LABEL CONSISTENCY
# ----------------------------------------------------------

print("\n" + "-" * 70)
print("VALIDATING TRANSACTION SEMANTIC RELATIONSHIPS")
print("-" * 70)


semantic_transaction_rows_validated = 0

sender_bank_mismatch_rows = 0

receiver_bank_mismatch_rows = 0


aml_bridge_transactions_found = 0

aml_bridge_non_laundering_rows = 0


for chunk_number, transaction_chunk in enumerate(

    pd.read_csv(

        TRANSACTIONS_FILE,

        usecols=[
            "transaction_id",
            "sender_account_id",
            "receiver_account_id",
            "from_bank_id",
            "to_bank_id",
            "is_laundering",
        ],

        dtype={
            "transaction_id": "string",
            "sender_account_id": "string",
            "receiver_account_id": "string",
            "from_bank_id": "int64",
            "to_bank_id": "int64",
            "is_laundering": "int64",
        },

        chunksize=TRANSACTION_CHUNK_SIZE,

    ),

    start=1,

):

    semantic_transaction_rows_validated += len(
        transaction_chunk
    )


    # ------------------------------------------------------
    # MAP SENDER ACCOUNT TO EXPECTED BANK
    # ------------------------------------------------------

    expected_sender_bank_ids = (

        transaction_chunk[
            "sender_account_id"
        ]

        .map(
            account_bank_mapping
        )

    )


    # ------------------------------------------------------
    # MAP RECEIVER ACCOUNT TO EXPECTED BANK
    # ------------------------------------------------------

    expected_receiver_bank_ids = (

        transaction_chunk[
            "receiver_account_id"
        ]

        .map(
            account_bank_mapping
        )

    )


    # ------------------------------------------------------
    # VALIDATE SENDER ACCOUNT <-> FROM BANK
    # ------------------------------------------------------

    sender_bank_mismatch_rows += int(

        (

            expected_sender_bank_ids

            !=

            transaction_chunk[
                "from_bank_id"
            ]

        ).sum()

    )


    # ------------------------------------------------------
    # VALIDATE RECEIVER ACCOUNT <-> TO BANK
    # ------------------------------------------------------

    receiver_bank_mismatch_rows += int(

        (

            expected_receiver_bank_ids

            !=

            transaction_chunk[
                "to_bank_id"
            ]

        ).sum()

    )


    # ------------------------------------------------------
    # FIND TRANSACTIONS REFERENCED BY AML BRIDGE
    # ------------------------------------------------------

    aml_bridge_rows = (

        transaction_chunk[

            transaction_chunk[
                "transaction_id"
            ].isin(
                aml_bridge_transaction_id_set
            )

        ]

    )


    aml_bridge_transactions_found += len(
        aml_bridge_rows
    )


    # ------------------------------------------------------
    # VERIFY AML BRIDGE TRANSACTIONS ARE LAUNDERING
    # ------------------------------------------------------

    aml_bridge_non_laundering_rows += int(

        (

            aml_bridge_rows[
                "is_laundering"
            ]

            != 1

        ).sum()

    )


    print(
        f"Processed Semantic Chunk "
        f"{chunk_number:>2} | "
        f"Rows Validated: "
        f"{semantic_transaction_rows_validated:>9,}"
    )


# ----------------------------------------------------------
# VALIDATE TRANSACTION SEMANTIC RESULTS
# ----------------------------------------------------------

transaction_semantic_valid = (

    semantic_transaction_rows_validated
        == EXPECTED_ROW_COUNTS["transactions"]

    and sender_bank_mismatch_rows == 0

    and receiver_bank_mismatch_rows == 0

    and aml_bridge_transactions_found
        == len(aml_pattern_transactions_df)

    and aml_bridge_non_laundering_rows == 0

)


print("\nTransaction Semantic Results:")

print(
    f"  Total Transaction Rows Validated      : "
    f"{semantic_transaction_rows_validated:,}"
)

print(
    f"  Sender Account-Bank Mismatches        : "
    f"{sender_bank_mismatch_rows:,}"
)

print(
    f"  Receiver Account-Bank Mismatches      : "
    f"{receiver_bank_mismatch_rows:,}"
)

print(
    f"  Expected AML Bridge Transactions      : "
    f"{len(aml_pattern_transactions_df):,}"
)

print(
    f"  AML Bridge Transactions Found         : "
    f"{aml_bridge_transactions_found:,}"
)

print(
    f"  AML Bridge Non-Laundering Transactions: "
    f"{aml_bridge_non_laundering_rows:,}"
)

print(
    f"  Transaction Semantic Status           : "
    f"{'PASS' if transaction_semantic_valid else 'FAIL'}"
)


if not transaction_semantic_valid:

    semantic_validation_failures += 1


# ----------------------------------------------------------
# VALIDATE AML PATTERN TRANSACTION COUNTS
# ----------------------------------------------------------

print("\n" + "-" * 70)
print("VALIDATING AML PATTERN TRANSACTION COUNTS")
print("-" * 70)


actual_pattern_transaction_counts = (

    aml_pattern_transactions_df

    .groupby(
        "aml_pattern_id"
    )

    .size()

    .rename(
        "actual_transaction_count"
    )

)


pattern_count_validation_df = (

    aml_patterns_df[

        [
            "aml_pattern_id",
            "transaction_count",
        ]

    ]

    .set_index(
        "aml_pattern_id"
    )

    .join(

        actual_pattern_transaction_counts,

        how="left",

    )

)


pattern_count_validation_df[

    "actual_transaction_count"

] = (

    pattern_count_validation_df[

        "actual_transaction_count"

    ]

    .fillna(0)

    .astype("int64")

)


pattern_transaction_count_mismatches = int(

    (

        pattern_count_validation_df[
            "transaction_count"
        ]

        !=

        pattern_count_validation_df[
            "actual_transaction_count"
        ]

    ).sum()

)


patterns_without_transactions = int(

    (

        pattern_count_validation_df[
            "actual_transaction_count"
        ]

        == 0

    ).sum()

)


expected_pattern_transaction_total = int(

    aml_patterns_df[
        "transaction_count"
    ].sum()

)


actual_pattern_transaction_total = int(

    len(
        aml_pattern_transactions_df
    )

)


pattern_semantic_valid = (

    pattern_transaction_count_mismatches == 0

    and patterns_without_transactions == 0

    and expected_pattern_transaction_total
        == actual_pattern_transaction_total

)


print("\nAML Pattern Semantic Results:")

print(
    f"  AML Patterns Validated                : "
    f"{len(aml_patterns_df):,}"
)

print(
    f"  Pattern Transaction Count Mismatches  : "
    f"{pattern_transaction_count_mismatches:,}"
)

print(
    f"  Patterns Without Transactions         : "
    f"{patterns_without_transactions:,}"
)

print(
    f"  Expected Pattern Transaction Total    : "
    f"{expected_pattern_transaction_total:,}"
)

print(
    f"  Actual Pattern Transaction Total      : "
    f"{actual_pattern_transaction_total:,}"
)

print(
    f"  AML Pattern Semantic Status           : "
    f"{'PASS' if pattern_semantic_valid else 'FAIL'}"
)


if not pattern_semantic_valid:

    semantic_validation_failures += 1


# ----------------------------------------------------------
# FINAL STEP VALIDATION
# ----------------------------------------------------------

if semantic_validation_failures > 0:

    raise ValueError(
        f"{semantic_validation_failures:,} semantic "
        "consistency validation groups failed."
    )


print(
    "\nAll cross-table semantic consistency "
    "validations passed successfully."
)

# ==========================================================
# STEP 8: FINAL VALIDATION SUMMARY AND REPORT GENERATION
# ==========================================================

print("\n" + "=" * 70)
print("FINAL CLEANED DATA VALIDATION SUMMARY")
print("=" * 70)


# ----------------------------------------------------------
# PREPARE FINAL VALIDATION STATUS
# ----------------------------------------------------------

final_validation_status = "PASS"


# ----------------------------------------------------------
# BUILD VALIDATION REPORT
# ----------------------------------------------------------

validation_report_lines = [

    "=" * 70,

    "BANKING FRAUD & FINANCIAL RISK INTELLIGENCE PLATFORM",

    "CLEANED DATA VALIDATION REPORT",

    "=" * 70,

    "",

    "FINAL VALIDATION STATUS: PASS",

    "",

    "-" * 70,

    "CLEANED DATASET ROW COUNTS",

    "-" * 70,

    "",

    f"Banks                    : "
    f"{EXPECTED_ROW_COUNTS['banks']:,}",

    f"Customers                : "
    f"{EXPECTED_ROW_COUNTS['customers']:,}",

    f"Accounts                 : "
    f"{EXPECTED_ROW_COUNTS['accounts']:,}",

    f"Transactions             : "
    f"{EXPECTED_ROW_COUNTS['transactions']:,}",

    f"AML Patterns             : "
    f"{EXPECTED_ROW_COUNTS['aml_patterns']:,}",

    f"AML Pattern Transactions : "
    f"{EXPECTED_ROW_COUNTS['aml_pattern_transactions']:,}",

    "",

    "-" * 70,

    "VALIDATION CHECK SUMMARY",

    "-" * 70,

    "",

    "1. Cleaned Dataset File Verification        : PASS",

    "2. Cleaned Dataset Row Count Validation     : PASS",

    "3. Cleaned Dataset Schema Validation        : PASS",

    "4. Cleaned Dataset Primary Key Validation   : PASS",

    "5. Foreign Key / Referential Validation     : PASS",

    "6. Null and Transaction Business Rules      : PASS",

    "7. Cross-Table Semantic Consistency          : PASS",

    "",

    "-" * 70,

    "TRANSACTION VALIDATION RESULTS",

    "-" * 70,

    "",

    f"Transactions Validated                 : "
    f"{semantic_transaction_rows_validated:,}",

    f"Sender Account-Bank Mismatches         : "
    f"{sender_bank_mismatch_rows:,}",

    f"Receiver Account-Bank Mismatches       : "
    f"{receiver_bank_mismatch_rows:,}",

    f"AML Bridge Transactions Expected       : "
    f"{len(aml_pattern_transactions_df):,}",

    f"AML Bridge Transactions Found          : "
    f"{aml_bridge_transactions_found:,}",

    f"AML Bridge Non-Laundering Transactions : "
    f"{aml_bridge_non_laundering_rows:,}",

    "",

    "-" * 70,

    "AML PATTERN VALIDATION RESULTS",

    "-" * 70,

    "",

    f"AML Patterns Validated                 : "
    f"{len(aml_patterns_df):,}",

    f"Pattern Transaction Count Mismatches   : "
    f"{pattern_transaction_count_mismatches:,}",

    f"Patterns Without Transactions          : "
    f"{patterns_without_transactions:,}",

    f"Expected Pattern Transaction Total     : "
    f"{expected_pattern_transaction_total:,}",

    f"Actual Pattern Transaction Total       : "
    f"{actual_pattern_transaction_total:,}",

    "",

    "-" * 70,

    "DATA QUALITY OBSERVATIONS",

    "-" * 70,

    "",

    "Raw exact duplicate transaction rows removed : 9",

    "Missing AML pattern descriptions standardized: 136",

    "Missing AML pattern description replacement : Not Provided",

    "Orphan sender transaction rows                : 0",

    "Orphan receiver transaction rows              : 0",

    "Invalid foreign key relationships             : 0",

    "Transaction account-bank semantic mismatches  : 0",

    "AML pattern transaction-count mismatches      : 0",

    "",

    "-" * 70,

    "FINAL CONCLUSION",

    "-" * 70,

    "",

    (
        "All cleaned datasets passed structural, schema, "
        "primary-key, foreign-key, null, business-rule, "
        "and cross-table semantic consistency validation."
    ),

    "",

    (
        "The cleaned data layer is validated and approved "
        "for downstream feature engineering, analytical "
        "modeling, SQL analysis, and BI visualization."
    ),

    "",

    "=" * 70,

]


validation_report_text = "\n".join(
    validation_report_lines
)


# ----------------------------------------------------------
# SAVE VALIDATION REPORT
# ----------------------------------------------------------

VALIDATION_REPORT_FILE = (

    REPORTS_DIR

    / "cleaned_data_validation_report.txt"

)


VALIDATION_REPORT_FILE.write_text(

    validation_report_text,

    encoding="utf-8",

)


# ----------------------------------------------------------
# VERIFY REPORT CREATION
# ----------------------------------------------------------

if not VALIDATION_REPORT_FILE.exists():

    raise FileNotFoundError(
        "Cleaned data validation report was not created."
    )


if VALIDATION_REPORT_FILE.stat().st_size == 0:

    raise ValueError(
        "Cleaned data validation report is empty."
    )


# ----------------------------------------------------------
# PRINT FINAL SUMMARY
# ----------------------------------------------------------

print("\nValidation Check Summary:")

print(
    "  Cleaned Dataset File Verification       : PASS"
)

print(
    "  Cleaned Dataset Row Count Validation    : PASS"
)

print(
    "  Cleaned Dataset Schema Validation       : PASS"
)

print(
    "  Cleaned Dataset Primary Key Validation  : PASS"
)

print(
    "  Foreign Key / Referential Validation    : PASS"
)

print(
    "  Null and Transaction Business Rules     : PASS"
)

print(
    "  Cross-Table Semantic Consistency         : PASS"
)


print("\nCleaned Data Validation Report Created Successfully.")

print(
    f"Report Location: "
    f"{VALIDATION_REPORT_FILE}"
)


print("\n" + "=" * 70)

print(
    "CLEANED DATA LAYER VALIDATION COMPLETED SUCCESSFULLY."
)

print("=" * 70)

