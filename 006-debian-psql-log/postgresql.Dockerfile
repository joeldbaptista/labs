# Use the official PostgreSQL image from the Docker Hub
FROM postgres:15

# The official PostgreSQL image's entrypoint will take care of initializing the DB
# so no need to specify CMD or ENTRYPOINT.

