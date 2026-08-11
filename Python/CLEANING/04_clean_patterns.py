from pathlib import Path


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "DATA" / "RAW"
CLEANED_DATA_DIR = PROJECT_ROOT / "DATA" / "CLEANED"

PATTERNS_FILE = RAW_DATA_DIR / "HI-Small_Patterns.txt"

CLEANED_TRANSACTIONS_FILE = (
    CLEANED_DATA_DIR / "transactions.csv"
)


# --------------------------------------------------
# SCRIPT HEADER
# --------------------------------------------------

print("=" * 70)
print("BANKING FRAUD & FINANCIAL RISK INTELLIGENCE PLATFORM")
print("PHASE 2: CLEANING & STANDARDIZATION")
print("STEP 3: CLEAN PATTERNS DATASET")
print("=" * 70)

print(f"\nProject Root              : {PROJECT_ROOT}")
print(f"Raw Patterns File         : {PATTERNS_FILE}")
print(f"Cleaned Transactions File : {CLEANED_TRANSACTIONS_FILE}")
print(f"Cleaned Data Directory    : {CLEANED_DATA_DIR}")


# --------------------------------------------------
# VERIFY REQUIRED FILES
# --------------------------------------------------

if not PATTERNS_FILE.exists():
    raise FileNotFoundError(
        f"Raw patterns file not found: {PATTERNS_FILE}"
    )


if not CLEANED_TRANSACTIONS_FILE.exists():
    raise FileNotFoundError(
        f"Cleaned transactions file not found: "
        f"{CLEANED_TRANSACTIONS_FILE}"
    )


print("\nAll required input files were found successfully.")


# --------------------------------------------------
# INSPECT RAW PATTERNS FILE
# --------------------------------------------------

print("\n" + "=" * 70)
print("INSPECTING RAW PATTERNS FILE")
print("=" * 70)


TOTAL_PREVIEW_LINES = 30


with open(
    PATTERNS_FILE,
    mode="r",
    encoding="utf-8"
) as patterns_file:

    preview_lines = []

    for line_number, line in enumerate(
        patterns_file,
        start=1
    ):

        preview_lines.append(line.rstrip("\n"))

        if line_number >= TOTAL_PREVIEW_LINES:
            break


print(
    f"\nFirst {len(preview_lines)} "
    "Raw Pattern File Lines:"
)


for line_number, line in enumerate(
    preview_lines,
    start=1
):

    print(
        f"{line_number:>4}: {line}"
    )


# --------------------------------------------------
# BASIC FILE COUNTS
# --------------------------------------------------

print("\n" + "=" * 70)
print("COUNTING RAW PATTERN FILE STRUCTURE")
print("=" * 70)


total_lines = 0
non_empty_lines = 0
begin_pattern_lines = 0
end_pattern_lines = 0
transaction_pattern_lines = 0


with open(
    PATTERNS_FILE,
    mode="r",
    encoding="utf-8"
) as patterns_file:

    for line in patterns_file:

        total_lines += 1

        stripped_line = line.strip()


        if not stripped_line:
            continue


        non_empty_lines += 1


        if stripped_line.startswith(
            "BEGIN LAUNDERING ATTEMPT"
        ):

            begin_pattern_lines += 1


        elif stripped_line.startswith(
            "END LAUNDERING ATTEMPT"
        ):

            end_pattern_lines += 1


        else:

            transaction_pattern_lines += 1


print(f"\nTotal Lines               : {total_lines:,}")

print(f"Non-Empty Lines           : {non_empty_lines:,}")

print(f"BEGIN Pattern Lines       : {begin_pattern_lines:,}")

print(f"END Pattern Lines         : {end_pattern_lines:,}")

print(
    f"Transaction Pattern Lines : "
    f"{transaction_pattern_lines:,}"
)


# --------------------------------------------------
# BASIC STRUCTURE VALIDATION
# --------------------------------------------------

if begin_pattern_lines != end_pattern_lines:

    raise ValueError(
        "Pattern structure validation failed: "
        "BEGIN and END counts do not match."
    )


if begin_pattern_lines == 0:

    raise ValueError(
        "Pattern structure validation failed: "
        "no laundering attempts were detected."
    )


print("\nBasic pattern file structure validation passed successfully.")

# --------------------------------------------------
# PARSE LAUNDERING ATTEMPTS
# --------------------------------------------------

print("\n" + "=" * 70)
print("PARSING LAUNDERING ATTEMPTS")
print("=" * 70)


parsed_patterns = []

current_pattern = None


