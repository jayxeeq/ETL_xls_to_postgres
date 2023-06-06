# ETL_xls_to_postgres

# Required libraries
pip install pandas psycopg2

# Common problems encountered on linux environment:

Error installing psycopg2
ERROR: Command errored out with exit status 1:
Fixes: 
sudo apt-get install libpq-dev
sudo apt-get install build-essential
pip install --upgrade pip
pip install psycopg2


Numpy has no float attribute error when using Read_Excel https://stackoverflow.com/questions/75386792/numpy-has-no-float-attribute-error-when-using-read-excel
FIX: upgrading openpyxl 
pip install openpyxl --upgrade

