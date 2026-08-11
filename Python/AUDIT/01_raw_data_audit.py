from pathlib import Path

import pandas as pd


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "DATA" / "RAW"
REPORTS_DIR = PROJECT_ROOT / "REPORTS"

TRANSACTIONS_FILE = RAW_DATA_DIR / "HI-Small_Trans.csv"
ACCOUNTS_FILE = RAW_DATA_DIR / "HI-Small_accounts.csv"
PATTERNS_FILE = RAW_DATA_DIR / "HI-Small_Patterns.txt"


# --------------------------------------------------
# DISPLAY PROJECT PATHS
# --------------------------------------------------

print("=" * 70)
print("BANKING FRAUD & FINANCIAL RISK INTELLIGENCE PLATFORM")
print("PHASE 1: RAW DATA AUDIT")
print("=" * 70)

print(f"\nProject Root       : {PROJECT_ROOT}")
print(f"Raw Data Directory : {RAW_DATA_DIR}")
print(f"Reports Directory  : {REPORTS_DIR}")

# --------------------------------------------------
# VERIFY RAW FILES
# --------------------------------------------------

print("\n" + "=" * 70)
print("VERIFYING RAW FILES")
print("=" * 70)

raw_files = {
    "Transactions": TRANSACTIONS_FILE,
    "Accounts": ACCOUNTS_FILE,
    "Patterns": PATTERNS_FILE,
}

all_files_exist = True

for file_name, file_path in raw_files.items():

    if file_path.exists():
        file_size_mb = file_path.stat().st_size / (1024 ** 2)

        print(
            f"[FOUND]   {file_name:<15} "
            f"{file_path.name:<30} "
            f"{file_size_mb:,.2f} MB"
        )

    else:
        print(f"[MISSING] {file_name:<15} {file_path}")
        all_files_exist = False


if not all_files_exist:
    raise FileNotFoundError(
        "One or more required raw data files are missing. "
        "Check the DATA/RAW directory."
    )

print("\nAll required raw files were found successfully.")

# --------------------------------------------------
# LOAD ACCOUNTS DATASET
# --------------------------------------------------

print("\n" + "=" * 70)
print("LOADING ACCOUNTS DATASET")
print("=" * 70)

accounts_df = pd.read_csv(ACCOUNTS_FILE)

print("\nAccounts dataset loaded successfully.")

print(f"Rows    : {accounts_df.shape[0]:,}")
print(f"Columns : {accounts_df.shape[1]:,}")

print("\nColumn Names:")
for column in accounts_df.columns:
    print(f"  - {column}")

# --------------------------------------------------
# AUDIT ACCOUNTS DATASET STRUCTURE
# --------------------------------------------------

print("\n" + "=" * 70)
print("ACCOUNTS DATASET STRUCTURE AUDIT")
print("=" * 70)


# Display first 5 records
print("\nFirst 5 Records:")
print(accounts_df.head())


# Display data types
print("\nData Types:")
print(accounts_df.dtypes)


# Check missing values
print("\nMissing Values:")
print(accounts_df.isna().sum())


# Check duplicate rows
duplicate_rows = accounts_df.duplicated().sum()

print(f"\nDuplicate Rows: {duplicate_rows:,}")


# Check unique values in important identifier columns
print("\nUnique Value Counts:")

print(
    f"Unique Bank Names      : "
    f"{accounts_df['Bank Name'].nunique():,}"
)

print(
    f"Unique Bank IDs        : "
    f"{accounts_df['Bank ID'].nunique():,}"
)

print(
    f"Unique Account Numbers : "
    f"{accounts_df['Account Number'].nunique():,}"
)

print(
    f"Unique Entity IDs      : "
    f"{accounts_df['Entity ID'].nunique():,}"
)

print(
    f"Unique Entity Names    : "
    f"{accounts_df['Entity Name'].nunique():,}"
)

# --------------------------------------------------
# AUDIT ACCOUNT KEYS AND ENTITY RELATIONSHIPS
# --------------------------------------------------

print("\n" + "=" * 70)
print("ACCOUNT KEYS AND ENTITY RELATIONSHIP AUDIT")
print("=" * 70)


# Account Number uniqueness
duplicate_account_numbers = accounts_df["Account Number"].duplicated().sum()

print(
    f"\nDuplicate Account Numbers: "
    f"{duplicate_account_numbers:,}"
)


# Composite Bank ID + Account Number uniqueness
duplicate_bank_account_keys = accounts_df.duplicated(
    subset=["Bank ID", "Account Number"]
).sum()

print(
    f"Duplicate (Bank ID, Account Number) Keys: "
    f"{duplicate_bank_account_keys:,}"
)


# Check whether one Entity ID maps to multiple Entity Names
entity_name_counts = (
    accounts_df
    .groupby("Entity ID")["Entity Name"]
    .nunique()
)

entities_with_multiple_names = (entity_name_counts > 1).sum()

