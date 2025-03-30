#!/bin/bash

# Update package lists
yum update -y

# Install MySQL development libraries compatible with Amazon Linux 2
yum install -y mysql mysql-server mysql-devel

# Alternatively, try installing MariaDB-devel if mysql-devel is not found
yum install -y mariadb mariadb-server mariadb-devel