with open(
    PATTERNS_FILE,
    mode="r",
    encoding="utf-8"
) as patterns_file:

    for file_line_number, line in enumerate(
        patterns_file,
        start=1
    ):

        stripped_line = line.strip()


        # ------------------------------------------
        # IGNORE EMPTY LINES
        # ------------------------------------------

        if not stripped_line:
            continue


        # ------------------------------------------
        # BEGIN LAUNDERING ATTEMPT
        # ------------------------------------------

        if stripped_line.startswith(
            "BEGIN LAUNDERING ATTEMPT"
        ):

            if current_pattern is not None:

                raise ValueError(
                    f"Nested BEGIN detected at "
                    f"file line {file_line_number}."
                )


            # Example:
            # BEGIN LAUNDERING ATTEMPT - FAN-OUT: Max 16-degree Fan-Out

            header_content = stripped_line.split(
                "BEGIN LAUNDERING ATTEMPT - ",
                maxsplit=1
            )[1]


            if ":" in header_content:

                typology, pattern_description = (
                    header_content.split(
                        ":",
                        maxsplit=1
                    )
                )

                typology = typology.strip()

                pattern_description = (
                    pattern_description.strip()
                )

            else:

                typology = header_content.strip()

                pattern_description = ""


            aml_pattern_id = (
                f"AML_PATTERN_"
                f"{len(parsed_patterns) + 1:04d}"
            )


            current_pattern = {

                "aml_pattern_id": aml_pattern_id,

                "typology": typology,

                "pattern_description": pattern_description,

                "begin_file_line_number": file_line_number,

                "end_file_line_number": None,

                "transaction_lines": []
            }


        # ------------------------------------------
        # END LAUNDERING ATTEMPT
        # ------------------------------------------

        elif stripped_line.startswith(
            "END LAUNDERING ATTEMPT"
        ):

            if current_pattern is None:

                raise ValueError(
                    f"END without BEGIN detected at "
                    f"file line {file_line_number}."
                )


            # Example:
            # END LAUNDERING ATTEMPT - FAN-OUT

            end_typology = stripped_line.split(
                "END LAUNDERING ATTEMPT - ",
                maxsplit=1
            )[1].strip()


            if end_typology != current_pattern["typology"]:

                raise ValueError(
                    f"Typology mismatch at file line "
                    f"{file_line_number}: "
                    f"BEGIN={current_pattern['typology']}, "
                    f"END={end_typology}"
                )


            current_pattern[
                "end_file_line_number"
            ] = file_line_number


            parsed_patterns.append(
                current_pattern
            )


            current_pattern = None


        # ------------------------------------------
        # PATTERN TRANSACTION LINE
        # ------------------------------------------

        else:

            if current_pattern is None:

                raise ValueError(
                    f"Transaction line outside laundering "
                    f"attempt at file line "
                    f"{file_line_number}."
                )


            current_pattern[
                "transaction_lines"
            ].append(

                {
                    "file_line_number": file_line_number,

                    "raw_transaction_line": stripped_line
                }

            )


# --------------------------------------------------
# VALIDATE FINAL PARSER STATE
# --------------------------------------------------

if current_pattern is not None:

    raise ValueError(
        "Patterns file ended before the final "
        "laundering attempt was closed."
    )


# --------------------------------------------------
# PARSER COUNTS
# --------------------------------------------------

parsed_pattern_count = len(parsed_patterns)

parsed_transaction_line_count = sum(

    len(pattern["transaction_lines"])

    for pattern in parsed_patterns
)


parsed_typologies = sorted(

    {
        pattern["typology"]

        for pattern in parsed_patterns
    }

)


# --------------------------------------------------
# VALIDATE PARSER COUNTS
# --------------------------------------------------

if parsed_pattern_count != begin_pattern_lines:

    raise ValueError(
        "Parsed laundering attempt count does not "
        "match BEGIN pattern count."
    )


if parsed_transaction_line_count != transaction_pattern_lines:

    raise ValueError(
        "Parsed transaction line count does not "
        "match raw transaction pattern line count."
    )


# --------------------------------------------------
# PRINT PARSER RESULTS
# --------------------------------------------------

print("\nLaundering attempts parsed successfully.")

print(
    f"\nParsed Laundering Attempts : "
    f"{parsed_pattern_count:,}"
)

print(
    f"Parsed Transaction Lines   : "
    f"{parsed_transaction_line_count:,}"
)

print(
    f"Distinct AML Typologies    : "
    f"{len(parsed_typologies):,}"
)


print("\nAML Typologies:")

for typology in parsed_typologies:

    typology_count = sum(

        1

        for pattern in parsed_patterns

        if pattern["typology"] == typology
    )

    print(
        f"  - {typology:<20} "
        f"{typology_count:>4,} attempts"
    )


print("\nFirst 5 Parsed Laundering Attempts:")

for pattern in parsed_patterns[:5]:

    print(
        f"\n  AML Pattern ID      : "
        f"{pattern['aml_pattern_id']}"
    )

    print(
        f"  Typology            : "
        f"{pattern['typology']}"
    )

    print(
        f"  Pattern Description : "
        f"{pattern['pattern_description']}"
    )

    print(
        f"  Transaction Count   : "
        f"{len(pattern['transaction_lines']):,}"
    )

    print(
        f"  File Line Range     : "
        f"{pattern['begin_file_line_number']} - "
        f"{pattern['end_file_line_number']}"
    )

# --------------------------------------------------
# CREATE AML PATTERNS TABLE
# --------------------------------------------------

print("\n" + "=" * 70)
print("CREATING AML PATTERNS TABLE")
print("=" * 70)


import pandas as pd


# --------------------------------------------------
# BUILD ONE ROW PER LAUNDERING ATTEMPT
# --------------------------------------------------

aml_patterns_df = pd.DataFrame(

    [

        {
            "aml_pattern_id":
                pattern["aml_pattern_id"],

            "typology":
                pattern["typology"],

            "pattern_description":
                pattern["pattern_description"],

            "transaction_count":
                len(pattern["transaction_lines"]),

            "begin_file_line_number":
                pattern["begin_file_line_number"],

            "end_file_line_number":
                pattern["end_file_line_number"]
        }

        for pattern in parsed_patterns
    ]

)


# --------------------------------------------------
# VALIDATE ROW COUNT
# --------------------------------------------------

if len(aml_patterns_df) != 370:

    raise ValueError(
        f"Unexpected AML patterns row count: "
        f"{len(aml_patterns_df):,}"
    )


# --------------------------------------------------
# VALIDATE PRIMARY KEY
# --------------------------------------------------

