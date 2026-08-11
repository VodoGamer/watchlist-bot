## Production

This section describes the preferred method for deploying the bot (using Docker).

1. Install Docker with the Compose plugin
2. Download `docker-compose.yml` and `.env.example`
3. Fill out the `.env` file referring to the `.env.example` file
4. Create an empty database file, for example: `touch db.sqlite3`
5. Start services with `docker compose up -d` command

After this you can update services with command `docker compose pull && docker compose up -d`.