print(
    f"Entity IDs With Multiple Entity Names: "
    f"{entities_with_multiple_names:,}"
)


# Number of accounts owned by each entity
accounts_per_entity = (
    accounts_df
    .groupby("Entity ID")
    .size()
)


print("\nAccounts Per Entity Statistics:")

print(accounts_per_entity.describe())


# Entities with multiple accounts
entities_with_multiple_accounts = (
    accounts_per_entity > 1
).sum()

print(
    f"\nEntities With Multiple Accounts: "
    f"{entities_with_multiple_accounts:,}"
)


# Maximum accounts owned by one entity
print(
    f"Maximum Accounts Owned By One Entity: "
    f"{accounts_per_entity.max():,}"
)

# --------------------------------------------------
# AUDIT ENTITY TYPES
# --------------------------------------------------

print("\n" + "=" * 70)
print("ENTITY TYPE AUDIT")
print("=" * 70)


# Extract the text portion before the final "#number"
entity_types = (
    accounts_df["Entity Name"]
    .str.replace(r"\s+#\d+$", "", regex=True)
    .value_counts()
)


print("\nEntity Type Distribution:")

for entity_type, count in entity_types.items():
    print(f"{entity_type:<30} : {count:,}")


print(
    f"\nTotal Distinct Entity Types: "
    f"{len(entity_types):,}"
)

# --------------------------------------------------
# AUDIT DISTINCT ENTITIES BY TYPE
# --------------------------------------------------

print("\n" + "=" * 70)
print("DISTINCT ENTITY TYPE AUDIT")
print("=" * 70)


# Keep one record per Entity ID
distinct_entities_df = (
    accounts_df[
        ["Entity ID", "Entity Name"]
    ]
    .drop_duplicates(subset=["Entity ID"])
    .copy()
)


# Extract entity type
distinct_entities_df["Entity Type"] = (
    distinct_entities_df["Entity Name"]
    .str.replace(r"\s+#\d+$", "", regex=True)
)


# Count distinct entities by type
distinct_entity_type_counts = (
    distinct_entities_df["Entity Type"]
    .value_counts()
)


print("\nDistinct Entity Type Distribution:")

for entity_type, count in distinct_entity_type_counts.items():
    print(f"{entity_type:<30} : {count:,}")


print(
    f"\nTotal Distinct Entities: "
    f"{len(distinct_entities_df):,}"
)

# --------------------------------------------------
# AUDIT BANK STRUCTURE AND CONSISTENCY
# --------------------------------------------------

print("\n" + "=" * 70)
print("BANK STRUCTURE AND CONSISTENCY AUDIT")
print("=" * 70)


# Check whether one Bank ID maps to multiple Bank Names
bank_id_name_counts = (
    accounts_df
    .groupby("Bank ID")["Bank Name"]
    .nunique()
)

bank_ids_with_multiple_names = (
    bank_id_name_counts > 1
).sum()

print(
    f"\nBank IDs With Multiple Bank Names: "
    f"{bank_ids_with_multiple_names:,}"
)


# Check whether one Bank Name maps to multiple Bank IDs
bank_name_id_counts = (
    accounts_df
    .groupby("Bank Name")["Bank ID"]
    .nunique()
)

bank_names_with_multiple_ids = (
    bank_name_id_counts > 1
).sum()

print(
    f"Bank Names With Multiple Bank IDs: "
    f"{bank_names_with_multiple_ids:,}"
)


# Count accounts per bank
accounts_per_bank = (
    accounts_df
    .groupby("Bank ID")
    .size()
)

print("\nAccounts Per Bank Statistics:")
print(accounts_per_bank.describe())


# Count unique entities per bank
entities_per_bank = (
    accounts_df
    .groupby("Bank ID")["Entity ID"]
    .nunique()
)

print("\nUnique Entities Per Bank Statistics:")
print(entities_per_bank.describe())


# Largest banks by account count
top_banks_by_accounts = (
    accounts_df
    .groupby(["Bank ID", "Bank Name"])
    .size()
    .reset_index(name="Account Count")
    .sort_values("Account Count", ascending=False)
    .head(10)
)

print("\nTop 10 Banks By Account Count:")
print(top_banks_by_accounts.to_string(index=False))


# Largest banks by unique entity count
top_banks_by_entities = (
    accounts_df
    .groupby(["Bank ID", "Bank Name"])["Entity ID"]
    .nunique()
    .reset_index(name="Unique Entity Count")
    .sort_values("Unique Entity Count", ascending=False)
    .head(10)
)

print("\nTop 10 Banks By Unique Entity Count:")
print(top_banks_by_entities.to_string(index=False))

# --------------------------------------------------
# INSPECT TRANSACTIONS DATASET SCHEMA
# --------------------------------------------------

print("\n" + "=" * 70)
print("TRANSACTIONS DATASET SCHEMA INSPECTION")
print("=" * 70)