if not aml_patterns_df["aml_pattern_id"].is_unique:

    raise ValueError(
        "Duplicate aml_pattern_id values detected."
    )


if aml_patterns_df["aml_pattern_id"].isna().any():

    raise ValueError(
        "Missing aml_pattern_id values detected."
    )


# --------------------------------------------------
# VALIDATE TYPOLOGIES
# --------------------------------------------------

EXPECTED_TYPOLOGIES = {

    "BIPARTITE",
    "CYCLE",
    "FAN-IN",
    "FAN-OUT",
    "GATHER-SCATTER",
    "RANDOM",
    "SCATTER-GATHER",
    "STACK"
}


actual_typologies = set(
    aml_patterns_df["typology"].unique()
)


if actual_typologies != EXPECTED_TYPOLOGIES:

    raise ValueError(
        "AML typology set does not match "
        "the expected IBM typologies."
    )


# --------------------------------------------------
# VALIDATE TRANSACTION COUNTS
# --------------------------------------------------

if (
    aml_patterns_df["transaction_count"].sum()
    != 3_209
):

    raise ValueError(
        "AML pattern transaction count total "
        "does not equal 3,209."
    )


if (
    aml_patterns_df["transaction_count"] <= 0
).any():

    raise ValueError(
        "AML pattern with zero transactions detected."
    )


# --------------------------------------------------
# VALIDATE FILE LINE RANGES
# --------------------------------------------------

invalid_line_ranges = (

    aml_patterns_df[
        "begin_file_line_number"
    ]

    >=

    aml_patterns_df[
        "end_file_line_number"
    ]

).sum()


if invalid_line_ranges > 0:

    raise ValueError(
        f"{invalid_line_ranges:,} invalid "
        "pattern file line ranges detected."
    )


# --------------------------------------------------
# PRINT RESULTS
# --------------------------------------------------

print("\nAML patterns table created successfully.")

print(
    f"\nAML Pattern Rows       : "
    f"{len(aml_patterns_df):,}"
)

print(
    f"Unique AML Pattern IDs : "
    f"{aml_patterns_df['aml_pattern_id'].nunique():,}"
)

print(
    f"Distinct Typologies     : "
    f"{aml_patterns_df['typology'].nunique():,}"
)

print(
    f"Total Pattern Transactions: "
    f"{aml_patterns_df['transaction_count'].sum():,}"
)


print("\nAML Pattern Columns:")

for column in aml_patterns_df.columns:
    print(f"  - {column}")


print("\nTypology Distribution:")

print(

    aml_patterns_df[
        "typology"
    ]
    .value_counts()
    .sort_index()

)


print("\nTransaction Count Statistics:")

print(

    aml_patterns_df[
        "transaction_count"
    ]
    .describe()

)


print("\nFirst 10 AML Pattern Records:")

print(
    aml_patterns_df.head(10)
)

# --------------------------------------------------
# CREATE PATTERN TRANSACTION OCCURRENCE TABLE
# --------------------------------------------------

print("\n" + "=" * 70)
print("CREATING PATTERN TRANSACTION OCCURRENCE TABLE")
print("=" * 70)


PATTERN_TRANSACTION_COLUMNS = [
    "timestamp",
    "from_bank_id",
    "sender_account_number",
    "to_bank_id",
    "receiver_account_number",
    "amount_received",
    "receiving_currency",
    "amount_paid",
    "payment_currency",
    "payment_format",
    "is_laundering"
]


pattern_transaction_records = []


# --------------------------------------------------
# PARSE EVERY PATTERN TRANSACTION LINE
# --------------------------------------------------

for pattern in parsed_patterns:

    for occurrence_number, transaction_line in enumerate(
        pattern["transaction_lines"],
        start=1
    ):

        raw_transaction_line = (
            transaction_line["raw_transaction_line"]
        )

        values = [
            value.strip()
            for value in raw_transaction_line.split(",")
        ]


        # ------------------------------------------
        # VALIDATE COLUMN COUNT
        # ------------------------------------------

        if len(values) != 11:

            raise ValueError(
                f"Expected 11 transaction values, "
                f"found {len(values)} at file line "
                f"{transaction_line['file_line_number']}."
            )


        transaction_values = dict(
            zip(
                PATTERN_TRANSACTION_COLUMNS,
                values
            )
        )


        pattern_transaction_records.append(

            {
                "pattern_transaction_occurrence_id":
                    f"PATTERN_TXN_{len(pattern_transaction_records) + 1:04d}",

                "aml_pattern_id":
                    pattern["aml_pattern_id"],

                "pattern_transaction_sequence":
                    occurrence_number,

                "file_line_number":
                    transaction_line["file_line_number"],

                **transaction_values
            }

        )


# --------------------------------------------------
# CREATE DATAFRAME
# --------------------------------------------------

pattern_transactions_df = pd.DataFrame(
    pattern_transaction_records
)


# --------------------------------------------------
# APPLY DATA TYPES
# --------------------------------------------------

pattern_transactions_df["timestamp"] = pd.to_datetime(
    pattern_transactions_df["timestamp"],
    format="%Y/%m/%d %H:%M",
    errors="coerce"
)


pattern_transactions_df["from_bank_id"] = pd.to_numeric(
    pattern_transactions_df["from_bank_id"],
    errors="raise"
).astype("int64")


pattern_transactions_df["to_bank_id"] = pd.to_numeric(
    pattern_transactions_df["to_bank_id"],
    errors="raise"
).astype("int64")


pattern_transactions_df["amount_received"] = pd.to_numeric(
    pattern_transactions_df["amount_received"],
    errors="raise"
).astype("float64")


