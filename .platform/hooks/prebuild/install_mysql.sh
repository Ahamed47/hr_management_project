# #!/bin/bash
# set -e

# Check OS version
# if [ -f /etc/system-release ]; then
#     OS_VERSION=$(cat /etc/system-release)
    
#     # Amazon Linux 2
#     if [[ "$OS_VERSION" == *"Amazon Linux 2"* ]]; then
#         # Enable MySQL 8.0 and install MySQL for Amazon Linux 2
#         sudo amazon-linux-extras enable mysql8.0
#         sudo yum clean metadata
#         sudo yum install -y mysql mysql-server
        
#     # Amazon Linux 2023
#     elif [[ "$OS_VERSION" == *"Amazon Linux 2023"* ]]; then
#         # Install MySQL for Amazon Linux 2023 (uses dnf package manager)
#         sudo dnf install -y mysql-community-server
        
#         # In case MySQL is not available, install MariaDB as an alternative
#         if [ $? -ne 0 ]; then
#             echo "MySQL installation failed, attempting to install MariaDB instead."
#             sudo dnf install -y mariadb-server
#         fi
#     else
#         echo "Unknown OS version. Please ensure you're using Amazon Linux 2 or 2023."
#         exit 1
#     fi
# else
#     echo "Unable to detect OS version. Please ensure the system is running Amazon Linux."
#     exit 1
# fi

# # Start MySQL service
# sudo systemctl start mysqld
# sudo systemctl enable mysqld

# # Secure MySQL installation (interactive)
# sudo mysql_secure_installation
