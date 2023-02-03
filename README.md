Pull latest cassandra container
```docker pull cassandra:latest```

Run the container
```docker run --rm -d --name cassandra --hostname cassandra -p 9042:9042 cassandra ```

Run the `cql` module to initialise a keyspace
```poetry run python -m cql```