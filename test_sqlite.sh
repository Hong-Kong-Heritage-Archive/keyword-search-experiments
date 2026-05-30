

echo === Import books.csv ===

rm test.db
sqlite3 test.db <<EOF
.import --csv books.csv books

.mode column
select isbn,title from books LIMIT 5;
create index idx_title on books(title);

EOF

echo ...
echo

echo === Full title search ===

sqlite3 test.db <<EOF
.mode column

EXPLAIN QUERY PLAN select isbn,title from books where title = 'The Great Gatsby';
select isbn,title from books where title = 'The Great Gatsby';
EOF

echo


echo === Like searches ===

echo "Harry and Prince"

sqlite3 test.db <<EOF
.mode column

EXPLAIN QUERY PLAN select isbn,title from books where title LIKE '%Harry%' and title LIKE '%Prince%';
select isbn,title from books where title LIKE '%Harry%' and title LIKE '%Prince%';
EOF

echo

echo === Create FTS Indexes ===

sqlite3 test.db <<EOF
.mode column
CREATE VIRTUAL TABLE book_fts USING fts5(isbn, title);
insert into book_fts select isbn, title from books;
EOF

echo ...
echo

echo === Perform full text search ===

echo "Harry and Prince"

sqlite3 test.db <<EOF
.mode column

EXPLAIN QUERY PLAN select * from book_fts where title MATCH 'Harry' and title MATCH 'Prince';

select * from book_fts where title MATCH 'Harry' and title MATCH 'Prince';
EOF