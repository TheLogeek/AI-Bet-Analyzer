import os
import requests
#from dotenv import load_dotenv
import streamlit as st

AVAILABLE_LEAGUES = {
    'NCAAB': 'basketball_ncaab',
    'NBA': 'basketball_nba',
    'WNBA': 'basketball_wnba'
}

def get_upcoming_games(sport_key):
    """Fetches upcoming games and their odds from The Odds API."""
    #load_dotenv()
    
    api_key = st.secrets["API_KEY"]
    
    if not api_key or api_key == 'YOUR_API_KEY_HERE':
        st.error("Error: API_KEY not found or not set in .env file.")
        st.error("Please make sure to add your API key from The Odds API to the .env file.")
        return None

    url = (
        f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/"
        f"?apiKey={api_key}"
        "&regions=us"
        "&markets=h2h,totals"
        "&oddsFormat=decimal"
    )

    st.info(f"Fetching upcoming games from The Odds API for sport: {sport_key}")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        #st.info(f"Remaining requests: {response.headers['x-requests-remaining']}")
        #st.info(f"Used requests: {response.headers['x-requests-used']}")
        
        games = response.json()
        
        if not games:
            st.warning("No upcoming games found for this sport key.")
            return []
            
        return games

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from The Odds API: {e}")
        try:
            error_details = response.json()
            st.error(f"API Error Details: {error_details}")
        except ValueError:
            st.error(f"API returned non-JSON response: {response.text}")
        return None

if __name__ == '__main__':
    st.info("--- Testing API Client ---")
    
    for league_name, sport_key in AVAILABLE_LEAGUES.items():
        st.info(f"--- Fetching upcoming games for {league_name} ({sport_key}) ---")
        upcoming_games = get_upcoming_games(sport_key=sport_key)
        
        if upcoming_games:
            st.info(f"Successfully fetched {len(upcoming_games)} upcoming games for {league_name}.")
            
            if len(upcoming_games) > 0:
                first_game = upcoming_games[0]
                st.info("--- Example Game ---")
                st.info(f"ID: {first_game.get('id')}")
                st.info(f"Sport: {first_game.get('sport_title')}")
                st.info(f"Teams: {first_game.get('home_team')} vs. {first_game.get('away_team')}")
                st.info(f"Start Time: {first_game.get('commence_time')}")
                
                for bookmaker in first_game.get('bookmakers', []):
                    if any(market['key'] == 'totals' for market in bookmaker.get('markets', [])):
                        st.info(f"Bookmaker: {bookmaker.get('title')}")
                        for market in bookmaker.get('markets', []):
                            if market['key'] == 'totals':
                                st.info(f"  Market: Over/Under")
                                for outcome in market.get('outcomes', []):
                                    st.info(f"    - {outcome['name']} {outcome['point']}: {outcome['price']}")
                        break
        else:
            st.warning(f"Failed to fetch upcoming games for {league_name}. Please check your API key and network connection.")