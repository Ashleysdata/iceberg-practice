from pyiceberg.catalog.sql import SqlCatalog
import pyarrow as pa
from datetime import datetime

catalog = SqlCatalog(
    "local",
    uri="sqlite:///catalog.db",
    warehouse="C:/Users/jingl/DE2/iceberg-practice/warehouse",
)

table = catalog.load_table("demo.my_table")

data = pa.table({
    "id": [1, 2, 3],
    "name": ["Jing", "Ashley", "Test"],
    "created_at": [datetime.now(), datetime.now(), datetime.now()],
})

table.append(data)
print(table.scan().to_arrow())