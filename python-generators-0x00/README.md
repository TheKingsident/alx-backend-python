## Project File Overview

- **0-main.py**: Main script to create the database, table, and insert data from CSV using the functions in `seed.py`.
- **seed.py**: Contains functions to connect to MySQL, create the database/table, and insert CSV data into the table.
- **user_data.csv**: Sample CSV file with user data (name, email, age) used for populating the database.
- **0-stream_users.py**: Defines a generator function to stream user data from the MySQL database.
- **1-main.py**: Script that imports and uses the `stream_users` generator to print the first few user records from the database.