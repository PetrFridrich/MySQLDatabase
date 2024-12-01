import ast
import pandas as pd

from pathlib import Path
from dotenv import dotenv_values

import mysql.connector

ENV_PATH = Path('./.env')
INIT_DATA_PATH = Path('./data/clean_data/books.csv')

if not INIT_DATA_PATH.exists():
    raise FileNotFoundError(f"Error: The file '{INIT_DATA_PATH}' does not exist!\nRun data_cleaning.ipynb file first!")


def get_connection():
    
    config = dotenv_values(ENV_PATH)

    if 'MYSQL_USER' not in config or 'MYSQL_PASSWORD' not in config:
        raise KeyError("Environment variables are missing.")

    try:
        connection = mysql.connector.connect(host='localhost',
                                             port=3306,
                                             user=config['MYSQL_USER'],
                                             password=config['MYSQL_PASSWORD'])
        
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['MYSQL_DATABASE']}")
        cursor.execute(f"USE {config['MYSQL_DATABASE']}")
        cursor.close()
        
        if connection.is_connected():
            print('Connection successful!')

    except mysql.connector.Error as err:
        print(f'Error: {err}')
        return None

    return connection


def create_tables(connection):
    
    try:
        cursor = connection.cursor()
        
        # SQL Queries for table creation        
        table_books = """
            CREATE TABLE IF NOT EXISTS Books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                language_id INT,
                maturityRating VARCHAR(50),
                publisher_id INT,
                publishedDate DATE,
                pageCount INT
            );
        """

        table_authors = """
            CREATE TABLE IF NOT EXISTS Authors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            );
        """
        
        table_languages = """
            CREATE TABLE IF NOT EXISTS Languages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                language VARCHAR(100) NOT NULL
            );
        """

        table_categories = """
            CREATE TABLE IF NOT EXISTS Categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(100) NOT NULL
            );
        """

        table_publishers = """
            CREATE TABLE IF NOT EXISTS Publishers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            );
        """

        table_books_authors = """
            CREATE TABLE IF NOT EXISTS Books_Authors (
                book_id INT,
                author_id INT,
                PRIMARY KEY (book_id, author_id),
                FOREIGN KEY (book_id) REFERENCES Books(id),
                FOREIGN KEY (author_id) REFERENCES Authors(id)
            );
        """

        table_books_categories = """
            CREATE TABLE IF NOT EXISTS Books_Categories (
                book_id INT,
                category_id INT,
                PRIMARY KEY (book_id, category_id),
                FOREIGN KEY (book_id) REFERENCES Books(id),
                FOREIGN KEY (category_id) REFERENCES Categories(id)
            );
        """

        add_fk_books_language = """
            ALTER TABLE Books
            ADD CONSTRAINT fk_language
            FOREIGN KEY (language_id) REFERENCES Languages(id);
        """

        add_fk_books_publisher = """
            ALTER TABLE Books
            ADD CONSTRAINT fk_publisher
            FOREIGN KEY (publisher_id) REFERENCES Publishers(id);
        """
        
        # List of all queries
        all_queries = [
            table_books,
            table_authors,
            table_languages,
            table_categories,
            table_publishers,
            table_books_authors,
            table_books_categories,
            add_fk_books_language,
            add_fk_books_publisher
        ]
        
        # Start a transaction to ensure atomicity
        connection.start_transaction()

        # Execute each query
        for query in all_queries:
            cursor.execute(query)

        # Commit the transaction
        connection.commit()

        print("Tables created successfully!")
    
    except mysql.connector.Error as err:
        # Handle errors (e.g., log it or print the error message)
        print(f"Error: {err}")
        connection.rollback()  # Rollback in case of error

    finally:
        # Ensure the cursor is closed
        cursor.close()

    return None


def insert_data_to_db(connection):

    cursor = connection.cursor()

    chunksize = 1000

    for chunk in pd.read_csv(INIT_DATA_PATH, chunksize=chunksize):

        for index, row in chunk.iterrows():
            try:
                # Extracting data from the DataFrame row
                title = row['title']
                authors = row['authors']
                language = row['language']
                categories = row['categories']
                maturity_rating = row['maturityRating']
                publisher = row['publisher']
                published_date = row['publishedDate']
                page_count = row['pageCount']

                # 1. Insert language if not exists
                language_id = insert_language(connection, cursor, language)

                # 2. Insert publisher if not exists
                publisher_id = insert_publisher(connection, cursor, publisher)

                # Commit
                connection.commit()

                # 3. Insert the book into the Books table
                book_id = insert_book(connection, cursor, title, 
                                      language_id, maturity_rating, 
                                      publisher_id, published_date, 
                                      page_count)
                
                # 4. Insert authors if not exists and link to the book
                insert_books_authors(connection, cursor, book_id, authors)

                # 5. Insert categories if not exists and link to the book
                insert_books_categories(connection, cursor, book_id, categories)

            except mysql.connector.Error as err:
                print(f"Error while inserting row {index}: {err}")
                connection.rollback()  # Rollback if something goes wrong

    cursor.close()

    return None