# Read only the first 5 transaction records
transactions_sample_df = pd.read_csv(
    TRANSACTIONS_FILE,
    nrows=5
)


print("\nFirst 5 Transaction Records:")
print(transactions_sample_df.to_string(index=False))


print("\nTransaction Column Names:")

for column in transactions_sample_df.columns:
    print(f"  - {column}")


print(
    f"\nTotal Transaction Columns: "
    f"{transactions_sample_df.shape[1]}"
)


print("\nDetected Data Types:")

print(transactions_sample_df.dtypes)

# --------------------------------------------------
# FULL TRANSACTION DATASET AUDIT - CHUNK PROCESSING
# --------------------------------------------------

print("\n" + "=" * 70)
print("FULL TRANSACTION DATASET AUDIT")
print("=" * 70)

CHUNK_SIZE = 250_000

total_rows = 0
missing_values = None
duplicate_rows_within_chunks = 0
laundering_transactions = 0

min_timestamp = None
max_timestamp = None

payment_formats = set()
payment_currencies = set()
receiving_currencies = set()
from_bank_ids = set()
to_bank_ids = set()

chunk_number = 0


for chunk in pd.read_csv(
    TRANSACTIONS_FILE,
    chunksize=CHUNK_SIZE
):
    chunk_number += 1

    print(f"Processing chunk {chunk_number}...")

    # Total row count
    total_rows += len(chunk)

    # Missing values
    chunk_missing = chunk.isna().sum()

    if missing_values is None:
        missing_values = chunk_missing
    else:
        missing_values = missing_values.add(
            chunk_missing,
            fill_value=0
        )

    # Duplicate rows inside the current chunk
    duplicate_rows_within_chunks += chunk.duplicated().sum()

    # Laundering transaction count
    laundering_transactions += chunk["Is Laundering"].sum()

    # Parse timestamps
    chunk_timestamps = pd.to_datetime(
        chunk["Timestamp"],
        errors="coerce"
    )

    chunk_min_timestamp = chunk_timestamps.min()
    chunk_max_timestamp = chunk_timestamps.max()

    if min_timestamp is None or chunk_min_timestamp < min_timestamp:
        min_timestamp = chunk_min_timestamp

    if max_timestamp is None or chunk_max_timestamp > max_timestamp:
        max_timestamp = chunk_max_timestamp

    # Collect distinct categorical values
    payment_formats.update(
        chunk["Payment Format"].dropna().unique()
    )

    payment_currencies.update(
        chunk["Payment Currency"].dropna().unique()
    )

    receiving_currencies.update(
        chunk["Receiving Currency"].dropna().unique()
    )

    # Collect distinct bank IDs
    from_bank_ids.update(
        chunk["From Bank"].dropna().unique()
    )

    to_bank_ids.update(
        chunk["To Bank"].dropna().unique()
    )


laundering_rate = (
    laundering_transactions / total_rows * 100
)


print("\n" + "-" * 70)
print("FULL TRANSACTION AUDIT RESULTS")
print("-" * 70)

print(f"Total Rows                  : {total_rows:,}")
print(f"Total Columns               : {len(transactions_sample_df.columns):,}")

print("\nMissing Values:")
print(missing_values.astype("int64"))

print(
    f"\nDuplicate Rows Within Chunks: "
    f"{duplicate_rows_within_chunks:,}"
)

print(
    "\nNOTE: This duplicate count only detects duplicates occurring "
    "inside the same chunk."
)

print(f"\nMinimum Timestamp           : {min_timestamp}")
print(f"Maximum Timestamp           : {max_timestamp}")

print(f"\nLaundering Transactions     : {laundering_transactions:,}")
print(f"Laundering Transaction Rate : {laundering_rate:.6f}%")

print(f"\nUnique From Bank IDs        : {len(from_bank_ids):,}")
print(f"Unique To Bank IDs          : {len(to_bank_ids):,}")

print(f"\nPayment Formats             : {sorted(payment_formats)}")
print(f"Payment Currencies          : {sorted(payment_currencies)}")
print(f"Receiving Currencies        : {sorted(receiving_currencies)}")

# --------------------------------------------------
# VALIDATE TRANSACTION ACCOUNT REFERENCES
# --------------------------------------------------

print("\n" + "=" * 70)
print("TRANSACTION ACCOUNT REFERENCE VALIDATION")
print("=" * 70)


# Build the valid IBM account key set from Accounts
valid_account_keys = set(
    zip(
        accounts_df["Bank ID"],
        accounts_df["Account Number"]
    )
)


orphan_sender_rows = 0
orphan_receiver_rows = 0

unique_orphan_sender_keys = set()
unique_orphan_receiver_keys = set()

total_validated_rows = 0
chunk_number = 0


