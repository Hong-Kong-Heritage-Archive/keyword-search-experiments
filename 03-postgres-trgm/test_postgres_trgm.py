import psycopg2
import csv
import os
import traceback


def import_csv_to_postgres(csv_file, table_name='books'):
    # Database connection parameters - adjust these as needed
    db_params = {
        'host': 'localhost',
        'user': 'postgres',
        'password': 'mysecretpassword',
        'port': '5432'
    }

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Check if table exists, if not create it (only isbn and title)
        cursor.execute(f"""
        DO $$
        BEGIN
            DROP TABLE IF EXISTS {table_name};
            CREATE TABLE {table_name} (
                isbn VARCHAR(20) PRIMARY KEY,
                title TEXT NOT NULL
            );
        END $$;
        """)

        # Create pg_trgm extension and GIN index on title
        cursor.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_extension
                WHERE extname = 'pg_trgm'
            ) THEN
                CREATE EXTENSION pg_trgm;
            END IF;
        END $$;
        """)

        cursor.execute(f"""
        CREATE INDEX IF NOT EXISTS idx_{table_name}_title_gin
        ON {table_name} USING GIN (title gin_trgm_ops);
        """)

        # Create an index on the title column
        cursor.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_{table_name}_title
            ON {table_name}(title);
        """)

        # Read CSV file and insert data (only isbn and title)
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            # Prepare SQL query (only for isbn and title)
            columns = 'isbn, title'
            placeholders = ', '.join(['%s', '%s'])  # Explicitly for isbn and title
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            # Insert data in batches (only isbn and title)
            batch_size = 1000
            batch = []

            for row in reader:
                # Only append isbn and title to the batch
                batch.append([row['isbn'], row['title']])

                if len(batch) >= batch_size:
                    cursor.executemany(query, batch)
                    conn.commit()
                    batch = []

            # Insert remaining rows
            if batch:
                cursor.executemany(query, batch)
                conn.commit()

        # Count the number of books in the table
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        book_count = cursor.fetchone()[0]
        print(f"Successfully imported data from {csv_file} to {table_name} table")
        print(f"Total books in {table_name}: {book_count}")

    except Exception as e:
        traceback.print_exc()
        print(f"Error: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def search_similar_titles(query_term="Harry Potter"):
    db_params = {
        'host': 'localhost',
        'user': 'postgres',
        'password': 'mysecretpassword',
        'port': '5432'
    }

    print(f"Searching for titles similar to '{query_term}'...")

    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Use similarity() for fuzzy matching
        cursor.execute(f"""
        SELECT title, isbn, similarity(title, '{query_term}') AS similarity_score
        FROM books
        WHERE similarity(title, '{query_term}') > 0.3
        ORDER BY similarity(title, '{query_term}') DESC;
        """)

        results = cursor.fetchall()
        for title, isbn, similarity_score in results:
            print(f"Title: {title}, ISBN: {isbn}, Similarity: {similarity_score:.2f}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
    

if __name__ == "__main__":
    # Use one of your CSV files (e.g., 'books.csv')
    csv_filename = 'books.csv'
    if os.path.exists(csv_filename):
        import_csv_to_postgres(csv_filename)
    else:
        print(f"CSV file {csv_filename} not found. Please check the filename.")
    
    search_similar_titles("Harry Potter")
