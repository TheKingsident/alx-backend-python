## Project File Overview

- **0-main.py**: Main script to create the database, table, and insert data from CSV using the functions in `seed.py`.
- **seed.py**: Contains functions to connect to MySQL, create the database/table, and insert CSV data into the table.
- **user_data.csv**: Sample CSV file with user data (name, email, age) used for populating the database.
- **0-stream_users.py**: Defines a generator function to stream user data from the MySQL database.
- **1-main.py**: Script that imports and uses the `stream_users` generator to print the first few user records from the database.
- **1-batch_processing.py**: Contains generator functions to fetch user data in batches and filter users over age 25.
- **2-main.py**: Script that uses `batch_processing` to print users over age 25 in batches.
- **2-lazy_paginate.py**: Provides lazy pagination over user data, yielding pages of users from the database.
- **3-main.py**: Script that uses the lazy pagination generator to print users page by page.
- **4-stream_ages.py**: Streams user ages from the database and provides a function to calculate the average age.