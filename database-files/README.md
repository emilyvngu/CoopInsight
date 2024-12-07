# `database-files` Folder

TODO: Put some notes here about how this works.  include how to re-bootstrap the db. 

The database-files folder contains SQL scripts that define and populate the CoopInsight database. These scripts are used to initialize the database structure and populate it with seed data for development and testing purposes.

# How to Re-Bootstrap the Database
1. Stop and Remove the Existing Database Container:
    ```
    docker compose down
    ```
2. Stop and Remove the Existing Database Container:
    ```
    docker compose up db
    ```
Note: If you need the entire application stack (frontend, backend, and database) running, then yes, you should run:
    ```
    docker compose up
    ```