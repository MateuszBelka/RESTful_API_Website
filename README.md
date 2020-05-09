# Install sqlite, express and body-parser modules

```bash
$ npm install sqlite express body-parser
```

# Running the server

You can start the server by executing the Python script:
```
$ python server.py
```

This starts a server at http://localhost:8080/ (Links to an external site.)

You can verify this with a browser or a REST client such as `Postman`.

Your server restarts automatically every time you save the file `server.py` (because the Bottle reloader is enabled).


# Accessing the database

The server will automatically create an SQLite database table 'supermarket' in the file `inventory.db`.
This file is re-created whenever you delete it. The code in server.py shows how you can access this database by adding a parameter `db` to the function in which you need it. The plugin will provide you a database cursor (Links to an external site.). This works in all functions with a routing decorator (Links to an external site.) (e.g. `@route()`, `@get()`, `@post()`, etc.). Using this cursor, you can execute SQL queries and retrieve results.