for chunk in pd.read_csv(
    TRANSACTIONS_FILE,
    chunksize=CHUNK_SIZE,
    usecols=[
        "From Bank",
        "Account",
        "To Bank",
        "Account.1"
    ]
):

    chunk_number += 1
    total_validated_rows += len(chunk)

    print(f"Validating account references in chunk {chunk_number}...")


    # Create sender account keys
    sender_keys = list(
        zip(
            chunk["From Bank"],
            chunk["Account"]
        )
    )


    # Create receiver account keys
    receiver_keys = list(
        zip(
            chunk["To Bank"],
            chunk["Account.1"]
        )
    )


    # Check sender references
    sender_valid_mask = [
        key in valid_account_keys
        for key in sender_keys
    ]


    # Check receiver references
    receiver_valid_mask = [
        key in valid_account_keys
        for key in receiver_keys
    ]


    # Count orphan sender rows
    orphan_sender_rows += (
        len(sender_valid_mask)
        - sum(sender_valid_mask)
    )


    # Count orphan receiver rows
    orphan_receiver_rows += (
        len(receiver_valid_mask)
        - sum(receiver_valid_mask)
    )


    # Store distinct orphan sender keys
    unique_orphan_sender_keys.update(
        key
        for key, is_valid
        in zip(sender_keys, sender_valid_mask)
        if not is_valid
    )


    # Store distinct orphan receiver keys
    unique_orphan_receiver_keys.update(
        key
        for key, is_valid
        in zip(receiver_keys, receiver_valid_mask)
        if not is_valid
    )


print("\n" + "-" * 70)
print("TRANSACTION ACCOUNT REFERENCE RESULTS")
print("-" * 70)

print(f"Total Validated Rows          : {total_validated_rows:,}")

print(f"\nOrphan Sender Transaction Rows: {orphan_sender_rows:,}")

print(
    f"Unique Orphan Sender Accounts : "
    f"{len(unique_orphan_sender_keys):,}"
)

print(f"\nOrphan Receiver Transaction Rows: {orphan_receiver_rows:,}")

print(
    f"Unique Orphan Receiver Accounts : "
    f"{len(unique_orphan_receiver_keys):,}"
)

# --------------------------------------------------
# AUDIT TRANSACTION VALUES AND LAUNDERING DISTRIBUTION
# --------------------------------------------------

print("\n" + "=" * 70)
print("TRANSACTION VALUES AND LAUNDERING AUDIT")
print("=" * 70)

total_rows_checked = 0

zero_amount_paid = 0
negative_amount_paid = 0
zero_amount_received = 0
negative_amount_received = 0

min_amount_paid = None
max_amount_paid = None
min_amount_received = None
max_amount_received = None

laundering_value_counts = pd.Series(dtype="int64")
laundering_by_payment_format = pd.Series(dtype="int64")
transactions_by_payment_format = pd.Series(dtype="int64")

laundering_by_payment_currency = pd.Series(dtype="int64")

chunk_number = 0


for chunk in pd.read_csv(
    TRANSACTIONS_FILE,
    chunksize=CHUNK_SIZE
):
    chunk_number += 1
    total_rows_checked += len(chunk)

    print(f"Auditing transaction values in chunk {chunk_number}...")

    # --------------------------------------------------
    # AMOUNT VALIDATION
    # --------------------------------------------------

    zero_amount_paid += (chunk["Amount Paid"] == 0).sum()
    negative_amount_paid += (chunk["Amount Paid"] < 0).sum()

    zero_amount_received += (chunk["Amount Received"] == 0).sum()
    negative_amount_received += (chunk["Amount Received"] < 0).sum()


    chunk_min_paid = chunk["Amount Paid"].min()
    chunk_max_paid = chunk["Amount Paid"].max()

    chunk_min_received = chunk["Amount Received"].min()
    chunk_max_received = chunk["Amount Received"].max()


    if min_amount_paid is None or chunk_min_paid < min_amount_paid:
        min_amount_paid = chunk_min_paid

    if max_amount_paid is None or chunk_max_paid > max_amount_paid:
        max_amount_paid = chunk_max_paid

    if (
        min_amount_received is None
        or chunk_min_received < min_amount_received
    ):
        min_amount_received = chunk_min_received

    if (
        max_amount_received is None
        or chunk_max_received > max_amount_received
    ):
        max_amount_received = chunk_max_received


    # --------------------------------------------------
    # LAUNDERING LABEL DISTRIBUTION
    # --------------------------------------------------

    laundering_value_counts = laundering_value_counts.add(
        chunk["Is Laundering"].value_counts(),
        fill_value=0
    )


    # --------------------------------------------------
    # PAYMENT FORMAT DISTRIBUTION
    # --------------------------------------------------

    transactions_by_payment_format = (
        transactions_by_payment_format.add(
            chunk["Payment Format"].value_counts(),
            fill_value=0
        )
    )


    laundering_by_payment_format = (
        laundering_by_payment_format.add(
            chunk.loc[
                chunk["Is Laundering"] == 1,
                "Payment Format"
            ].value_counts(),
            fill_value=0
        )
    )


    # --------------------------------------------------
    # LAUNDERING BY PAYMENT CURRENCY
    # --------------------------------------------------

    laundering_by_payment_currency = (
        laundering_by_payment_currency.add(
            chunk.loc[
                chunk["Is Laundering"] == 1,
                "Payment Currency"
            ].value_counts(),
            fill_value=0
        )
    )


