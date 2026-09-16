from pyiceberg.catalog.sql import SqlCatalog
import pyarrow as pa

catalog = SqlCatalog(
    "local",
    uri="sqlite:///catalog.db",
    warehouse="C:/Users/jingl/DE2/iceberg-practice/warehouse",
)

schema = pa.schema([
    ("id", pa.int64()),
    ("name", pa.string()),
    ("created_at", pa.timestamp("us")),
])

table = catalog.create_table("demo.my_table", schema=schema)
print(table)