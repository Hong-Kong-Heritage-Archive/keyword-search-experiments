# What is this

This is a project for evaluating full text search across different databases.

It contains the following
* Sample data books.csv and simplified.csv
* There are scripts to run the databases e.g. test_sqlite.sh and test_postgres.sh.
* And output after running the script:  postgres_out.txt and sqlite_out.txt

Refer to

| Database | Notes | Script | Output |
| -------- | -------- | -------- | -------- |
| SQLITE    | [01-sqlite/sqlite.md](01-sqlite/sqlite.md)    | [01-sqlite/test_sqlite.sh](01-sqlite/test_sqlite.sh)   | [01-sqlite/sqlite_out.txt](01-sqlite/sqlite_out.txt)  |
| Postgres FTS (EN books)  | [02-postgres-fts/postgre.md](02-postgres-fts/postgre.md)  | [02-postgres-fts/test_postgres.sh](02-postgres-fts/test_postgres.sh)   | [02-postgres-fts/postgres_out.txt](02-postgres-fts/postgres_out.txt) |
| Postgres trgm (EN books) | [03-postgres-trgm/postgre.md](03-postgres-trgm/postgre.md)  | [03-postgres-trgm/test_postgres_trgm.py](03-postgres-trgm/test_postgres_trgm.py)   | [03-postgres-trgm/stdout.txt](03-postgres-trgm/stdout.txt) |
| Postgres bigm (CN books) | [04-postgres-bigm/notes.md](04-postgres-bigm/notes.md) | [04-postgres-bigm/bigm_search.py](04-postgres-bigm/bigm_search.py) | [04-postgres-bigm/notes.md](04-postgres-bigm/notes.md) |  
| Postgres trgm (CN books) | [05-postgres-trgm-cn/postgre.md](05-postgres-trgm-cn/postgre.md)  | [05-postgres-trgm-cn/test_postgres_trgm.py](05-postgres-trgm-cn/test_postgres_trgm.py)   | [05-postgres-trgm-cn/stdout.txt](05-postgres-trgm-cn/stdout.txt) |
| Postgres bigm (EN books) | [06-postgres-bigm-en/notes.md](06-postgres-bigm-en/notes.md) | [06-postgres-bigm-en/bigm_search.py](06-postgres-bigm-en/bigm_search.py) | [06-postgres-bigm-en/notes.md](06-postgres-bigm-en/notes.md) |  
| Postgres JSON | [07-postgres-json/jsonb.md](07-postgres-json/jsonb.md) | [07-postgres-json/test_postgres.sh](07-postgres-json/test_postgres.sh) | [07-postgres-json/stdout.txt](07-postgres-json/stdout.txt) |


# Online Suggestions for searching Chinese book titles

https://github.com/pgbigm/pg_bigm

https://github.com/amutu/zhparser 

