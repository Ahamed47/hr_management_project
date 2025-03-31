#!/bin/bash

# Enable MySQL 8.0 repository (if using Amazon Linux 2)
sudo amazon-linux-extras enable mysql8.0

# Install MySQL
sudo yum clean metadata
sudo yum install -y mysql mysql-server

# Start MySQL service
sudo systemctl start mysqld
sudo systemctl enable mysqld

# Run MySQL secure installation
sudo mysql_secure_installation








#!/bin/bash
# install_mysql.sh

# Update the package repository
# sudo dnf update -y

# # Install MySQL 8.0
# sudo dnf install -y mysql mysql-server mysql-devel

# If you want MariaDB, use the following command instead:
# sudo dnf install -y mariadb mariadb-devel


#!/bin/bash

# # Update packages and install amazon-linux-extras if missing
# sudo yum update -y
# sudo yum install -y amazon-linux-extras

# # Enable MySQL 8.0
# sudo amazon-linux-extras enable mysql8.0

# # Install MySQL server
# sudo yum install -y mysql mysql-server

# # Start MySQL service
# sudo systemctl start mysqld
# sudo systemctl enable mysqld

# # Secure MySQL installation
# sudo mysql_secure_installation

