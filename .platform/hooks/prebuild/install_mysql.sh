#!/bin/bash
# install_mysql.sh

# Update the package repository
sudo yum update -y

# Install MySQL client (do not install MySQL server or MariaDB server)
sudo yum install -y mysql

# Install MySQL development libraries (for the MySQL client and Python bindings)
sudo yum install -y mysql-devel
