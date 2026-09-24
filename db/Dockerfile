FROM postgres:16-alpine

COPY init/ /docker-entrypoint-initdb.d/
COPY data/preparados/ /docker-entrypoint-initdb.d/data/