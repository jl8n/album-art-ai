# Album Art AI

Trains an AI via user selection to select the best search result


## Dev

### Set-up database

Start the postgres docker container

```bash
docker compose up db pgadmin
```

Create postgres schema

```bash
psql -d musicbrainz -f db_setup.sql
```

> The pgAdmin UI is accessible at http://localhost:8080