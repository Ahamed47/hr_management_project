#!/bin/bash
# install_mysql.sh

# Update the package repository
# sudo dnf update -y

# # Install MySQL 8.0
# sudo dnf install -y mysql mysql-server mysql-devel

# If you want MariaDB, use the following command instead:
# sudo dnf install -y mariadb mariadb-devel


#!/bin/bash

# Update package repository
sudo yum update -y

# Install MariaDB server and development libraries
sudo yum install -y mariadb-server mariadb-devel

# Start the MariaDB service
sudo systemctl start mariadb
sudo systemctl enable mariadb

# Secure the MariaDB installation (optional but recommended)
sudo mysql_secure_installation
