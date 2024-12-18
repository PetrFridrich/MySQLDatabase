# MySQL databse

This small project demonstrates how to set up and manage a MySQL database using Docker and Python. It serves as an example for testing Docker Compose with a MySQL service and performing basic data processing, querying, and visualization tasks. It's a practical resource for learning and experimenting with database operations.

## Features

- Simple Data Cleaning:
  Process raw book data (google_books_dataset.csv) into a cleaner format for demonstration purposes.

- Easy MySQL Setup:
  Set up a MySQL database quickly using Docker Compose and load sample data with a Python script (`__main__.py`).

- Basic Entity-Relationship Diagram (ERD):
  A simple ERD is included to illustrate the database structure and relationships.

- Predefined SQL Queries and Visualizations:
  Run example SQL queries and generate basic visualizations using the `simple_Q_&_V.ipynb` notebook.

- Modular Project Structure:
  Clear folder organization to help you understand each step, from raw data to database setup and querying.

- Docker Integration:
  A straightforward Docker Compose setup makes it easy to start and stop the MySQL service for testing.

## Dataset

### Source  
This project uses the [Google Books Dataset](https://www.kaggle.com/datasets/bilalyussef/google-books-dataset) provided by Bilal Youssef on Kaggle.  
©2019 Google. All rights reserved.

### Usage  
The dataset is used strictly for educational and non-commercial purposes. For licensing details and terms of use, please refer to the [Kaggle dataset page](https://www.kaggle.com/datasets/bilalyussef/google-books-dataset).

### Disclaimer  
This dataset is owned by Google, and I do not claim any ownership or rights over it.

## Installation

**Prerequisite:** Ensure [Poetry](https://python-poetry.org/docs/#installation) is installed on your system, and [Docker](https://www.docker.com/get-started) is running.

1. Clone the repository:
   ```bash
   git clone https://github.com/PetrFridrich/MySQLDatabase.git
   ```
2.  Navigate to the project directory:
    ```bash
    cd MySQLDatabase
    ```
3. Install the dependencies with Poetry:
    ```bash 
    poetry install
    ```
This will install all required dependencies as defined in pyproject.toml.

4. Set up the MySQL service using Docker Compose:
    + Ensure Docker is running on your system.
    + Start the MySQL service with Docker Compose:
    ```bash 
    docker-compose up -d
    ```
    This command will start the MySQL container in the background.

## Usage

Once you’ve installed the dependencies and set up MySQL, follow these steps to use the project:

+ **Data Cleaning:**  
  If the `clean_data` folder is missing, run `data_cleaning.ipynb` to process `google_books_dataset.csv` and create `books.csv`.

+ **Database Setup:**  
  Run `__main__.py` to set up the MySQL database and load the cleaned data.

+ **SQL Queries and Visualizations:**  
  Open `simple_Q_&_V.ipynb` to execute queries and visualize the data.

## Project Structure

The project is organized as follows:

<pre>
MySQLDatabse/
├── data/                                  # Folder containing datasets
│   ├── clean_data/                            # Folder with cleaned and processed data
│   │   └── books.csv                              # Cleaned dataset containing book details
│   └── raw_data/                              # Folder containing raw, unprocessed data
│       └── google_books_dataset.csv               # Raw dataset from Google Books
├── docs/                                  # Documentation folder
│   ├── ERD.pdf                                # Entity-Relationship Diagram (ERD) in PDF format
│   └── ERD.txt                                # Entity-Relationship Diagram (ERD) in text format
├── src/                                   # # Folder with source codes
│   ├── data_cleaning/                         # Folder for data cleaning notebook
│   │   └── data_cleaning.ipynb                    # Jupyter notebook for data cleaning processes
│   ├── setup_database/                        # Folder for database setup scripts
│   │   └── db_setup.py                            # Python script to initialize and set up the MySQL database
│   ├── simple_queries_and_visualization/      # Folder for simple SQL queries and data visualization scripts
│   │   └── simple_Q_&_V.ipynb                     # Jupyter notebook for running queries and visualizing results
│   └── __main__.py                            # Main script
├── .gitignore                             # Git ignore file
├── docker-compose.yml                     # Docker Compose file for setting up MySQL service
├── LICENSE                                # License file for the project
├── pyproject.toml                         # Poetry project configuration and dependencies
├── poetry.lock                            # Poetry lock file to ensure consistent dependencies
└── README.md                              # This README file
</pre>

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.  
⚠️ **Note:** The dataset is ©2019 Google and is not covered by this license. It must be downloaded separately from Kaggle.