pattern_transactions_df["amount_paid"] = pd.to_numeric(
    pattern_transactions_df["amount_paid"],
    errors="raise"
).astype("float64")


pattern_transactions_df["is_laundering"] = pd.to_numeric(
    pattern_transactions_df["is_laundering"],
    errors="raise"
).astype("int64")


# --------------------------------------------------
# VALIDATE ROW COUNT
# --------------------------------------------------

if len(pattern_transactions_df) != 3_209:

    raise ValueError(
        f"Unexpected pattern transaction row count: "
        f"{len(pattern_transactions_df):,}"
    )


# --------------------------------------------------
# VALIDATE OCCURRENCE PRIMARY KEY
# --------------------------------------------------

if not pattern_transactions_df[
    "pattern_transaction_occurrence_id"
].is_unique:

    raise ValueError(
        "Duplicate pattern transaction occurrence IDs detected."
    )


# --------------------------------------------------
# VALIDATE PATTERN FOREIGN KEY
# --------------------------------------------------

invalid_pattern_references = (

    ~pattern_transactions_df[
        "aml_pattern_id"
    ].isin(
        aml_patterns_df["aml_pattern_id"]
    )

).sum()


if invalid_pattern_references > 0:

    raise ValueError(
        f"{invalid_pattern_references:,} invalid "
        "AML pattern references detected."
    )


# --------------------------------------------------
# VALIDATE TIMESTAMPS
# --------------------------------------------------

invalid_pattern_timestamps = (

    pattern_transactions_df[
        "timestamp"
    ].isna().sum()

)


if invalid_pattern_timestamps > 0:

    raise ValueError(
        f"{invalid_pattern_timestamps:,} invalid "
        "pattern transaction timestamps detected."
    )


# --------------------------------------------------
# VALIDATE LAUNDERING LABELS
# --------------------------------------------------

invalid_laundering_labels = (

    ~pattern_transactions_df[
        "is_laundering"
    ].isin([0, 1])

).sum()


if invalid_laundering_labels > 0:

    raise ValueError(
        f"{invalid_laundering_labels:,} invalid "
        "laundering labels detected."
    )


# --------------------------------------------------
# VALIDATE SEQUENCE NUMBERS
# --------------------------------------------------

expected_sequence_counts = (

    pattern_transactions_df
    .groupby("aml_pattern_id")
    ["pattern_transaction_sequence"]
    .max()

)


actual_pattern_counts = (

    aml_patterns_df
    .set_index("aml_pattern_id")
    ["transaction_count"]

)


if not expected_sequence_counts.equals(
    actual_pattern_counts
):

    raise ValueError(
        "Pattern transaction sequence validation failed."
    )


# --------------------------------------------------
# PRINT RESULTS
# --------------------------------------------------

print(
    "\nPattern transaction occurrence table "
    "created successfully."
)

print(
    f"\nPattern Transaction Rows       : "
    f"{len(pattern_transactions_df):,}"
)

print(
    f"Unique Occurrence IDs          : "
    f"{pattern_transactions_df['pattern_transaction_occurrence_id'].nunique():,}"
)

print(
    f"Referenced AML Patterns        : "
    f"{pattern_transactions_df['aml_pattern_id'].nunique():,}"
)

print(
    f"Invalid Pattern References      : "
    f"{invalid_pattern_references:,}"
)

print(
    f"Invalid Pattern Timestamps      : "
    f"{invalid_pattern_timestamps:,}"
)

print(
    f"Distinct Raw Transaction Lines  : "
    f"{pattern_transactions_df[PATTERN_TRANSACTION_COLUMNS].drop_duplicates().shape[0]:,}"
)


print("\nPattern Transaction Columns:")

for column in pattern_transactions_df.columns:
    print(f"  - {column}")


print("\nFirst 10 Pattern Transaction Records:")

print(
    pattern_transactions_df.head(10)
)

# --------------------------------------------------
# MAP PATTERN OCCURRENCES TO CLEANED TRANSACTIONS
# --------------------------------------------------

print("\n" + "=" * 70)
print("MAPPING PATTERN OCCURRENCES TO CLEANED TRANSACTIONS")
print("=" * 70)


TRANSACTION_CHUNK_SIZE = 250_000


# --------------------------------------------------
# DEFINE EXACT TRANSACTION MATCHING COLUMNS
# --------------------------------------------------

MATCH_COLUMNS = [
    "timestamp",
    "from_bank_id",
    "sender_account_number",
    "to_bank_id",
    "receiver_account_number",
    "amount_received",
    "receiving_currency",
    "amount_paid",
    "payment_currency",
    "payment_format",
    "is_laundering"
]


# --------------------------------------------------
# CREATE EXACT MATCH KEY
#
# IMPORTANT:
# We do not concatenate values into strings.
# pandas MultiIndex preserves the typed composite key.
# --------------------------------------------------

pattern_match_index = pd.MultiIndex.from_frame(
    pattern_transactions_df[MATCH_COLUMNS]
)


# --------------------------------------------------
# VALIDATE PATTERN KEYS
# --------------------------------------------------

unique_pattern_match_key_count = (
    pattern_match_index.nunique()
)


print(
    f"\nPattern Occurrence Rows      : "
    f"{len(pattern_transactions_df):,}"
)

print(
    f"Unique Pattern Match Keys    : "
    f"{unique_pattern_match_key_count:,}"
)


if unique_pattern_match_key_count != 3_209:

    raise ValueError(
        "Pattern transaction match keys are not unique. "
        "The matching strategy must be reviewed."
    )


