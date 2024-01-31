FROM mysql:8.3

WORKDIR /workspace

# COPY ./my.cnf /etc/mysql/conf.d/custom.cnf

COPY scripts/ /workspace/scripts/
COPY sql/ /workspace/sql/

CMD ["mysqld"]
