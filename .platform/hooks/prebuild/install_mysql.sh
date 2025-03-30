#!/bin/bash
# install_mysql.sh

# Update the package repository
sudo dnf update -y

# Install MySQL 8.0
sudo dnf install -y mysql mysql-server mysql-devel

# If you want MariaDB, use the following command instead:
# sudo dnf install -y mariadb mariadb-devel
