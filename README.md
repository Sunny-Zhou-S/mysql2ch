# set up clickhouse cluster and mysql

```shell
docker-compose up
```

# connect to clickhouse

```shell
clickhouse-client -h localhost
```

# create database and table

```sql
CREATE DATABASE imdb ON CLUSTER 'imdb_cluster';

CREATE TABLE imdb.title_akas ON CLUSTER 'imdb_cluster' (
    titleID String,
    ordering Int64,
    title String,
    region Nullable(String),
    language Nullable(String),
    types Nullable(String),
    attributes Nullable(String),
    isOriginalTitle Int64
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{cluster}/{shard}/table', '{replica}') PARTITION BY titleID ORDER BY (titleID);
```

# import tsv file into mysql

```shell
python3 import_title_akas.py
```

# import mysql data into clickhouse

```shell
python3 main.py
```