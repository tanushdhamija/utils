#!/bin/bash

# https://learn.microsoft.com/en-us/sql/connect/python/pyodbc/step-1-configure-development-environment-for-pyodbc-python-development?view=sql-server-ver16#install-the-odbc-driver

if ! [[ "20.04 22.04 24.04 24.10" == *"$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2)"* ]];
then
    echo "Ubuntu $(grep VERSION_ID /etc/os-release | cut -d '"' -f 2) is not currently supported.";
    exit;
fi

# Download the package to configure the Microsoft repo
curl -sSL -O "https://packages.microsoft.com/config/ubuntu/$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2)/packages-microsoft-prod.deb"
# Install the package
sudo dpkg -i packages-microsoft-prod.deb
# Delete the file
rm packages-microsoft-prod.deb

# Install the driver
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
# optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools18
echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.zshrc
source ~/.zshrc
# optional: for unixODBC development headers
sudo apt-get install -y unixodbc-dev
