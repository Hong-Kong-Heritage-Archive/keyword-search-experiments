#!/usr/bin/python3

import psycopg2
import csv
import argparse
import sys

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Search for books in a PostgreSQL database using pg_bigm.")
    
    # Database Configuration Arguments
    parser.add_argument("--host", required=True, help="PostgreSQL host IP address")
    parser.add_argument("--db", required=True, help="Database name")
    parser.add_argument("--user", required=True, help="Database user account")
    parser.add_argument("--password", required=True, help="Database password")
    parser.add_argument("--port", default="5432", help="Database port (default: 5432)")
    
    # File and Search Arguments
    parser.add_argument("--csv", required=True, help="Path to the CSV file containing book data")
    parser.add_argument("--search", required=True, help="The string to search for in titles")

    args = parser.parse_args()

    # Construct DB Config from arguments
    db_config = {
        "host": args.host,
        "database": args.db,
        "user": args.user,
        "password": args.password,
        "port": args.port,
        "sslmode": "require"
    }

    conn = None
    try:
        # 1. Connect to the PostgreSQL instance
        print(f"Connecting to {args.host}:{args.port}...")
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Ensure pg_bigm extension is available
        cur.execute("CREATE EXTENSION IF NOT EXISTS pg_bigm;")
        print("Extension 'pg_bigm' ensured.")

        # 2. Create the books table if it does not exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                isbn TEXT,
                title TEXT
            );
        """)
        print("Table 'books' ensured.")

        # Create GIN index on title using pg_bigm operator class
        cur.execute("CREATE INDEX IF NOT EXISTS idx_books_title ON books USING gin (title gin_bigm_ops);")
        print("GIN index on 'title' ensured.")

        # 3. Import CSV file
        with open(args.csv, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute(
                    "INSERT INTO books (isbn, title) VALUES (%s, %s)",
                    (row['isbn'], row['title'])
                )
        print(f"Data imported from {args.csv}.")

        # Set similarity socre to minimum to see all matches
        print(f"\n--- Set Similarity Limit ---")
        cur.execute("SET pg_bigm.similarity_limit TO 0.01;")

        # 4. Search using pg_bigm
        # The ~* operator is used for bigm matching (case-insensitive)
        print(f"\n--- Execution Plan ---")
        cur.execute("EXPLAIN SELECT bigm_similarity( title, %s ), isbn, title FROM books WHERE title =%% %s", (args.search,args.search))
        plan = cur.fetchall()
        for line in plan:
            print(line[0])

        print(f"\n--- Search Results ---")
        print(f"Searching for titles matching: '{args.search}'...")
        cur.execute("SELECT bigm_similarity( title, %s ), isbn, title FROM books WHERE title =%% %s", (args.search,args.search))
        results = cur.fetchall()

        if results:
            for row in results:
                print(f"Score: {row[0]} - Found: ISBN {row[1]} - Title: {row[2]}")
        else:
            print("No matches found.")

        # 5. Delete the table
        cur.execute("DROP TABLE books;")
        conn.commit()
        print("\nTable 'books' deleted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Connection closed.")

if __name__ == "__main__":
    main()