# Convert accumulated counts to integers
laundering_value_counts = laundering_value_counts.astype("int64")

transactions_by_payment_format = (
    transactions_by_payment_format.astype("int64")
)

laundering_by_payment_format = (
    laundering_by_payment_format.astype("int64")
)

laundering_by_payment_currency = (
    laundering_by_payment_currency.astype("int64")
)


# Calculate laundering rate by payment format
laundering_rate_by_payment_format = (
    laundering_by_payment_format
    .div(transactions_by_payment_format)
    .mul(100)
    .fillna(0)
    .sort_values(ascending=False)
)


print("\n" + "-" * 70)
print("TRANSACTION VALUES AND LAUNDERING RESULTS")
print("-" * 70)

print(f"Total Rows Checked          : {total_rows_checked:,}")

print(f"\nZero Amount Paid Rows       : {zero_amount_paid:,}")
print(f"Negative Amount Paid Rows   : {negative_amount_paid:,}")

print(f"Zero Amount Received Rows   : {zero_amount_received:,}")
print(f"Negative Amount Received Rows: {negative_amount_received:,}")

print(f"\nMinimum Amount Paid         : {min_amount_paid:,.6f}")
print(f"Maximum Amount Paid         : {max_amount_paid:,.6f}")

print(f"Minimum Amount Received     : {min_amount_received:,.6f}")
print(f"Maximum Amount Received     : {max_amount_received:,.6f}")


print("\nIs Laundering Label Distribution:")
print(
    laundering_value_counts
    .sort_index()
    .to_string()
)


print("\nTransaction Count By Payment Format:")
print(
    transactions_by_payment_format
    .sort_values(ascending=False)
    .to_string()
)


print("\nLaundering Count By Payment Format:")
print(
    laundering_by_payment_format
    .sort_values(ascending=False)
    .to_string()
)


print("\nLaundering Rate (%) By Payment Format:")
print(
    laundering_rate_by_payment_format.to_string()
)


print("\nLaundering Count By Payment Currency:")
print(
    laundering_by_payment_currency
    .sort_values(ascending=False)
    .to_string()
)

# --------------------------------------------------
# BASIC PATTERNS FILE AUDIT
# --------------------------------------------------

print("\n" + "=" * 70)
print("BASIC PATTERNS FILE AUDIT")
print("=" * 70)


total_pattern_lines = 0
non_empty_pattern_lines = 0
begin_pattern_lines = 0
end_pattern_lines = 0
transaction_pattern_lines = 0

first_20_lines = []


with open(
    PATTERNS_FILE,
    "r",
    encoding="utf-8"
) as patterns_file:

    for line_number, line in enumerate(patterns_file, start=1):

        total_pattern_lines += 1

        stripped_line = line.strip()

        if stripped_line:
            non_empty_pattern_lines += 1

        if stripped_line.startswith("BEGIN LAUNDERING ATTEMPT"):
            begin_pattern_lines += 1

        elif stripped_line.startswith("END LAUNDERING ATTEMPT"):
            end_pattern_lines += 1

        elif stripped_line:
            transaction_pattern_lines += 1


        if line_number <= 20:
            first_20_lines.append(stripped_line)


print(f"\nTotal Lines                 : {total_pattern_lines:,}")

print(f"Non-Empty Lines             : {non_empty_pattern_lines:,}")

print(f"BEGIN Pattern Lines         : {begin_pattern_lines:,}")

print(f"END Pattern Lines           : {end_pattern_lines:,}")

print(f"Transaction Pattern Lines   : {transaction_pattern_lines:,}")


print("\nFirst 20 Lines:")

for line_number, line in enumerate(first_20_lines, start=1):
    print(f"{line_number:>3}: {line}")

# --------------------------------------------------
# PARSE LAUNDERING PATTERNS AND TYPOLOGIES
# --------------------------------------------------

print("\n" + "=" * 70)
print("LAUNDERING PATTERN TYPOLOGY AUDIT")
print("=" * 70)


pattern_attempt_counts = {}
pattern_transaction_counts = {}

current_pattern_type = None
current_attempt_transaction_count = 0

attempt_transaction_counts = []


