
sqlite3 test.db <<EOF
.mode csv
select isbn,title from books;
EOF
