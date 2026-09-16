from pathlib import Path
import duckdb

warehouse_path = Path("warehouse").resolve().as_posix()

con = duckdb.connect()
con.sql("INSTALL iceberg; LOAD iceberg;")
con.sql("SET unsafe_enable_version_guessing = true;")
con.sql(f"SELECT * FROM iceberg_scan('{warehouse_path}/demo/my_table')").show()

print("updated_data：")
con.sql(f"SELECT * FROM iceberg_scan('{warehouse_path}/demo/my_table')").show()

print("first_snapshot：")
con.sql(f"""
    SELECT * FROM iceberg_scan(
        '{warehouse_path}/demo/my_table',
        snapshot_from_id = 6462316467855310278
    )
""").show()