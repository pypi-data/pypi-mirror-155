# Kongodb

**Kongodb** is Hybrid Row-and-Document Oriented datastore leveraging SQL/RDBMS database: SQLite, MySQL, MariaDB, Postgresql 

Kongodb is both RDMBS + Document Oriented together.

It supports, regular SQL query along with Document Oriented and Key Value store.

Engine:
- JSON
- SQLite
- Mariadb
- PostgreSQL
- MySQL



### Install

```python 
pip install kongodb
```

### Usage


```python
from kongodb import kongodb

# Open the db
db = kongodb("./my.db") 

# Select a container 
# Container will be created automatically
container = db.container("test")

# Get total items
print(len(container))

# Insert an item. It returns kongodb#Item
item = conatiner.add({
  "name": "Fun",
  "type": "DB",
  "version": "1.0.0"
})

# Retrieve item by _id
_id = "9c5e5fbd05544700995c5fa3ca3ef214"
entry = container.get(_id)

# Access properties
entry.name # -> fun 
entry.type # -> DB
entry.version # -> 1.0.0

# Update a field
entry.update(version="1.0.1")
# ...or 
entry.update({"version": "1.0.1"})
# ... or
entry.set("version", "1.0.1")
#
entry.version # -> 1.0.1

# Delete entry
entry.delete()

# Search
for entry in container.find():
  print(entry.name)


```

## ~ API ~

## Database

### kongodb

### #select

To select a collection in the database

```python
fun = kongodb()

users = fun.select("users")

## or 

users = fun.users
```


### #Container

List all the collections in the database 

```python
fun = kongodb()

users = fun.select("users")

## or 

users = fun.users
```

##D