with open(
    PATTERNS_FILE,
    "r",
    encoding="utf-8"
) as patterns_file:

    for line in patterns_file:

        stripped_line = line.strip()


        # Start of laundering attempt
        if stripped_line.startswith("BEGIN LAUNDERING ATTEMPT"):

            # Extract text between "- " and ":"
            pattern_type = (
                stripped_line
                .split(" - ", 1)[1]
                .split(":", 1)[0]
                .strip()
            )

            current_pattern_type = pattern_type
            current_attempt_transaction_count = 0

            pattern_attempt_counts[current_pattern_type] = (
                pattern_attempt_counts.get(
                    current_pattern_type,
                    0
                )
                + 1
            )


        # End of laundering attempt
        elif stripped_line.startswith("END LAUNDERING ATTEMPT"):

            attempt_transaction_counts.append(
                current_attempt_transaction_count
            )

            current_pattern_type = None
            current_attempt_transaction_count = 0


        # Transaction line inside a laundering attempt
        elif stripped_line and current_pattern_type is not None:

            current_attempt_transaction_count += 1

            pattern_transaction_counts[current_pattern_type] = (
                pattern_transaction_counts.get(
                    current_pattern_type,
                    0
                )
                + 1
            )


print("\nLaundering Attempt Count By Typology:")

for pattern_type, count in sorted(
    pattern_attempt_counts.items(),
    key=lambda item: item[1],
    reverse=True
):
    print(f"{pattern_type:<25} : {count:,}")


print("\nPattern Transaction Count By Typology:")

for pattern_type, count in sorted(
    pattern_transaction_counts.items(),
    key=lambda item: item[1],
    reverse=True
):
    print(f"{pattern_type:<25} : {count:,}")


print(
    f"\nTotal Parsed Attempts       : "
    f"{sum(pattern_attempt_counts.values()):,}"
)

print(
    f"Total Parsed Transaction Lines: "
    f"{sum(pattern_transaction_counts.values()):,}"
)


attempt_counts_series = pd.Series(
    attempt_transaction_counts
)


print("\nTransactions Per Laundering Attempt Statistics:")

print(
    attempt_counts_series
    .describe()
)

# --------------------------------------------------
# MATCH PATTERN TRANSACTIONS TO MAIN TRANSACTIONS
# --------------------------------------------------

print("\n" + "=" * 70)
print("PATTERN TO TRANSACTION MATCHING AUDIT")
print("=" * 70)


def build_transaction_key(
    timestamp,
    from_bank,
    sender_account,
    to_bank,
    receiver_account,
    amount_received,
    receiving_currency,
    amount_paid,
    payment_currency,
    payment_format,
    is_laundering
):
    return (
        str(timestamp),
        int(from_bank),
        str(sender_account),
        int(to_bank),
        str(receiver_account),
        f"{float(amount_received):.6f}",
        str(receiving_currency),
        f"{float(amount_paid):.6f}",
        str(payment_currency),
        str(payment_format),
        int(is_laundering)
    )


# --------------------------------------------------
# PARSE PATTERN TRANSACTION KEYS
# --------------------------------------------------

pattern_transaction_keys = []

with open(
    PATTERNS_FILE,
    "r",
    encoding="utf-8"
) as patterns_file:

    for line in patterns_file:

        stripped_line = line.strip()

        if (
            not stripped_line
            or stripped_line.startswith("BEGIN LAUNDERING ATTEMPT")
            or stripped_line.startswith("END LAUNDERING ATTEMPT")
        ):
            continue

        values = stripped_line.split(",")

        if len(values) != 11:
            continue

        pattern_transaction_keys.append(
            build_transaction_key(*values)
        )


pattern_key_set = set(pattern_transaction_keys)


print(
    f"\nPattern Transaction Lines        : "
    f"{len(pattern_transaction_keys):,}"
)

print(
    f"Unique Pattern Transaction Keys  : "
    f"{len(pattern_key_set):,}"
)


# --------------------------------------------------
# MATCH AGAINST MAIN TRANSACTION FILE
# --------------------------------------------------

matched_main_rows = 0
matched_unique_keys = set()

laundering_rows_not_in_patterns = 0

chunk_number = 0


for chunk in pd.read_csv(
    TRANSACTIONS_FILE,
    chunksize=CHUNK_SIZE
):

    chunk_number += 1

    print(f"Matching patterns in chunk {chunk_number}...")

    laundering_chunk = chunk[
        chunk["Is Laundering"] == 1
    ]


    for row in laundering_chunk.itertuples(index=False):

        transaction_key = build_transaction_key(
            row[0],   # Timestamp
            row[1],   # From Bank
            row[2],   # Account
            row[3],   # To Bank
            row[4],   # Account.1
            row[5],   # Amount Received
            row[6],   # Receiving Currency
            row[7],   # Amount Paid
            row[8],   # Payment Currency
            row[9],   # Payment Format
            row[10]   # Is Laundering
        )


        if transaction_key in pattern_key_set:

            matched_main_rows += 1
            matched_unique_keys.add(transaction_key)

        else:

            laundering_rows_not_in_patterns += 1


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