# --------------------------------------------------
# STORAGE FOR MATCHED CLEANED TRANSACTIONS
# --------------------------------------------------

matched_transaction_parts = []

total_cleaned_rows_scanned = 0

total_candidate_rows_found = 0


# --------------------------------------------------
# SCAN CLEANED TRANSACTIONS IN CHUNKS
# --------------------------------------------------

for chunk_number, transaction_chunk in enumerate(

    pd.read_csv(
        CLEANED_TRANSACTIONS_FILE,
        usecols=[
            "transaction_id",
            *MATCH_COLUMNS
        ],
        parse_dates=["timestamp"],
        chunksize=TRANSACTION_CHUNK_SIZE
    ),

    start=1
):

    total_cleaned_rows_scanned += len(
        transaction_chunk
    )


    # ----------------------------------------------
    # BUILD TYPED COMPOSITE INDEX FOR THIS CHUNK
    # ----------------------------------------------

    chunk_match_index = pd.MultiIndex.from_frame(
        transaction_chunk[MATCH_COLUMNS]
    )


    # ----------------------------------------------
    # FIND ROWS WHOSE EXACT KEY EXISTS IN PATTERNS
    # ----------------------------------------------

    matching_mask = chunk_match_index.isin(
        pattern_match_index
    )


    matched_chunk = transaction_chunk.loc[
        matching_mask,
        [
            "transaction_id",
            *MATCH_COLUMNS
        ]
    ].copy()


    total_candidate_rows_found += len(
        matched_chunk
    )


    if not matched_chunk.empty:

        matched_transaction_parts.append(
            matched_chunk
        )


    print(
        f"Processed Chunk {chunk_number:>2} | "
        f"Rows Scanned: "
        f"{total_cleaned_rows_scanned:>9,} | "
        f"Candidate Matches Found: "
        f"{total_candidate_rows_found:>5,}"
    )


# --------------------------------------------------
# COMBINE MATCHED CLEANED TRANSACTIONS
# --------------------------------------------------

if not matched_transaction_parts:

    raise ValueError(
        "No cleaned transactions matched "
        "the pattern transaction occurrences."
    )


matched_cleaned_transactions_df = pd.concat(
    matched_transaction_parts,
    ignore_index=True
)


# --------------------------------------------------
# VALIDATE SCANNED ROW COUNT
# --------------------------------------------------

if total_cleaned_rows_scanned != 5_078_336:

    raise ValueError(
        f"Unexpected cleaned transaction row count: "
        f"{total_cleaned_rows_scanned:,}"
    )


# --------------------------------------------------
# VALIDATE CANDIDATE MATCH TABLE
# --------------------------------------------------

duplicate_matched_transaction_ids = (

    matched_cleaned_transactions_df[
        "transaction_id"
    ].duplicated().sum()

)


duplicate_matched_keys = (

    matched_cleaned_transactions_df[
        MATCH_COLUMNS
    ].duplicated().sum()

)


print("\nCleaned transaction scan completed successfully.")

print(
    f"\nTotal Cleaned Rows Scanned       : "
    f"{total_cleaned_rows_scanned:,}"
)

print(
    f"Candidate Cleaned Rows Found     : "
    f"{len(matched_cleaned_transactions_df):,}"
)

print(
    f"Unique Matched Transaction IDs   : "
    f"{matched_cleaned_transactions_df['transaction_id'].nunique():,}"
)

print(
    f"Duplicate Matched Transaction IDs: "
    f"{duplicate_matched_transaction_ids:,}"
)

print(
    f"Duplicate Matched Composite Keys : "
    f"{duplicate_matched_keys:,}"
)


# --------------------------------------------------
# ATTACH TRANSACTION IDs TO PATTERN OCCURRENCES
# --------------------------------------------------

pattern_transactions_mapped_df = (

    pattern_transactions_df.merge(

        matched_cleaned_transactions_df,

        on=MATCH_COLUMNS,

        how="left",

        validate="one_to_one"
    )

)


# --------------------------------------------------
# VALIDATE MAPPING RESULTS
# --------------------------------------------------

unmatched_pattern_occurrences = (

    pattern_transactions_mapped_df[
        "transaction_id"
    ].isna().sum()

)


mapped_occurrence_rows = (

    pattern_transactions_mapped_df[
        "transaction_id"
    ].notna().sum()

)


unique_mapped_transaction_ids = (

    pattern_transactions_mapped_df[
        "transaction_id"
    ].nunique()

)


if unmatched_pattern_occurrences > 0:

    raise ValueError(
        f"{unmatched_pattern_occurrences:,} pattern "
        "transaction occurrences could not be mapped "
        "to cleaned transaction IDs."
    )


if mapped_occurrence_rows != 3_209:

    raise ValueError(
        f"Unexpected mapped occurrence row count: "
        f"{mapped_occurrence_rows:,}"
    )


# --------------------------------------------------
# REORDER COLUMNS
# --------------------------------------------------

PATTERN_MAPPED_COLUMNS = [

    "pattern_transaction_occurrence_id",
    "aml_pattern_id",
    "pattern_transaction_sequence",
    "transaction_id",
    "file_line_number",

    "timestamp",
    "from_bank_id",
    "sender_account_number",
    "to_bank_id",
    "receiver_account_number",

    "amount_received",
    "receiving_currency",
    "amount_paid",
    "payment_currency",
    "payment_format",
    "is_laundering"
]


pattern_transactions_mapped_df = (

    pattern_transactions_mapped_df[
        PATTERN_MAPPED_COLUMNS
    ]

)


# --------------------------------------------------
# PRINT FINAL MAPPING RESULTS
# --------------------------------------------------

