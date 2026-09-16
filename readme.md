# Apache Iceberg Local Practice

A hands-on local practice project exploring core Apache Iceberg concepts using `pyiceberg`, `pyarrow`, and `DuckDB` — no cluster, no cloud, everything runs on a laptop.

## What this project demonstrates

Apache Iceberg is an open table format that sits on top of plain Parquet files, adding database-like guarantees (ACID transactions, schema evolution, time travel) without requiring a traditional data warehouse. This project walks through the core mechanics hands-on:

1. **Catalog setup** — a local SQLite-backed Iceberg catalog (`pyiceberg.catalog.sql.SqlCatalog`)
2. **Table creation** — defining a schema and creating an Iceberg table
3. **Data ingestion & snapshots** — appending data and observing how each write creates a new immutable snapshot
4. **Cross-engine interoperability** — reading the same Iceberg table with DuckDB, without DuckDB knowing anything about how the data was written
5. **Schema evolution** — adding a new column without rewriting any existing data files
6. **Time travel** — querying a historical snapshot to see the table exactly as it looked before a change, schema included

## Tech stack

- **pyiceberg** — table creation, catalog management, writes, schema evolution
- **pyarrow** — in-memory columnar data representation
- **DuckDB** — SQL querying engine, demonstrating multi-engine access to the same Iceberg table
- **SQLite** — lightweight local catalog backend

## Project structure

```
iceberg-practice/
├── setup_catalog.py      # Initializes the local SQLite catalog and namespace
├── create_table.py       # Defines schema and creates the Iceberg table
├── insert_data.py        # Appends data, producing a new snapshot
├── insert_more.py        # Appends a second batch, producing a second snapshot
├── query.py               # Reads the table via DuckDB's iceberg_scan()
├── evolve_schema.py       # Adds a new column via schema evolution
├── history.py              # Lists all snapshots for the table
└── .gitignore
```

## Key concepts illustrated

**Snapshots are immutable.** Every `append()` call creates a new snapshot rather than modifying existing data — this is what makes time travel possible.

**Schema evolution doesn't rewrite data.** Adding the `email` column via `update_schema()` didn't touch a single existing Parquet file. Old rows simply return `NULL` for the new field; the change is purely a metadata operation.

**Time travel preserves schema history too.** Querying an older snapshot didn't just return the data as it was — it returned the *schema* as it was, before the `email` column existed. Iceberg tracks schema versioning alongside data versioning.

**Multi-engine interoperability is real.** DuckDB read the table written by pyiceberg with zero coordination between the two tools — both simply understand the same open metadata format.

## A note on Windows path handling

This project was built and debugged on Windows, which surfaced a real interoperability issue: `pyiceberg`'s `PyArrowFileIO` and DuckDB's `iceberg_scan()` don't handle Windows `file://` URIs consistently. The working configuration that resolved it:

- **pyiceberg catalog config**: uses a plain absolute Windows path for `warehouse` (no `file://` prefix) — e.g. `"C:/Users/.../warehouse"`
- **DuckDB query**: uses an absolute POSIX-style path (via `pathlib.Path.resolve().as_posix()`), plus `SET unsafe_enable_version_guessing = true;` to allow version auto-detection

This is a Windows-local-development quirk, not something you'd typically encounter in production (which usually runs on Linux servers or cloud object storage with globally-unique paths like S3 URIs).

## Setup

```powershell
python -m venv venv
venv\Scripts\activate
pip install pyiceberg[sql-sqlite,pyarrow] duckdb pyarrow
```

Then run the scripts in order:

```powershell
python setup_catalog.py
python create_table.py
python insert_data.py
python query.py
python evolve_schema.py
python query.py
python insert_more.py
python history.py
python query.py
```

## Why this project

Built as part of a broader effort to build hands-on familiarity with the modern open lakehouse stack (Iceberg is now the dominant open table format for new lakehouse deployments) alongside an existing toolset of Snowflake, Databricks, dbt, and Microsoft Fabric.
