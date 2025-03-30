#!/bin/bash

# Update package information
sudo dnf update -y

# Install MySQL or MariaDB server and development libraries
sudo dnf install -y mysql mysql-server mysql-devel || sudo dnf install -y mariadb mariadb-server mariadb-devel
