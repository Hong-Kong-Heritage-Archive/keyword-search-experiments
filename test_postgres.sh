#
# Assumes you have installed postgres in docker and have the psql client installed on your machine. 
#

sudo docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres

until sudo docker exec some-postgres pg_isready -h localhost -U postgres; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done

PGPASSWORD=mysecretpassword psql -e -h localhost -p 5432 -U postgres <<EOF

\echo

\echo === Create Books table ===
\echo

create table books ( isbn text, title text );
CREATE INDEX title_index ON books (title);
CREATE INDEX title_index_gin ON books USING GIN ( to_tsvector('english', title) );

\echo
\echo === Import data ===
\echo

\copy books FROM 'simplified.csv' WITH (FORMAT csv, HEADER true);

select * from books LIMIT 5;

\echo
\echo === Select books by title ===
\echo

EXPLAIN select * from books WHERE title = 'The Great Gatsby';
select * from books WHERE title = 'The Great Gatsby';

\echo
\echo === Select books by keyword (Sequential Scan) ===
\echo

EXPLAIN select * from books WHERE title LIKE '%Potter%';

select * from books WHERE title LIKE '%Potter%';


\echo
\echo === Select books by keyword (Full text search) ===
\echo

EXPLAIN select * from books WHERE to_tsvector('english', title) @@ to_tsquery('english', 'Potter & Harry');

\echo
\echo === Select books by keyword (Full text search 2) ===
\echo

EXPLAIN select * from books WHERE to_tsvector('english', title) @@ phraseto_tsquery('english', 'Harry Potter');

select * from books WHERE to_tsvector('english', title) @@ phraseto_tsquery('english', 'Harry Potter');


EOF

sudo docker stop some-postgres
sudo docker rm some-postgres
sudo docker ps -a

