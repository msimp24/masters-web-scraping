import sqlite3
import os

conn = sqlite3.connect('pga-data.db')
mycursor = conn.cursor()

def get_tournament_id():

  mycursor.execute("select last_tournament_id from tournament_tracker")

  myresult = mycursor.fetchone()
  tournament_id = myresult[0]
  
  return tournament_id
 
print(get_tournament_id()) 
 

conn.close()