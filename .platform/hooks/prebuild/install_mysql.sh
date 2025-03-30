#!/bin/bash
# install_mysql.sh

# Update the package repository
sudo yum update -y

# Install MySQL 8.0 using amazon-linux-extras (for Amazon Linux 2)
sudo amazon-linux-extras install -y mysql8.0

# Install MySQL client and development libraries
sudo yum install -y mysql-devel

# Alternatively, if you prefer MariaDB instead of MySQL, you can use the following:
# sudo yum install -y mariadb mariadb-devel