print("\n" + "=" * 70)
print("PATTERN TRANSACTION MAPPING RESULTS")
print("=" * 70)


print(
    f"\nPattern Occurrence Rows       : "
    f"{len(pattern_transactions_mapped_df):,}"
)

print(
    f"Mapped Occurrence Rows        : "
    f"{mapped_occurrence_rows:,}"
)

print(
    f"Unmatched Pattern Occurrences : "
    f"{unmatched_pattern_occurrences:,}"
)

print(
    f"Unique Mapped Transaction IDs : "
    f"{unique_mapped_transaction_ids:,}"
)

print(
    f"Referenced AML Patterns       : "
    f"{pattern_transactions_mapped_df['aml_pattern_id'].nunique():,}"
)


print("\nFirst 10 Mapped Pattern Transactions:")

print(
    pattern_transactions_mapped_df.head(10)
)

# --------------------------------------------------
# FINAL AML PATTERN RELATIONSHIP VALIDATION
# --------------------------------------------------

print("\n" + "=" * 70)
print("FINAL AML PATTERN RELATIONSHIP VALIDATION")
print("=" * 70)


# --------------------------------------------------
# 1. VALIDATE ALL PATTERN TRANSACTIONS ARE LAUNDERING
# --------------------------------------------------

non_laundering_pattern_rows = (

    pattern_transactions_mapped_df[
        "is_laundering"
    ].ne(1).sum()

)


if non_laundering_pattern_rows > 0:

    raise ValueError(
        f"{non_laundering_pattern_rows:,} mapped pattern "
        "transactions are not labelled as laundering."
    )


# --------------------------------------------------
# 2. VALIDATE ACTUAL TRANSACTION COUNT PER PATTERN
# --------------------------------------------------

actual_mapped_counts = (

    pattern_transactions_mapped_df

    .groupby("aml_pattern_id")

    .size()

    .rename("actual_mapped_transaction_count")

)


pattern_count_validation_df = (

    aml_patterns_df[
        [
            "aml_pattern_id",
            "transaction_count"
        ]
    ]

    .merge(

        actual_mapped_counts,

        on="aml_pattern_id",

        how="left",

        validate="one_to_one"
    )

)


pattern_count_validation_df[
    "actual_mapped_transaction_count"
] = (

    pattern_count_validation_df[
        "actual_mapped_transaction_count"
    ]

    .fillna(0)

    .astype("int64")

)


pattern_count_mismatches = (

    pattern_count_validation_df[
        "transaction_count"
    ]

    !=

    pattern_count_validation_df[
        "actual_mapped_transaction_count"
    ]

).sum()


if pattern_count_mismatches > 0:

    raise ValueError(
        f"{pattern_count_mismatches:,} AML patterns have "
        "incorrect mapped transaction counts."
    )


# --------------------------------------------------
# 3. VALIDATE CONTIGUOUS SEQUENCES WITHIN PATTERNS
# --------------------------------------------------

invalid_sequence_patterns = 0


for aml_pattern_id, group in (

    pattern_transactions_mapped_df

    .groupby(
        "aml_pattern_id",
        sort=False
    )

):

    actual_sequences = sorted(

        group[
            "pattern_transaction_sequence"
        ].tolist()

    )


    expected_sequences = list(

        range(
            1,
            len(group) + 1
        )

    )


    if actual_sequences != expected_sequences:

        invalid_sequence_patterns += 1


if invalid_sequence_patterns > 0:

    raise ValueError(
        f"{invalid_sequence_patterns:,} AML patterns have "
        "invalid transaction sequences."
    )


# --------------------------------------------------
# 4. VALIDATE TRANSACTION ID UNIQUENESS
# --------------------------------------------------

duplicate_pattern_transaction_ids = (

    pattern_transactions_mapped_df[
        "transaction_id"
    ]

    .duplicated()

    .sum()

)


if duplicate_pattern_transaction_ids > 0:

    raise ValueError(
        f"{duplicate_pattern_transaction_ids:,} duplicate "
        "transaction IDs detected across AML patterns."
    )


# --------------------------------------------------
# 5. VERIFY TOTAL LAUNDERING TRANSACTIONS AND
#    LAUNDERING TRANSACTIONS OUTSIDE PATTERNS
# --------------------------------------------------

pattern_transaction_ids = set(

    pattern_transactions_mapped_df[
        "transaction_id"
    ]

)


total_laundering_transactions = 0

laundering_transactions_in_patterns = 0

laundering_transactions_outside_patterns = 0


for transaction_chunk in pd.read_csv(

    CLEANED_TRANSACTIONS_FILE,

    usecols=[
        "transaction_id",
        "is_laundering"
    ],

    chunksize=TRANSACTION_CHUNK_SIZE

):

    laundering_chunk = transaction_chunk.loc[

        transaction_chunk[
            "is_laundering"
        ].eq(1),

        [
            "transaction_id",
            "is_laundering"
        ]

    ]


    total_laundering_transactions += len(
        laundering_chunk
    )


    in_pattern_mask = (

        laundering_chunk[
            "transaction_id"
        ].isin(
            pattern_transaction_ids
        )

    )


    laundering_transactions_in_patterns += (

        in_pattern_mask.sum()

    )


    laundering_transactions_outside_patterns += (

        (~in_pattern_mask).sum()

    )


# --------------------------------------------------
# 6. FINAL EXPECTED COUNT VALIDATIONS
# --------------------------------------------------

if total_laundering_transactions != 5_177:

    raise ValueError(
        f"Unexpected total laundering transaction count: "
        f"{total_laundering_transactions:,}"
    )


