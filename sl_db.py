import psycopg2, psycopg2.extras

db_name = "proddb"
host_name = "rs1pproddb003v"
# host_name = "db"
# db_name = "staging"
# host_name = "devdb"

database = psycopg2.connect( dbname=db_name, user="reports", password="5w0rdf1sh", host=host_name)
print "[Database] Connected to "+db_name+" on "+host_name
