import mysql.connector

mydb = mysql.connector.connect(
 host="localhost",
 port=3307,
 user="admin",
 password="Pass1234",
 db="pga-data",
)

mycursor = mydb.cursor()

sql = "INSERT INTO tournaments(tournament_id, name, year, location) VALUES (%s, %s, %s, %s)"
val = ("401703492", "Farmers Insurance", "2025", "La Jolla, CA")

mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "Record inserted")