if laundering_transactions_in_patterns != 3_209:

    raise ValueError(
        f"Unexpected laundering transactions represented "
        f"in patterns: "
        f"{laundering_transactions_in_patterns:,}"
    )


if laundering_transactions_outside_patterns != 1_968:

    raise ValueError(
        f"Unexpected laundering transactions outside "
        f"patterns: "
        f"{laundering_transactions_outside_patterns:,}"
    )


# --------------------------------------------------
# PRINT FINAL VALIDATION RESULTS
# --------------------------------------------------

print("\nAll AML pattern relationship validations passed successfully.")


print(
    f"\nAML Patterns                          : "
    f"{len(aml_patterns_df):,}"
)

print(
    f"Pattern Transaction Occurrences       : "
    f"{len(pattern_transactions_mapped_df):,}"
)

print(
    f"Non-Laundering Pattern Rows            : "
    f"{non_laundering_pattern_rows:,}"
)

print(
    f"Pattern Transaction Count Mismatches   : "
    f"{pattern_count_mismatches:,}"
)

print(
    f"Patterns With Invalid Sequences        : "
    f"{invalid_sequence_patterns:,}"
)

print(
    f"Duplicate Pattern Transaction IDs      : "
    f"{duplicate_pattern_transaction_ids:,}"
)

print(
    f"Total Laundering Transactions          : "
    f"{total_laundering_transactions:,}"
)

print(
    f"Laundering Transactions In Patterns    : "
    f"{laundering_transactions_in_patterns:,}"
)

print(
    f"Laundering Transactions Outside Patterns: "
    f"{laundering_transactions_outside_patterns:,}"
)

# --------------------------------------------------
# CREATE FINAL NORMALIZED AML OUTPUT TABLES
# --------------------------------------------------

print("\n" + "=" * 70)
print("CREATING FINAL NORMALIZED AML OUTPUT TABLES")
print("=" * 70)


# --------------------------------------------------
# DEFINE OUTPUT FILES
# --------------------------------------------------

AML_PATTERNS_OUTPUT_FILE = (
    CLEANED_DATA_DIR / "aml_patterns.csv"
)

AML_PATTERN_TRANSACTIONS_OUTPUT_FILE = (
    CLEANED_DATA_DIR / "aml_pattern_transactions.csv"
)


# --------------------------------------------------
# CREATE FINAL AML PATTERNS TABLE
# --------------------------------------------------

FINAL_AML_PATTERN_COLUMNS = [

    "aml_pattern_id",
    "typology",
    "pattern_description",
    "transaction_count"

]


final_aml_patterns_df = (

    aml_patterns_df[
        FINAL_AML_PATTERN_COLUMNS
    ]

    .copy()

)

# --------------------------------------------------
# STANDARDIZE MISSING PATTERN DESCRIPTIONS
# --------------------------------------------------

pattern_description_text = (

    final_aml_patterns_df[
        "pattern_description"
    ]

    .astype("string")

    .str.strip()

)


missing_pattern_descriptions_before = (

    pattern_description_text.isna()

    |

    pattern_description_text.eq("")

).sum()


final_aml_patterns_df[
    "pattern_description"
] = (

    pattern_description_text

    .fillna("Not Provided")

    .replace("", "Not Provided")

)


pattern_description_after = (

    final_aml_patterns_df[
        "pattern_description"
    ]

    .astype("string")

    .str.strip()

)


missing_pattern_descriptions_after = (

    pattern_description_after.isna()

    |

    pattern_description_after.eq("")

).sum()


print("\nPattern Description Standardization:")

print(
    f"  Missing/Blank Before : "
    f"{missing_pattern_descriptions_before:,}"
)

print(
    f"  Missing/Blank After  : "
    f"{missing_pattern_descriptions_after:,}"
)


if missing_pattern_descriptions_after > 0:

    raise ValueError(
        "Missing or blank pattern descriptions "
        "remain after standardization."
    )

# --------------------------------------------------
# CREATE FINAL AML PATTERN TRANSACTION BRIDGE TABLE
# --------------------------------------------------

FINAL_AML_PATTERN_TRANSACTION_COLUMNS = [

    "pattern_transaction_occurrence_id",
    "aml_pattern_id",
    "transaction_id",
    "pattern_transaction_sequence"

]


final_aml_pattern_transactions_df = (

    pattern_transactions_mapped_df[
        FINAL_AML_PATTERN_TRANSACTION_COLUMNS
    ]

    .copy()

)


# --------------------------------------------------
# SORT OUTPUT TABLES DETERMINISTICALLY
# --------------------------------------------------

final_aml_patterns_df = (

    final_aml_patterns_df

    .sort_values(
        by="aml_pattern_id"
    )

    .reset_index(drop=True)

)


final_aml_pattern_transactions_df = (

    final_aml_pattern_transactions_df

    .sort_values(

        by=[
            "aml_pattern_id",
            "pattern_transaction_sequence"
        ]

    )

    .reset_index(drop=True)

)


# --------------------------------------------------
# VALIDATE AML PATTERNS OUTPUT
# --------------------------------------------------

if len(final_aml_patterns_df) != 370:

    raise ValueError(
        "Final AML patterns table must contain "
        "exactly 370 rows."
    )


if not final_aml_patterns_df[
    "aml_pattern_id"
].is_unique:

    raise ValueError(
        "Duplicate aml_pattern_id values detected "
        "in final AML patterns table."
    )


if final_aml_patterns_df.isna().any().any():

    raise ValueError(
        "Missing values detected in final "
        "AML patterns table."
    )