def insert_language(connection, cursor, language):

    # Insert language if not exists
    cursor.execute("SELECT id FROM Languages WHERE LOWER(language) = LOWER(%s)", (language,))
    language_id = cursor.fetchone()

    if language_id is None:
        cursor.execute("INSERT INTO Languages (language) VALUES (%s)", (language,))
        connection.commit()  # Commit after inserting
        language_id = cursor.lastrowid
    
    else:
        language_id = language_id[0]


    return language_id


def insert_publisher(connection, cursor, publisher):

    # Insert publisher if not exists
    cursor.execute("SELECT id FROM Publishers WHERE LOWER(name) = LOWER(%s)", (publisher,))
    publisher_id = cursor.fetchone()

    if publisher_id is None:
        cursor.execute("INSERT INTO Publishers (name) VALUES (%s)", (publisher,))
        connection.commit()  # Commit after inserting
        publisher_id = cursor.lastrowid
    
    else:
        publisher_id = publisher_id[0]

    return publisher_id


def insert_book(connection, cursor, title, language_id, maturity_rating, publisher_id, published_date, page_count):
    
    # Insert the book into the Books table

    # Define the SQL query as a variable
    query = """
        INSERT INTO Books (title, language_id, maturityRating, publisher_id, publishedDate, pageCount)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    # Execute the query with parameters
    cursor.execute(query, (title, language_id, maturity_rating, publisher_id, published_date, page_count))

    connection.commit()
    book_id = cursor.lastrowid  # Get the id of the inserted book

    return book_id


def insert_books_authors(connection, cursor, book_id, authors):

    # Insert authors if not exists and link to the book
    authors_to_insert = []  # Collect authors to insert into the Books_Authors table

    for author in ast.literal_eval(authors):

        cursor.execute("SELECT id FROM Authors WHERE LOWER(name) = LOWER(%s)", (author,))
        author_id = cursor.fetchone()

        if author_id is None:
            cursor.execute("INSERT INTO Authors (name) VALUES (%s)", (author,))
            author_id = cursor.lastrowid  # Get the ID of the newly inserted author
        else:
            author_id = author_id[0]

        # Prepare for Books_Authors insert
        authors_to_insert.append((book_id, author_id))

    # Insert into Books_Authors once after the loop
    cursor.executemany("""INSERT INTO Books_Authors (book_id, author_id) VALUES (%s, %s)""", authors_to_insert)

    # Commit once after all operations for this book
    connection.commit()

    return None


def insert_books_categories(connection, cursor, book_id, categories):
    
    # Collect category insertions for batch processing
    categories_to_insert = []

    for category in ast.literal_eval(categories):
        
        # Check if the category already exists
        cursor.execute("SELECT id FROM Categories WHERE LOWER(category) = LOWER(%s)", (category,))
        category_id = cursor.fetchone()

        if category_id is None:
            cursor.execute("INSERT INTO Categories (category) VALUES (%s)", (category,))
            category_id = cursor.lastrowid  # Get the ID of the newly inserted category
        else:
            category_id = category_id[0]
        
        # Prepare data for batch insert
        categories_to_insert.append((book_id, category_id))

    # Batch insert into Books_Categories
    cursor.executemany("""INSERT INTO Books_Categories (book_id, category_id) VALUES (%s, %s)""",categories_to_insert)

    # Commit once after all operations for this book
    connection.commit()

    return None


def INIT_DB():

    try:
        # Establish database connection
        connection = get_connection()

        # Create tables in the database
        create_tables(connection)

        # Insert data into the database
        insert_data_to_db(connection)

    except KeyError as e:
        print(f"Configuration error: {e}")

    except mysql.connector.Error as e:
        print(f"Database error: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        if connection is not None:
            # Closing database connection
            connection.close()

    return None


if __name__ == '__main__':

    print('Hello, home!')