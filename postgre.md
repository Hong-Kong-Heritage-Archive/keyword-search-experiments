# Install Docker

```
sudo snap install docker
```

# Reference:

https://hub.docker.com/_/postgres

# Using Postgresql

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

Stop
```
$ docker stop some-postgres
```

Clear all running
```
$ sudo docker container prune
```


# Connecting to the database

Run inside docker
```
$ docker exec -it some-postgres psql -U postgres
```

Connect to docker locally. ( Assuming you have psql installed )
```
$ sudo apt install postgresql-client
$ psql -h localhost -p 5432 -U postgres
```