if (
    final_aml_patterns_df[
        "transaction_count"
    ].sum()
    != 3_209
):

    raise ValueError(
        "Final AML pattern transaction count "
        "total does not equal 3,209."
    )


# --------------------------------------------------
# VALIDATE BRIDGE TABLE OUTPUT
# --------------------------------------------------

if len(final_aml_pattern_transactions_df) != 3_209:

    raise ValueError(
        "Final AML pattern transaction bridge table "
        "must contain exactly 3,209 rows."
    )


if not final_aml_pattern_transactions_df[
    "pattern_transaction_occurrence_id"
].is_unique:

    raise ValueError(
        "Duplicate pattern transaction occurrence IDs "
        "detected in final bridge table."
    )


if final_aml_pattern_transactions_df[
    "transaction_id"
].duplicated().any():

    raise ValueError(
        "Duplicate transaction IDs detected "
        "in final AML bridge table."
    )


if final_aml_pattern_transactions_df.isna().any().any():

    raise ValueError(
        "Missing values detected in final "
        "AML bridge table."
    )


# --------------------------------------------------
# VALIDATE FOREIGN KEY TO AML PATTERNS
# --------------------------------------------------

invalid_aml_pattern_foreign_keys = (

    ~final_aml_pattern_transactions_df[
        "aml_pattern_id"
    ].isin(
        final_aml_patterns_df[
            "aml_pattern_id"
        ]
    )

).sum()


if invalid_aml_pattern_foreign_keys > 0:

    raise ValueError(
        f"{invalid_aml_pattern_foreign_keys:,} invalid "
        "AML pattern foreign keys detected."
    )


# --------------------------------------------------
# VALIDATE FOREIGN KEY TO TRANSACTIONS
#
# We already validated this relationship during
# the mapping stage. Here we verify the final bridge
# table still contains exactly the mapped IDs.
# --------------------------------------------------

expected_transaction_ids = set(

    pattern_transactions_mapped_df[
        "transaction_id"
    ]

)


final_bridge_transaction_ids = set(

    final_aml_pattern_transactions_df[
        "transaction_id"
    ]

)


if (
    final_bridge_transaction_ids
    !=
    expected_transaction_ids
):

    raise ValueError(
        "Final bridge transaction IDs do not match "
        "the validated mapped transaction IDs."
    )


# --------------------------------------------------
# VALIDATE PATTERN COUNTS AFTER NORMALIZATION
# --------------------------------------------------

final_bridge_pattern_counts = (

    final_aml_pattern_transactions_df

    .groupby("aml_pattern_id")

    .size()

    .rename("bridge_transaction_count")

)


final_pattern_count_validation = (

    final_aml_patterns_df

    .set_index("aml_pattern_id")

    ["transaction_count"]

    .to_frame()

    .join(
        final_bridge_pattern_counts,
        how="left"
    )

)


final_pattern_count_validation[
    "bridge_transaction_count"
] = (

    final_pattern_count_validation[
        "bridge_transaction_count"
    ]

    .fillna(0)

    .astype("int64")

)


final_pattern_count_mismatches = (

    final_pattern_count_validation[
        "transaction_count"
    ]

    !=

    final_pattern_count_validation[
        "bridge_transaction_count"
    ]

).sum()


if final_pattern_count_mismatches > 0:

    raise ValueError(
        f"{final_pattern_count_mismatches:,} AML patterns "
        "have incorrect bridge transaction counts."
    )


# --------------------------------------------------
# SAVE CLEANED AML TABLES
# --------------------------------------------------

CLEANED_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


final_aml_patterns_df.to_csv(

    AML_PATTERNS_OUTPUT_FILE,

    index=False

)


final_aml_pattern_transactions_df.to_csv(

    AML_PATTERN_TRANSACTIONS_OUTPUT_FILE,

    index=False

)


# --------------------------------------------------
# VERIFY OUTPUT FILES
# --------------------------------------------------

if not AML_PATTERNS_OUTPUT_FILE.exists():

    raise FileNotFoundError(
        "aml_patterns.csv was not created."
    )


if not AML_PATTERN_TRANSACTIONS_OUTPUT_FILE.exists():

    raise FileNotFoundError(
        "aml_pattern_transactions.csv was not created."
    )


# --------------------------------------------------
# PRINT FINAL RESULTS
# --------------------------------------------------

print("\nAll final normalized AML output validations passed successfully.")


print("\nCleaned AML Files Created:")

print(
    f"  - {AML_PATTERNS_OUTPUT_FILE}"
)

print(
    f"  - {AML_PATTERN_TRANSACTIONS_OUTPUT_FILE}"
)


print("\nFinal AML Row Counts:")

print(
    f"  AML Patterns             : "
    f"{len(final_aml_patterns_df):,}"
)

print(
    f"  AML Pattern Transactions : "
    f"{len(final_aml_pattern_transactions_df):,}"
)


print("\nFinal AML Pattern Columns:")

for column in final_aml_patterns_df.columns:

    print(f"  - {column}")


print("\nFinal AML Pattern Transaction Columns:")

for column in final_aml_pattern_transactions_df.columns:

    print(f"  - {column}")


print("\nFirst 10 Final AML Pattern Records:")

print(
    final_aml_patterns_df.head(10)
)


print("\nFirst 10 Final AML Pattern Transaction Records:")

print(
    final_aml_pattern_transactions_df.head(10)
)


print("\n" + "=" * 70)

print(
    "STEP 3: CLEAN PATTERNS DATASET "
    "COMPLETED SUCCESSFULLY."
)

print("=" * 70)



