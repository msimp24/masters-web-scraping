import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

DB_PATH = 'pga-data.db' 

# Creates SQLite database connection
conn = sqlite3.connect(DB_PATH)
mycursor = conn.cursor()

#bypasses website firewall header
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}
  
#function that gets the current id of the tournament  
def get_tournament_id():

  mycursor.execute("select last_tournament_id from tournament_tracker")

  myresult = mycursor.fetchone()
  tournament_id = myresult[0]
  
  return tournament_id

def scrape_data_to_database(headers):
  
    isNewWeek = True
  
    tournamentId = get_tournament_id()
    
  
    url = f"https://www.espn.co.uk/golf/leaderboard/_/tournamentId/{tournamentId}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
      
      soup = BeautifulSoup(response.text, 'html.parser')
    
      div = soup.find('div', class_='status cf mt4 mb4')

      span_element = div.find('span')

      status = span_element.get_text()      

      soup = BeautifulSoup(response.text, 'html.parser')

      table = soup.find('table', class_="Table Table--align-right Full__Table")

      if table:

        headers = [header.text.strip() for header in table.find_all("th")]
        rows = []
        for row in table.find_all('tr')[1:]:
          cells = row.find_all('td')
          row_data = [cell.text.strip() for cell in cells]
          row_data[0] = tournamentId
          rows.append(row_data)
        

      else:
        isNewWeek = False
        print("table not found, the structure might have changed")  

    else:
      print('Failed to retrieve the page, Status code: {respsonse.status_code}')
      
    print
      
    if(status == 'Final'):
      columns = ['tournament_id', 'Position', 'Player', 'Score', 'R1', 'R2', 'R3', 'R4', 'Total', 'Earnings', 'Fedex Pts']  
      

      
      df = pd.DataFrame(rows, columns = columns)
      df.to_sql('final_leaderboard', conn, if_exists='replace', index=False)
      
      newTournamentId = tournamentId + 1
      print(newTournamentId)
      mycursor.execute("UPDATE tournament_tracker SET last_tournament_id = ?" , (newTournamentId,))
      conn.commit()
      
      
    elif(isNewWeek):
      
      columns = ['tournament_id', 'Position', 'Player', 'Score','Today','Thru','R1', 'R2', 'R3', 'R4', 'Total']      
      df = pd.DataFrame(rows, columns = columns)
      df.to_sql('live_leaderboard', conn, if_exists='replace', index=False)
    
    else:
      
      print('New Tournament Data table has not yet been added to the website to be scraped')


scrape_data_to_database(headers)