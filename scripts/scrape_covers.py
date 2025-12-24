import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime, timedelta
import re
import os

def get_data_for_date(date_str, league_key):
    """
    Fetches basketball game data (scores and odds) for a given date and league from Covers.com.

    Args:
        date_str (str): The date in 'YYYY-MM-DD' format.
        league_key (str): The league abbreviation used in Covers.com URL (e.g., 'ncaab', 'nba', 'wnba').

    Returns:
        list: A list of dictionaries, where each dictionary represents a game.
    """
    url = f"https://www.covers.com/sports/{league_key}/matchups?selectedDate={date_str}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"Fetching data from: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {date_str} in league {league_key}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    games_data = []

    game_cards = soup.find_all('article', class_='gamebox')
    
    if not game_cards:
        # Fallback for older Covers.com structures if present, or if 'gamebox' isn't always the class
        game_cards = soup.find_all('div', class_='rc-Card cmg_matchup_game_card')
        if not game_cards:
            print(f"No game cards found for {date_str} in league {league_key} with expected selectors.")
            return []

    print(f"Found {len(game_cards)} potential game cards for {date_str}.")

    for card in game_cards:
        try:
            home_team_fullname = card.get('data-home-team-fullname', 'N/A')
            away_team_fullname = card.get('data-away-team-fullname', 'N/A')

            home_score = 'N/A'
            away_score = 'N/A'
            
            score_table = card.find('table')
            if score_table and score_table.find('tbody'):
                rows = score_table.find('tbody').find_all('tr')
                if len(rows) == 2:
                    away_score_cells = rows[0].find_all('td')
                    home_score_cells = rows[1].find_all('td')
                    if away_score_cells and home_score_cells:
                        away_score = away_score_cells[-1].text.strip()
                        home_score = home_score_cells[-1].text.strip()

            if home_score == 'N/A' or away_score == 'N/A':
                home_score_elem = card.find('strong', class_='team-score home')
                away_score_elem = card.find('strong', class_='team-score away')
                if home_score_elem and away_score_elem:
                    home_score = home_score_elem.text.strip()
                    away_score = away_score_elem.text.strip()
            
            ou_summary_elem = card.find('p', class_='summary-box')
            ou_line = 'N/A'
            if ou_summary_elem:
                match = re.search(r'was\s+(?:over|under)\s+([\d.]+)', ou_summary_elem.text)
                if match:
                    ou_line = match.group(1)

            if home_team_fullname == 'N/A' or away_team_fullname == 'N/A' or home_score == 'N/A' or away_score == 'N/A' or ou_line == 'N/A':
                # print(f"Skipping game due to missing essential data: {away_team_fullname} vs {home_team_fullname}")
                continue

            games_data.append({
                'Date': date_str,
                'League': league_key.upper(),
                'HomeTeam': home_team_fullname.title(),
                'AwayTeam': away_team_fullname.title(),
                'HomeScore': home_score,
                'AwayScore': away_score,
                'OU_Line': ou_line
            })
        except Exception as e:
            print(f"An unexpected error occurred while parsing a game card for {league_key} on {date_str}: {e}")
            continue

    return games_data

def scrape_historical_data(start_date, end_date, league_key, output_file):
    """
    Scrapes basketball data for a given league and date range, saving it to a CSV file.
    """
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
    
    all_games = []

    while current_date <= end_date_dt:
        date_str = current_date.strftime('%Y-%m-%d')
        games_for_date = get_data_for_date(date_str, league_key=league_key)
        if games_for_date:
            all_games.extend(games_for_date)
        
        time.sleep(1) # Be respectful
        current_date += timedelta(days=1)
    
    if all_games:
        df = pd.DataFrame(all_games)
        
        # Check if file exists to append or write new
        if os.path.exists(output_file):
            df.to_csv(output_file, mode='a', header=False, index=False)
        else:
            df.to_csv(output_file, index=False)
            
        print(f"Successfully scraped/appended {len(all_games)} games for {league_key.upper()} to {output_file}")
    else:
        print(f"No games scraped for {league_key.upper()} in the specified date range.")

if __name__ == "__main__":
    # Define leagues and date ranges
    # Covers.com league keys: 'ncaab', 'nba', 'wnba'
    
    leagues_to_scrape = [
        # Existing NCAAB data
        ('ncaab', '2022-11-01', '2023-03-31'),
        # New: NBA data (last two full seasons)
        ('nba', '2022-10-01', '2023-06-30'), # NBA 2022-2023 season
        ('nba', '2023-10-01', '2024-06-30'), # NBA 2023-2024 season
        # New: WNBA data (last two full seasons)
        ('wnba', '2023-05-01', '2023-10-31'), # WNBA 2023 season
        ('wnba', '2024-05-01', '2024-10-31'), # WNBA 2024 season
    ]
    
    output_filename = 'data/raw/historical_basketball_data.csv'

    # Clear the file to start fresh with combined data
    if os.path.exists(output_filename):
        os.remove(output_filename)
        print(f"Removed existing data file: {output_filename}")


    for league_key, start, end in leagues_to_scrape:
        scrape_historical_data(start, end, league_key, output_filename)

    print("\n--- Scraping process complete for all defined leagues. ---")
