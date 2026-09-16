from pyiceberg.catalog.sql import SqlCatalog

catalog = SqlCatalog(
    "local",
    uri="sqlite:///catalog.db",
    warehouse="C:/Users/jingl/DE2/iceberg-practice/warehouse",
)
catalog.create_namespace("demo")
print(catalog.list_namespaces())
