import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime, timedelta
import re
import os

def get_data_for_date(date_str, league_key):
    """Fetches basketball game data for a given date and league from Covers.com."""
    url = f"https://www.covers.com/sports/{league_key}/matchups?selectedDate={date_str}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}: Fetching data from: {url}")
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            games_data = []

            game_cards = soup.find_all('article', class_='gamebox')
            
            if not game_cards:
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
                    print(f"An unexpected error occurred while parsing a game card for {league_key} on {date_str} (Attempt {attempt + 1}): {e}")
                    continue
            return games_data # Successfully fetched and parsed data for this date

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed for {url}: {e}")
            if attempt < max_retries - 1:
                sleep_time = 2 ** attempt
                print(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                print(f"Failed to fetch data for {date_str} in league {league_key} after {max_retries} attempts.")
                return [] # Return empty list if all retries fail
        except Exception as e: # Catch any other unexpected errors during parsing
            print(f"An unexpected error occurred for {date_str} in league {league_key} on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                sleep_time = 2 ** attempt
                print(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                print(f"Failed to process data for {date_str} in league {league_key} after {max_retries} attempts.")
                return []

    return games_data # Safeguard return

def scrape_historical_data(start_date, end_date, league_key, output_file):
    """Scrapes basketball data for a given league and date range, saving it to a CSV file."""
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
    
    all_games = []

    while current_date <= end_date_dt:
        date_str = current_date.strftime('%Y-%m-%d')
        games_for_date = get_data_for_date(date_str, league_key=league_key)
        if games_for_date:
            all_games.extend(games_for_date)
        
        current_date += timedelta(days=1)
    
    if all_games:
        df = pd.DataFrame(all_games)
        
        if os.path.exists(output_file):
            df.to_csv(output_file, mode='a', header=False, index=False)
        else:
            df.to_csv(output_file, index=False)
            
        print(f"Successfully scraped/appended {len(all_games)} games for {league_key.upper()} to {output_file}")
    else:
        print(f"No games scraped for {league_key.upper()} in the specified date range.")

if __name__ == "__main__":
    # Updated date ranges to include recent data up to December 24, 2025
    # NCAA season typically ends in early April, so extending to March 31, 2025 is reasonable.
    # NBA/WNBA seasons typically extend into June/October. Extending to Dec 24, 2025 captures ongoing and upcoming data.
    leagues_to_scrape = [
        ('ncaab', '2024-09-01', '2025-03-31'), # NCAA Fall/Winter season through early 2025
        ('nba', '2023-10-01', '2025-12-24'), # NBA up to present date
        ('wnba', '2024-05-01', '2025-12-24'), # WNBA up to present date
    ]
    
    output_filename = 'data/raw/historical_basketball_data.csv'

    # Clear the file to start fresh with combined data
    if os.path.exists(output_filename):
        os.remove(output_filename)
        print(f"Removed existing data file: {output_filename}")


    for league_key, start, end in leagues_to_scrape:
        scrape_historical_data(start, end, league_key, output_filename)

    print("\n--- Scraping process complete for all defined leagues. ---")
