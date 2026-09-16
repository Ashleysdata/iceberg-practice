

from pyiceberg.catalog.sql import SqlCatalog
from pyiceberg.types import StringType

catalog = SqlCatalog(
    "local",
    uri="sqlite:///catalog.db",
    warehouse="C:/Users/jingl/DE2/iceberg-practice/warehouse",
)

table = catalog.load_table("demo.my_table")

with table.update_schema() as update:
    update.add_column("email", field_type=StringType())

print(table.schema())