from pyiceberg.catalog.sql import SqlCatalog
import pyarrow as pa
from datetime import datetime

catalog = SqlCatalog(
    "local",
    uri="sqlite:///catalog.db",
    warehouse="C:/Users/jingl/DE2/iceberg-practice/warehouse",
)

table = catalog.load_table("demo.my_table")

more_data = pa.table({
    "id": [4, 5],
    "name": ["Bob", "Alice"],
    "created_at": [datetime.now(), datetime.now()],
    "email": ["bob@test.com", "alice@test.com"],
})

table.append(more_data)

