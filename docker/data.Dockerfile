FROM alpine:latest

WORKDIR /data

# Copy both CSV and SQLite DB into the shared volume
COPY ./data/titanic.csv .
COPY ./data/titanic.db .

# Keep the container alive; it just exists to hold the shared volume
CMD ["tail", "-f", "/dev/null"]
