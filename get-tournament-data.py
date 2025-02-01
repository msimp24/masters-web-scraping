import mysql.connector

mydb = mysql.connector.connect(
 host="localhost",
 port=3307,
 user="admin",
 password="Pass1234",
 db="pga-data",
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM tournaments")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)