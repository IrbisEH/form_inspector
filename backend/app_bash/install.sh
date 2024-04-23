#!/bin/bash

APP_PATH="/var/www/html/form_inspector"
ENV_PATH=$APP_PATH"/backend/.env"
SQL_SCRIPT_PATH=$APP_PATH"/backend/db_backup/form_inspector.sql"

FILE_CONF_PATH="/etc/mysql/mysql.conf.d/mysqld.cnf"

. $ENV_PATH

# RENEW APP DIR
if [ -d $APP_PATH ];
then
  sudo rm -rf $APP_PATH
fi

sudo mkdir -p $APP_PATH
sudo chmod -R 777 $APP_PATH

# update os
sudo apt update -y
sudo apt upgrade -y

if ! command -v mysql &> /dev/null
then
    sudo apt install -y mysql-server
fi

# CONFIGURE REMOTE ACCESS
sudo sed -i "s/^bind-address.*/bind_address=${DB_BIND_ADDRESS}/" $FILE_CONF_PATH
sudo systemctl restart mysql

#sudo systemctl restart mysql.service
sudo ufw allow from any to any port $DB_PORT

# CREATE DB
sudo mysql -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
sudo mysql -e "CREATE USER IF NOT EXISTS '$DB_USER'@'%' IDENTIFIED BY '$DB_PASS';"
sudo mysql -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'%' WITH GRANT OPTION;"
sudo mysql -e "FLUSH PRIVILEGES;"