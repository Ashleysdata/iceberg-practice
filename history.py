

from pyiceberg.catalog.sql import SqlCatalog

catalog = SqlCatalog(
    "local",
    uri="sqlite:///catalog.db",
    warehouse="C:/Users/jingl/DE2/iceberg-practice/warehouse",
)

table = catalog.load_table("demo.my_table")

for snap in table.history():
    print(snap)