#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <database_name>"
    exit 1
fi

DB_NAME="$1"
DB_USER="${DB_NAME}_manager"
DB_PASSWORD="${DB_NAME}_manager"

# Create a new database
mysql -u root -p"password" -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME};"

# Create a user and grant privileges on the new database
mysql -u root -p"password" -e "CREATE USER ${DB_USER}@'%' IDENTIFIED BY '${DB_PASSWORD}';"
mysql -u root -p"password"  -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO ${DB_USER}@'%';"

# Flush privileges
mysql -u root -p"password"  -e "FLUSH PRIVILEGES;"

echo "Database '${DB_NAME}' and user '${DB_USER}' with password '${DB_PASSWORD}' created."
