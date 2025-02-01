import requests
from bs4 import BeautifulSoup
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

mydb = mysql.connector.connect(
 host="localhost",
 port=3307,
 user="admin",
 password="Pass1234",
 db="pga-data",
)

engine = create_engine("mysql+mysqlconnector://admin:Pass1234@localhost:3307/pga-data")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}

def get_tournament_status(headers, tournamentId):
  url = f"https://www.espn.co.uk/golf/leaderboard/_/tournamentId/{tournamentId}"
  response = requests.get(url, headers=headers)

  if response.status_code == 200:

    soup = BeautifulSoup(response.text, 'html.parser')
    
    div = soup.find('div', class_='status cf mt4 mb4')

    span_element = div.find('span')

    text = span_element.get_text()

    return text
  
def get_last_id():
  mycursor = mydb.cursor()

  mycursor.execute("SELECT MAX(tournament_id) FROM tournaments")

  myresult = mycursor.fetchone()
  tournament_id = myresult[0]
  
  return tournament_id

def scrape_data_to_database(headers):
  
    tournamentId = get_last_id()
  
    url = f"https://www.espn.co.uk/golf/leaderboard/_/tournamentId/{tournamentId}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:

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
        print("table not found, the structure might have changed")  

    else:
      print('Failed to retrieve the page, Status code: {respsonse.status_code}')

    columns = ['tournament_id', 'Position', 'Player', 'Score','Today','Thru','R1', 'R2', 'R3', 'R4', 'Total']

    df = pd.DataFrame(rows, columns = columns)
    
    df.to_sql('leaderboard', engine,if_exists='replace', index=False)


scrape_data_to_database(headers)