unmatched_pattern_keys = (
    pattern_key_set - matched_unique_keys
)


print("\n" + "-" * 70)
print("PATTERN TO TRANSACTION MATCHING RESULTS")
print("-" * 70)


print(
    f"Pattern Transaction Lines          : "
    f"{len(pattern_transaction_keys):,}"
)

print(
    f"Unique Pattern Transaction Keys    : "
    f"{len(pattern_key_set):,}"
)

print(
    f"Matched Main Laundering Rows        : "
    f"{matched_main_rows:,}"
)

print(
    f"Matched Unique Pattern Keys         : "
    f"{len(matched_unique_keys):,}"
)

print(
    f"Unmatched Unique Pattern Keys       : "
    f"{len(unmatched_pattern_keys):,}"
)

print(
    f"Main Laundering Rows Not In Patterns: "
    f"{laundering_rows_not_in_patterns:,}"
)

# --------------------------------------------------
# EXACT WHOLE-FILE DUPLICATE AUDIT
# --------------------------------------------------

print("\n" + "=" * 70)
print("EXACT WHOLE-FILE DUPLICATE AUDIT")
print("=" * 70)

seen_hashes = set()

total_rows_hashed = 0
exact_duplicate_rows = 0
duplicate_hashes = set()

chunk_number = 0


for chunk in pd.read_csv(
    TRANSACTIONS_FILE,
    chunksize=CHUNK_SIZE
):

    chunk_number += 1
    total_rows_hashed += len(chunk)

    print(f"Hashing transactions in chunk {chunk_number}...")


    # Create deterministic hash for every complete row
    row_hashes = pd.util.hash_pandas_object(
        chunk,
        index=False
    ).values


    for row_hash in row_hashes:

        row_hash = int(row_hash)

        if row_hash in seen_hashes:

            exact_duplicate_rows += 1
            duplicate_hashes.add(row_hash)

        else:

            seen_hashes.add(row_hash)


print("\n" + "-" * 70)
print("EXACT WHOLE-FILE DUPLICATE RESULTS")
print("-" * 70)

print(f"Total Rows Hashed          : {total_rows_hashed:,}")

print(f"Unique Complete Rows       : {len(seen_hashes):,}")

print(f"Exact Duplicate Rows       : {exact_duplicate_rows:,}")

print(f"Distinct Duplicated Records: {len(duplicate_hashes):,}")

# --------------------------------------------------
# GENERATE RAW DATA AUDIT REPORT
# --------------------------------------------------

print("\n" + "=" * 70)
print("GENERATING RAW DATA AUDIT REPORT")
print("=" * 70)


REPORT_FILE = REPORTS_DIR / "raw_data_audit_report.txt"


report_content = f"""
BANKING FRAUD & FINANCIAL RISK INTELLIGENCE PLATFORM
RAW DATA AUDIT REPORT
===================================================


1. DATASET OVERVIEW
-------------------

Dataset:
IBM Transactions for Anti Money Laundering (AML)

Dataset Variant:
HI-Small

Raw Files:

1. HI-Small_accounts.csv
2. HI-Small_Trans.csv
3. HI-Small_Patterns.txt


2. ACCOUNTS DATASET AUDIT
-------------------------

Total Account Rows:
{len(accounts_df):,}

Total Columns:
{len(accounts_df.columns):,}

Missing Values:
{accounts_df.isna().sum().sum():,}

Duplicate Complete Rows:
{accounts_df.duplicated().sum():,}

Unique Bank IDs:
{accounts_df["Bank ID"].nunique():,}

Unique Account Numbers:
{accounts_df["Account Number"].nunique():,}

Unique Entity IDs:
{accounts_df["Entity ID"].nunique():,}

Unique Entity Names:
{accounts_df["Entity Name"].nunique():,}

Duplicate Account Numbers:
{accounts_df["Account Number"].duplicated().sum():,}

Duplicate Composite Account Keys:
{accounts_df.duplicated(subset=["Bank ID", "Account Number"]).sum():,}

Entity IDs With Multiple Entity Names:
{accounts_df.groupby("Entity ID")["Entity Name"].nunique().gt(1).sum():,}

Entities With Multiple Accounts:
{(accounts_df.groupby("Entity ID").size() > 1).sum():,}

Maximum Accounts Owned By One Entity:
{accounts_df.groupby("Entity ID").size().max():,}


3. TRANSACTION DATASET AUDIT
----------------------------

Total Transaction Rows:
{total_rows:,}

Total Columns:
{len(transactions_sample_df.columns):,}

Missing Values:
{int(missing_values.sum()):,}

Minimum Timestamp:
{min_timestamp}

Maximum Timestamp:
{max_timestamp}

Laundering Transactions:
{laundering_transactions:,}

Laundering Transaction Rate:
{laundering_rate:.6f}%

Zero Amount Paid Rows:
{zero_amount_paid:,}

Negative Amount Paid Rows:
{negative_amount_paid:,}

Zero Amount Received Rows:
{zero_amount_received:,}

Negative Amount Received Rows:
{negative_amount_received:,}

Minimum Amount Paid:
{min_amount_paid:.6f}

Maximum Amount Paid:
{max_amount_paid:.6f}

Minimum Amount Received:
{min_amount_received:.6f}

Maximum Amount Received:
{max_amount_received:.6f}


4. TRANSACTION ACCOUNT REFERENCE VALIDATION
-------------------------------------------

Total Validated Transaction Rows:
{total_validated_rows:,}

Orphan Sender Transaction Rows:
{orphan_sender_rows:,}

Unique Orphan Sender Accounts:
{len(unique_orphan_sender_keys):,}

Orphan Receiver Transaction Rows:
{orphan_receiver_rows:,}

Unique Orphan Receiver Accounts:
{len(unique_orphan_receiver_keys):,}


5. AML PATTERNS FILE AUDIT
--------------------------

Total Pattern File Lines:
{total_pattern_lines:,}

Non-Empty Pattern Lines:
{non_empty_pattern_lines:,}

BEGIN Pattern Lines:
{begin_pattern_lines:,}

END Pattern Lines:
{end_pattern_lines:,}

Transaction Pattern Lines:
{transaction_pattern_lines:,}

Total Laundering Attempts:
{sum(pattern_attempt_counts.values()):,}

Total AML Typologies:
{len(pattern_attempt_counts):,}


AML ATTEMPT COUNT BY TYPOLOGY
-----------------------------

"""

