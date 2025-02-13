import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

DB_PATH = os.path.join(os.getcwd(), 'pga-data.db')

conn = sqlite3.connect(DB_PATH)
mycursor = conn.cursor()


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}
  
def get_tournament_id():

  mycursor.execute("select last_tournament_id from tournament_tracker")

  myresult = mycursor.fetchone()
  tournament_id = myresult[0]
  
  return tournament_id
 
 
url = f"https://www.espn.co.uk/golf/leaderboard/_/tournamentId/{get_tournament_id()}" 
  
response = requests.get(url, headers=headers)
  
if response.status_code == 200:
   soup = BeautifulSoup(response.text, 'html.parser')

   table = soup.find('table', class_="Table Table--align-right Full__Table")

   if table:

     columns = [header.text.strip() for header in table.find_all("th")]
     rows = []
     for row in table.find_all('tr')[1:]:
       cells = row.find_all('td')
       row_data = [cell.text.strip() for cell in cells]
       row_data[0] = get_tournament_id()
       rows.append(row_data)
       
       
   
   df = pd.DataFrame(rows, columns = columns)
   df.to_sql('final_leaderboard', conn, if_exists='replace', index=False)
       