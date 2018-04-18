# Dumb script to kill all python processes and clear databases. USE CAREFULLY.
killall -s KILL python;
mysql --host=localhost --user=root --password=root --database=honeywords -e "clear_tables.sql"
rm auxiliary/database.crypt
