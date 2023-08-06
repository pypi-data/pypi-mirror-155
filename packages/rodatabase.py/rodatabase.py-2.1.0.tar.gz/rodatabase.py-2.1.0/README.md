# Rodatabase.py

# How to install?

`pip install rodatabase.py`

# How to start using the Library?

```
from robase.imports import DatabaseClient

DB = DatabaseClient(universeId=YOUR_ID_HERE, token="YOUR_API_TOKEN_HERE", ROBLOSECURITY="YOUR_.ROBlOSECURITY_HERE")
```


# All functions

```
await DB.get_datastores()
Datastore = await DB.get_datastore("Test1")
await Datastore.get_keys(datastore="ExampleDatastore", limit=99)
await Datastore.set_data(datastore="ExampleDatastore", key="ExampleKey", data="ExampleData") 
await Datastore.increment_data(datastore="ExampleDatastore", key="ExampleKey", incrementby=1)
await Datastore.delete_data(datastore="ExampleDatastore", key="ExampleKey")
await Datastore.get_data(datastore="ExampleDatastore", key="ExampleKey")
```
For calling set_data data must be a JSON object.
```
All JSON objects:
    String
    Number
    JSON object
    Array
    Boolean
    null
```