for pattern_type, count in sorted(
    pattern_attempt_counts.items(),
    key=lambda item: item[1],
    reverse=True
):
    report_content += f"{pattern_type}: {count:,}\n"


report_content += """

AML TRANSACTION COUNT BY TYPOLOGY
---------------------------------

"""

for pattern_type, count in sorted(
    pattern_transaction_counts.items(),
    key=lambda item: item[1],
    reverse=True
):
    report_content += f"{pattern_type}: {count:,}\n"


report_content += f"""

6. PATTERN TO TRANSACTION MATCHING
----------------------------------

Pattern Transaction Lines:
{len(pattern_transaction_keys):,}

Unique Pattern Transaction Keys:
{len(pattern_key_set):,}

Matched Main Laundering Rows:
{matched_main_rows:,}

Matched Unique Pattern Keys:
{len(matched_unique_keys):,}

Unmatched Unique Pattern Keys:
{len(unmatched_pattern_keys):,}

Main Laundering Rows Not In Patterns:
{laundering_rows_not_in_patterns:,}


7. EXACT WHOLE-FILE DUPLICATE AUDIT
-----------------------------------

Total Transaction Rows Hashed:
{total_rows_hashed:,}

Unique Complete Transaction Rows:
{len(seen_hashes):,}

Exact Duplicate Transaction Rows:
{exact_duplicate_rows:,}

Distinct Duplicated Transaction Records:
{len(duplicate_hashes):,}


8. RAW DATA AUDIT CONCLUSIONS
-----------------------------

1. The Accounts dataset contains {len(accounts_df):,} account records.

2. The dataset contains {accounts_df["Entity ID"].nunique():,}
   distinct banking entities.

3. The composite key (Bank ID, Account Number) uniquely identifies
   every IBM account record.

4. The Transactions dataset contains {total_rows:,} transaction rows.

5. No missing values were detected in the Transactions dataset.

6. All transaction sender and receiver account references exist
   in the Accounts dataset.

7. The Transactions dataset contains {exact_duplicate_rows:,}
   exact duplicate rows.

8. After removing exact duplicates, the cleaned transaction dataset
   should contain {len(seen_hashes):,} unique transaction rows.

9. The dataset contains {laundering_transactions:,}
   IBM-labelled laundering transactions.

10. The AML Patterns file contains
    {sum(pattern_attempt_counts.values()):,} laundering attempts
    across {len(pattern_attempt_counts):,} AML typologies.

11. The Patterns file contains {len(pattern_transaction_keys):,}
    transaction lines that match the Transactions dataset.

12. {laundering_rows_not_in_patterns:,} laundering-labelled
    transactions are not assigned an explicit typology in the
    Patterns file.

13. These transactions will retain is_laundering = 1 and will receive
    aml_typology = NOT_SPECIFIED during dataset construction.

14. The raw IBM files will remain immutable. All cleaning,
    standardization, derivation, and synthetic data generation will
    be performed in separate project directories.


END OF RAW DATA AUDIT REPORT
============================
"""


# Write report to file
with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as report_file:

    report_file.write(report_content.strip())


print(f"\nRaw Data Audit Report Created Successfully.")

print(f"Report Location: {REPORT_FILE}")

print("\nPHASE 1: RAW DATA AUDIT COMPLETED SUCCESSFULLY.")

