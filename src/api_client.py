import os
import requests
import streamlit as st

AVAILABLE_LEAGUES = {
    'NCAAB': 'basketball_ncaab',
    'NBA': 'basketball_nba',
    'WNBA': 'basketball_wnba'
}

def get_upcoming_games(sport_key):
    """
    Fetches upcoming games and their odds from The Odds API.

    Args:
        sport_key (str): The key for the sport to fetch, e.g., 'basketball_ncaab'.

    Returns:
        list: A list of dictionaries, where each dictionary represents an upcoming game.
              Returns None if the API call fails.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    api_key = st.secrets["API_KEY"]
    
    if not api_key or api_key == 'YOUR_API_KEY_HERE':
        print("Error: API_KEY not found or not set in .env file.")
        print("Please make sure to add your API key from The Odds API to the .env file.")
        return None

    # API endpoint for upcoming odds
    # We are interested in 'h2h' (head-to-head) and 'totals' (for over/under)
    url = (
        f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/"
        f"?apiKey={api_key}"
        "&regions=us"
        "&markets=h2h,totals"
        "&oddsFormat=decimal"
    )

    print(f"Fetching upcoming games from The Odds API for sport: {sport_key}")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Check usage
        print('Remaining requests', response.headers['x-requests-remaining'])
        print('Used requests', response.headers['x-requests-used'])
        
        games = response.json()
        
        if not games:
            print("No upcoming games found for this sport key.")
            return []
            
        return games

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from The Odds API: {e}")
        # The API might return a non-JSON error message
        try:
            error_details = response.json()
            print(f"API Error Details: {error_details}")
        except ValueError:
            print(f"API returned non-JSON response: {response.text}")
        return None

if __name__ == '__main__':
    print("--- Testing API Client ---")
    
    for league_name, sport_key in AVAILABLE_LEAGUES.items():
        print(f"\n--- Fetching upcoming games for {league_name} ({sport_key}) ---")
        upcoming_games = get_upcoming_games(sport_key=sport_key)
        
        if upcoming_games:
            print(f"Successfully fetched {len(upcoming_games)} upcoming games for {league_name}.")
            
            # Print details of the first game for verification
            if len(upcoming_games) > 0:
                first_game = upcoming_games[0]
                print("\n--- Example Game ---")
                print(f"ID: {first_game.get('id')}")
                print(f"Sport: {first_game.get('sport_title')}")
                print(f"Teams: {first_game.get('home_team')} vs. {first_game.get('away_team')}")
                print(f"Start Time: {first_game.get('commence_time')}")
                
                # Find a bookmaker with 'totals' odds to display
                for bookmaker in first_game.get('bookmakers', []):
                    if any(market['key'] == 'totals' for market in bookmaker.get('markets', [])):
                        print(f"\nBookmaker: {bookmaker.get('title')}")
                        for market in bookmaker.get('markets', []):
                            if market['key'] == 'totals':
                                print(f"  Market: Over/Under")
                                for outcome in market.get('outcomes', []):
                                    print(f"    - {outcome['name']} {outcome['point']}: {outcome['price']}")
                        break # Stop after finding one bookmaker with totals
        else:
            print(f"\nFailed to fetch upcoming games for {league_name}. Please check your API key and network connection.")
