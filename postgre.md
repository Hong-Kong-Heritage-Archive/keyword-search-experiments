# Installation


## Install docker

```
sudo snap install docker
```

## Reference

https://hub.docker.com/_/postgres

## Using Postgresql

Start and run postgre. Use sudo if required.

```
$ docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
```

Check running process
```
$ sudo docker ps -a
CONTAINER ID   IMAGE      COMMAND                  CREATED              STATUS              PORTS                                         NAMES
db225a0f7fc9   postgres   "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp   some-postgres
```

After you are done
```
$ docker stop some-postgres
```

Clear all running
```
$ sudo docker container prune
```


## Connecting to the database

Run inside docker
```
$ docker exec -it some-postgres psql -U postgres
```

Connect to docker locally. ( Assuming you have psql installed )
```
$ sudo apt install postgresql-client
$ psql -h localhost -p 5432 -U postgres
```

# Import data

```
$ PGPASSWORD=mysecretpassword psql -h localhost -p 5432 -U postgres

postgres=# create table books ( isbn text, title text );
CREATE TABLE

postgres=# \copy books FROM 'simplified.csv' WITH (FORMAT csv, HEADER true);
COPY 98

postgres=# select * from books LIMIT 5;
   isbn    |                          title                           
-----------+----------------------------------------------------------
 439554934 | Harry Potter and the Sorcerer's Stone (Harry Potter, #1)
 316015849 | Twilight (Twilight, #1)
 61120081  | To Kill a Mockingbird
 743273567 | The Great Gatsby
 525478817 | The Fault in Our Stars
(5 rows)
```

# Start creating full text search



