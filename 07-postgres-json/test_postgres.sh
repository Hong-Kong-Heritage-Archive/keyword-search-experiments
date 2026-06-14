#
# Assumes you have installed postgres in docker and have the psql client installed on your machine. 
#

sudo docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres

until sudo docker exec some-postgres pg_isready -h localhost -U postgres; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done

PGPASSWORD=mysecretpassword psql -e -h localhost -p 5432 -U postgres <<EOF

CREATE TABLE books (
    data jsonb
);

\set ECHO none

-- Use sed to escape single quotes and expand the JSON array into multiple rows
INSERT INTO books (data) 
SELECT jsonb_array_elements(CAST('$(sed "s/'/''/g" books.json)' AS jsonb));

\set ECHO all

-- Enable the trigram extension
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Create a GIN index using gin_trgm_ops on the 'title' field extracted from the JSONB data
CREATE INDEX idx_books_title_trgm ON books USING gin ((data->>'title') gin_trgm_ops);

-- Count books
SELECT COUNT(*) FROM books;

-- Perform a similarity search using the % operator.
-- Added parentheses around (data->>'title') to fix operator precedence issues.
EXPLAIN SELECT *, similarity((data->>'title'), 'Harry Potter') AS score 
FROM books 
WHERE (data->>'title') % 'Harry Potter'
ORDER BY score DESC;


-- Perform a similarity search using the % operator.
-- Added parentheses around (data->>'title') to fix operator precedence issues.
SELECT data->>'title' as TITLE, similarity((data->>'title'), 'Harry Potter') AS score 
FROM books 
WHERE (data->>'title') % 'Harry Potter'
ORDER BY score DESC;

EOF

sudo docker stop some-postgres
sudo docker rm some-postgres
sudo docker ps -a