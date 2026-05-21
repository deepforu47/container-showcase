FROM postgres:15-alpine

# Set default environment variables inside the DB image metadata
ENV POSTGRES_DB=analytics_db
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=supersecurepassword

# Configure a custom internal path for database storage files (optional customization demo)
ENV PGDATA=/var/lib/postgresql/data/custom

# Document that this runtime container relies on an external data volume at this mount point
VOLUME /var/lib/postgresql/data

EXPOSE 5432
