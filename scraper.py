import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

DB_PATH = os.path.join(os.getcwd(), 'pga-data.db')

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
    
    print(tournamentId)
    
  
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
      print('Failed to retrieve the page, Status code: {response.status_code}')
      
      
    if(status == 'Final'):
      columns = ['tournament_id', 'Position', 'Player', 'Score', 'R1', 'R2', 'R3', 'R4', 'Total', 'Earnings', 'Fedex Pts']  
      
      df = pd.DataFrame(rows, columns = columns)
      df.to_sql('final_leaderboard', conn, if_exists='append', index=False)
      
      print("Saving to database path:", DB_PATH)  # Debugging line to check the path

      print('Final leaderboard updated')
      
      newTournamentId = tournamentId + 1
      mycursor.execute("UPDATE tournament_tracker SET last_tournament_id = ?" , (newTournamentId,))
      conn.commit()
      
    elif(isNewWeek and status != 'Tournament Field'):
      
      columns = ['tournament_id', 'Position', 'Player', 'Score','Today','Thru','R1', 'R2', 'R3', 'R4', 'Total']      
      
      print(columns)
      print(rows)
      
      
      df = pd.DataFrame(rows, columns = columns)
      df.to_sql('live_leaderboard', conn, if_exists='replace', index=False)
    
    else:
      
      print('New Tournament Data table has not yet been added to the website to be scraped')


scrape_data_to_database(headers)