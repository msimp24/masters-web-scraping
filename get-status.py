import requests
from bs4 import BeautifulSoup
import pandas as pd
import mysql.connector


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}
mydb = mysql.connector.connect(
 host="localhost",
 port=3307,
 user="admin",
 password="Pass1234",
 db="pga-data",
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}


def add_new_tournament(headers):
  url = f"https://www.espn.co.uk/golf/leaderboard/_/tournamentId"
  response = requests.get(url, headers=headers)

  if response.status_code == 200:

    soup = BeautifulSoup(response.text, 'html.parser')
    
    h1 = soup.find('h1', class_='headline headline__h1 Leaderboard__Event__Title')
    div = soup.find('div', class_="Leaderboard__Course__Location n8 clr-gray-05")
    title = h1.get_text()
    location = div.get_text()
    
    ## change this to get the id of the current tournament being played
    tournamentId = 12345678
    
    mycursor = mydb.cursor()

    sql = "INSERT INTO tournaments(tournament_id, name, year, location) VALUES (%s, %s, %s, %s)"
    val = (tournamentId, title, "2025", location)

    mycursor.execute(sql, val)

    mydb.commit()

  
  
add_new_tournament(headers)  