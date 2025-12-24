import pandas as pd
import joblib
from src.api_client import get_upcoming_games, AVAILABLE_LEAGUES
import numpy as np
import streamlit as st

TEAM_NAME_MAP = {
    "St. John's Red Storm": "St. John'S",
    "CSU Bakersfield Roadrunners": "Cal State Bakersfield",
    "Missouri St Bears": "Missouri State",
    "St. Mary's Gaels": "Saint Mary'S (Ca)",
    "Usc Trojans": "Usc",
    "Ole Miss Rebels": "Mississippi",
    "Ohio St Buckeyes": "Ohio State",
    "North Carolina St Wolfpack": "North Carolina State",
    "Lsu Tigers": "Lsu",
    "Byu Cougars": "Byu",
    "Loyola-Chicago Ramblers": "Loyola Chicago",
    "Central Florida Knights": "Central Florida",
    "Nc-Greensboro Spartans": "Unc Greensboro",
    "Long Beach State Beach": "Long Beach State",
    "Boise St Broncos": "Boise State",
    "Michigan St Spartans": "Michigan State",
    "Washington St Cougars": "Washington State",
    "Oregon St Beavers": "Oregon State",
    "Kansas St Wildcats": "Kansas State",
    "Okla State Cowboys": "Oklahoma State",
    "Florida St Seminoles": "Florida State",
    "Arizona St Sun Devils": "Arizona State",
    "Georgia Tech Yellow Jackets": "Georgia Tech",
    "Va Tech Hokies": "Virginia Tech",
    "Wvu Mountaineers": "West Virginia",
    "Penn State Nittany Lions": "Penn State",
    "Miss State Bulldogs": "Mississippi State",
    "Kent State Golden Flashes": "Kent State",
    "Iowa State Cyclones": "Iowa State",
    "East Carolina Pirates": "East Carolina",
    "South Carolina Gamecocks": "South Carolina",
    "Middle Tennessee Blue Raiders": "Middle Tennessee",
    "Florida Gulf Coast Eagles": "Florida Gulf Coast",
    "College of Charleston Cougars": "Charleston",
    "St Louis Billikens": "Saint Louis",
    "Saint Joseph's Hawks": "Saint Joseph'S",
    "North Carolina Tar Heels": "North Carolina",
    "UTEP Miners": "Utep",
    "UNLV Rebels": "Unlv",
    "Cal Poly Mustangs": "Cal Poly",
    "Abilene Christian Wildcats": "Abilene Christian",
    "S. Dakota State Jackrabbits": "South Dakota State",
    "Boston U Terriers": "Boston University",
    "UMass Lowell River Hawks": "Um-Lowell",
    "Central Conn State Blue Devils": "Central Connecticut",
    "Nc-Wilmington Seahawks": "Unc Wilmington",
    "Stephen F Austin Lumberjacks": "Stephen F Austin",
    "S Carolina Upstate Spartans": "Sc Upstate",
    "Little Rock Trojans": "Arkansas-Little Rock",
    "Eastern Washington Eagles": "Eastern Washington",
    "Western Carolina Catamounts": "Western Carolina",
    "Northern Kentucky Norse": "Northern Kentucky",
    "South Dakota Coyotes": "South Dakota",
    "Eastern Illinois Panthers": "Eastern Illinois",
    "Southeast Missouri State Redhawks": "Se Missouri State",
    "Western Illinois Leathernecks": "Western Illinois",
    "Southern Illinois Salukis": "Southern Illinois",
    "Cal Baptist Lancers": "California Baptist",
    "North Alabama Lions": "North Alabama",
    "South Alabama Jaguars": "South Alabama",
    "Central Arkansas Bears": "Central Arkansas",
    "Southern Utah Thunderbirds": "Southern Utah",
    "Utah Tech Trailblazers": "Utah Tech",
    "California Baptist Lancers": "California Baptist",
    "Louisiana-Monroe Warhawks": "Ul Monroe",
    "Louisiana-Lafayette Ragin' Cajuns": "Louisiana",
    "Appalachian State Mountaineers": "Appalachian State",
    "Georgia State Panthers": "Georgia State",
    "Coastal Carolina Chanticleers": "Coastal Carolina",
    "UL Monroe Warhawks": "Ul Monroe",
    "Arkansas State Red Wolves": "Arkansas State",
    "Ga Southern Eagles": "Georgia Southern",
    "Texas St Bobcats": "Texas State",
    "Ut-Arlington Mavericks": "Ut Arlington",
    "Wichita St Shockers": "Wichita State",
    "Middle Tenn Blue Raiders": "Middle Tennessee",
    "Old Dominion Monarchs": "Old Dominion",
    "Uab Blazers": "Uab",
    "Western Kentucky Hilltoppers": "Western Kentucky",
    "Florida Atlantic Owls": "Florida Atlantic",
    "Tx-San Antonio Roadrunners": "Ut San Antonio",
    "Louisiana Tech Bulldogs": "Louisiana Tech",
    "Bowling Green Falcons": "Bowling Green",
    "Eastern Michigan Eagles": "Eastern Michigan",
    "Central Michigan Chippewas": "Central Michigan",
    "Western Michigan Broncos": "Western Michigan",
    "Northern Illinois Huskies": "Northern Illinois",
    "Ball State Cardinals": "Ball State",
    "Miami-Ohio RedHawks": "Miami (Oh)",
    "Kent St Golden Flashes": "Kent State",
    "Akron Zips": "Akron",
    "Ohio Bobcats": "Ohio",
    "South Alabama Jaguars": "South Alabama",
    "Ga. Southern Eagles": "Georgia Southern",
    "Louisiana Ragin' Cajuns": "Louisiana",
    "Appalachian St Mountaineers": "Appalachian State",
    "Arkansas St Red Wolves": "Arkansas State",
    "Coastal Caro Chanticleers": "Coastal Carolina",
    "Texas-Arlington Mavericks": "Ut Arlington",
    "Little Rock Trojans": "Arkansas-Little Rock",
    "UMKC Kangaroos": "Umkc",
    "North Dakota State Bison": "North Dakota State",
    "South Dakota State Jackrabbits": "South Dakota State",
    "Western Illinois Leathernecks": "Western Illinois",
    "Southeast Missouri St Redhawks": "Se Missouri State",
    "Eastern Illinois Panthers": "Eastern Illinois",
    "Southern Illinois Salukis": "Southern Illinois",
    "Cal Poly Mustangs": "Cal Poly",
    "Cal St Fullerton Titans": "Cal State Fullerton",
    "CSUN Matadors": "Cs Northridge",
    "UC Riverside Highlanders": "Uc Riverside",
    "UC Davis Aggies": "Uc Davis",
    "UC Irvine Anteaters": "Uc Irvine",
    "UC Santa Barbara Gauchos": "Uc Santa Barbara",
    "Long Beach St Beach": "Long Beach State",
    "Hawai'i Rainbow Warriors": "Hawaii",
    "St. Thomas (MN) Tommies": "St Thomas",
    "UMass-Lowell River Hawks": "Um-Lowell",
    "Stonehill Skyhawks": "Stonehill",
    "Central Arkansas Bears": "Central Arkansas",
    "North Florida Ospreys": "North Florida",
    "Florida Gulf Coast Eagles": "Florida Gulf Coast",
    "Kennesaw State Owls": "Kennesaw State",
    "Jacksonville State Gamecocks": "Jacksonville State",
    "North Alabama Lions": "North Alabama",
    "Eastern Kentucky Colonels": "Eastern Kentucky",
    "Southern Indiana Screaming Eagles": "Southern Indiana",
    "UT Martin Skyhawks": "Ut Martin",
    "Tennessee Tech Golden Eagles": "Tennessee Tech",
    "SIUE Cougars": "Siue",
    "Morehead State Eagles": "Morehead State",
    "Western Illinois Leathernecks": "Western Illinois",
    "Lindenwood Lions": "Lindenwood",
    "Little Rock Trojans": "Arkansas-Little Rock",
    "Omaha Mavericks": "Omaha",
    "Denver Pioneers": "Denver",
    "St. Thomas-Minnesota Tommies": "St Thomas",
    "Tarleton State Texans": "Tarleton State",
    "UT Rio Grande Valley Vaqueros": "Ut Rio Grande Valley",
    "Grand Canyon Antelopes": "Grand Canyon",
    "California Baptist Lancers": "California Baptist",
    "Southern Utah Thunderbirds": "Southern Utah",
    "Utah Valley Wolverines": "Utah Valley",
    "Seattle U Redhawks": "Seattle",
    "New Mexico St Aggies": "New Mexico State",
    "Stephen F. Austin Lumberjacks": "Stephen F Austin",
    "Sam Houston State Bearkats": "Sam Houston State",
    "Florida Intl Golden Panthers": "Florida International",
    "Western Kentucky Hilltoppers": "Western Kentucky",
    "Middle Tennessee Blue Raiders": "Middle Tennessee",
    "Charlotte 49ers": "Charlotte",
    "Texas-San Antonio Roadrunners": "Ut San Antonio",
    "Florida Atlantic Owls": "Florida Atlantic",
    "North Texas Mean Green": "North Texas",
    "UAB Blazers": "Uab",
    "Louisiana Tech Bulldogs": "Louisiana Tech",
    "Old Dominion Monarchs": "Old Dominion",
    "Rice Owls": "Rice",
    "UTEP Miners": "Utep",
    "Wichita State Shockers": "Wichita State",
    "East Carolina Pirates": "East Carolina",
    "UCF Knights": "Central Florida",
    "Memphis Tigers": "Memphis",
    "South Florida Bulls": "South Florida",
    "Houston Cougars": "Houston",
    "Cincinnati Bearcats": "Cincinnati",
    "Tulane Green Wave": "Tulane",
    "Temple Owls": "Temple",
    "SMU Mustangs": "Smu",
    "UConn Huskies": "Connecticut",
    "BYU Cougars": "Byu",
    "UC Santa Barbara Gauchos": "Uc Santa Barbara",
    "Loyola Chicago Ramblers": "Loyola Chicago",
    "St. Louis Billikens": "Saint Louis",
    "Richmond Spiders": "Richmond",
    "St. Bonaventure Bonnies": "Saint Bonaventure",
    "George Mason Patriots": "George Mason",
    "George Washington Revolutionaries": "George Washington",
    "La Salle Explorers": "La Salle",
    "VCU Rams": "Vcu",
    "UMass Minutemen": "Um_Ass",
    "Dayton Flyers": "Dayton",
    "Saint Joseph's Hawks": "Saint Joseph'S",
    "North Carolina Tar Heels": "North Carolina",
    "Fordham Rams": "Fordham",
    "Rhode Island Rams": "Rhode Island",
    "St. Joseph's Hawks": "Saint Joseph'S",

    "Atlanta Hawks": "Atlanta",
    "Boston Celtics": "Boston",
    "Brooklyn Nets": "Brooklyn",
    "Charlotte Hornets": "Charlotte",
    "Chicago Bulls": "Chicago",
    "Cleveland Cavaliers": "Cleveland",
    "Dallas Mavericks": "Dallas",
    "Denver Nuggets": "Denver",
    "Detroit Pistons": "Detroit",
    "Golden State Warriors": "Golden State",
    "Houston Rockets": "Houston",
    "Indiana Pacers": "Indiana",
    "Los Angeles Clippers": "La Clippers",
    "Los Angeles Lakers": "La Lakers",
    "Memphis Grizzlies": "Memphis",
    "Miami Heat": "Miami",
    "Milwaukee Bucks": "Milwaukee",
    "Minnesota Timberwolves": "Minnesota",
    "New Orleans Pelicans": "New Orleans",
    "New York Knicks": "New York",
    "Oklahoma City Thunder": "Oklahoma City",
    "Orlando Magic": "Orlando",
    "Philadelphia 76ers": "Philadelphia",
    "Phoenix Suns": "Phoenix",
    "Portland Trail Blazers": "Portland",
    "Sacramento Kings": "Sacramento",
    "San Antonio Spurs": "San Antonio",
    "Toronto Raptors": "Toronto",
    "Utah Jazz": "Utah",
    "Washington Wizards": "Washington",

    "Atlanta Dream": "Atlanta",
    "Chicago Sky": "Chicago",
    "Connecticut Sun": "Connecticut",
    "Dallas Wings": "Dallas",
    "Indiana Fever": "Indiana",
    "Las Vegas Aces": "Las Vegas",
    "Los Angeles Sparks": "Los Angeles",
    "Minnesota Lynx": "Minnesota",
    "New York Liberty": "New York",
    "Phoenix Mercury": "Phoenix",
    "Seattle Storm": "Seattle",
    "Washington Mystics": "Washington",
}

def standardize_team_name(team_name):
    normalized_input = team_name.title()

    if normalized_input in TEAM_NAME_MAP:
        return TEAM_NAME_MAP[normalized_input].lower()
    
    for key, value in TEAM_NAME_MAP.items():
        if normalized_input == key.title():
             return value.lower()

    team_name_lower = team_name.lower()
    
    common_suffixes = [
        ' state', ' tech', ' a&m', ' am', ' red storm', ' roadrunners', ' bears', ' gaels', ' trojans', ' rebels',
        ' buckeyes', ' wolfpack', ' tigers', ' cougars', ' ramblers', ' knights', ' spartans', ' beavers',
        ' wildcats', ' cowboys', ' seminoles', ' sun devils', ' yellow jackets', ' hokies', ' mountaineers',
        ' nittany lions', ' bulldogs', ' golden flashes', ' cyclones', ' pirates', ' gamecocks', ' blue raiders',
        ' eagles', ' seahawks', ' lumberjacks', ' salukis', ' leathernecks', ' redhawks', ' broncos', ' chippewas',
        ' panthers', ' river hawks', ' thunderbirds', ' vaqueros', ' anteaters', ' gauchos', ' matadors',
        ' banana slugs', ' fighting hawaiians', ' shockers', ' monarchs', ' blazers', ' hilltoppers', ' owls',
        ' mean green', ' cardinals', ' huskie', ' bobcats', ' zips', ' aggies', ' bearkats', ' 49ers',
        ' green wave', ' grizzlies', ' heat', ' bucks', ' timberwolves', ' pelicans', ' knicks', ' thunder',
        ' magic', ' 76ers', ' suns', ' trail blazers', ' kings', ' spurs', ' raptors', ' jazz', ' wizards',
        ' dream', ' sky', ' sun', ' wings', ' fever', ' aces', ' sparks', ' lynx', ' liberty', ' mercury',
        ' storm', ' mystics'
    ]
    city_suffixes = [
        ' lakers', ' clippers', ' nets', ' celtics', ' hornets', ' bulls', ' cavaliers', ' mavericks',
        ' pistons', ' warriors', ' rockets', ' pacers', ' grizzlies', ' heat', ' bucks', ' timberwolves',
        ' pelicans', ' knicks', ' thunder', ' magic', ' 76ers', ' suns', ' trail blazers', ' kings',
        ' spurs', ' raptors', ' jazz', ' wizards', ' dream', ' sky', ' sun', ' wings', ' fever', ' aces',
        ' sparks', ' lynx', ' liberty', ' mercury', ' storm', ' mystics'
    ]

    for suffix in common_suffixes + city_suffixes:
        if team_name_lower.endswith(suffix):
            base_name = team_name_lower.replace(suffix, '').strip()
            if base_name:
                return base_name

    return team_name_lower.split(' ')[0] if team_name_lower else team_name_lower

def get_team_history(team_name, historical_df):
    std_team_name = standardize_team_name(team_name)
    history = historical_df[
        (historical_df['HomeTeam'].str.lower().str.contains(std_team_name)) |
        (historical_df['AwayTeam'].str.lower().str.contains(std_team_name))
    ].copy()
    return history.sort_values(by='Date', ascending=False)

def calculate_features_for_game(home_team, away_team, historical_df, window_size=10):
    home_history = get_team_history(home_team, historical_df)
    away_history = get_team_history(away_team, historical_df)

    std_home_team = standardize_team_name(home_team)
    std_away_team = standardize_team_name(away_team)

    if len(home_history) == 0 and len(away_history) == 0:
        st.warning(f"Skipping {home_team} vs {away_team}: No historical data for either team.")
        return None

    home_window = min(len(home_history), window_size)
    away_window = min(len(away_history), window_size)

    home_recent = home_history.head(home_window)
    away_recent = away_history.head(away_window)

    home_stats = {'mov': [], 'pts_for': [], 'pts_against': [], 'ou_hits': []}
    if home_window > 0:
        for _, game in home_recent.iterrows():
            ou_line_val = game.get('OU_Line', 0)
            if pd.isna(ou_line_val):
                ou_line_val = 0

            ou_hit = 1 if (game['HomeScore'] + game['AwayScore']) > ou_line_val else 0
            if std_home_team in game['HomeTeam'].lower():
                home_stats['mov'].append(game['HomeScore'] - game['AwayScore'])
                home_stats['pts_for'].append(game['HomeScore'])
                home_stats['pts_against'].append(game['AwayScore'])
                home_stats['ou_hits'].append(ou_hit)
            else:
                home_stats['mov'].append(game['AwayScore'] - game['HomeScore'])
                home_stats['pts_for'].append(game['AwayScore'])
                home_stats['pts_against'].append(game['HomeScore'])
                home_stats['ou_hits'].append(ou_hit)

    away_stats = {'mov': [], 'pts_for': [], 'pts_against': [], 'ou_hits': []}
    if away_window > 0:
        for _, game in away_recent.iterrows():
            ou_line_val = game.get('OU_Line', 0)
            if pd.isna(ou_line_val):
                ou_line_val = 0

            ou_hit = 1 if (game['HomeScore'] + game['AwayScore']) > ou_line_val else 0
            if std_away_team in game['AwayTeam'].lower():
                away_stats['mov'].append(game['AwayScore'] - game['HomeScore'])
                away_stats['pts_for'].append(game['AwayScore'])
                away_stats['pts_against'].append(game['HomeScore'])
                away_stats['ou_hits'].append(ou_hit)
            else:
                away_stats['mov'].append(game['HomeScore'] - game['AwayScore'])
                away_stats['pts_for'].append(game['HomeScore'])
                away_stats['pts_against'].append(game['HomeScore'])
                away_stats['ou_hits'].append(ou_hit)

    features = {
        'Home_Avg_MOV': np.mean(home_stats['mov']) if home_stats['mov'] else 0,
        'Home_Avg_Pts_For': np.mean(home_stats['pts_for']) if home_stats['pts_for'] else 0,
        'Home_Avg_Pts_Against': np.mean(home_stats['pts_against']) if home_stats['pts_against'] else 0,
        'Home_Avg_OU_Hit_Rate': np.mean(home_stats['ou_hits']) if home_stats['ou_hits'] else 0,
        'Away_Avg_MOV': np.mean(away_stats['mov']) if away_stats['mov'] else 0,
        'Away_Avg_Pts_For': np.mean(away_stats['pts_for']) if away_stats['pts_for'] else 0,
        'Away_Avg_Pts_Against': np.mean(away_stats['pts_against']) if away_stats['pts_against'] else 0,
        'Away_Avg_OU_Hit_Rate': np.mean(away_stats['ou_hits']) if away_stats['ou_hits'] else 0
    }
    
    features['Avg_MOV_Diff'] = features['Home_Avg_MOV'] - features['Away_Avg_MOV']
    features['Avg_Pts_For_Diff'] = features['Home_Avg_Pts_For'] - features['Away_Avg_Pts_For']
    features['Avg_Pts_Against_Diff'] = features['Home_Avg_Pts_Against'] - features['Away_Avg_Pts_Against']
    features['Avg_OU_Hit_Rate_Diff'] = features['Home_Avg_OU_Hit_Rate'] - features['Away_Avg_OU_Hit_Rate']
    
    return features

def generate_predictions(sport_key: str):
    st.info(f"Generating predictions for {sport_key}...")

    try:
        model = joblib.load('models/xgb_lgbm_rf_stacking_model.joblib')
        historical_df = pd.read_csv('data/raw/historical_basketball_data.csv', parse_dates=['Date'])
        for col in ['HomeScore', 'AwayScore', 'OU_Line']:
            historical_df[col] = pd.to_numeric(historical_df[col], errors='coerce')
        historical_df.dropna(subset=['HomeScore', 'AwayScore', 'OU_Line'], inplace=True)
    except FileNotFoundError as e:
        st.error(f"Error loading model or data: {e}.")
        return []

    upcoming_games = get_upcoming_games(sport_key)
    if not upcoming_games:
        st.warning(f"No upcoming games to predict for {sport_key}.")
        return []

    predictions = []
    
    for game in upcoming_games:
        home_team = game['home_team']
        away_team = game['away_team']
        
        ou_line = None
        bookmakers = game.get('bookmakers', [])
        preferred_books = ['draftkings', 'fanduel', 'betmgm', 'betonlineag', 'bovada']
        sorted_bookmakers = sorted(bookmakers, key=lambda b: (
            preferred_books.index(b['key']) if b['key'] in preferred_books else len(preferred_books),
            not any(market['key'] == 'totals' for market in b.get('markets', []))
        ))

        for bookmaker in sorted_bookmakers:
            for market in bookmaker.get('markets', []):
                if market['key'] == 'totals':
                    if market['outcomes']:
                        ou_line = market['outcomes'][0]['point']
                        break
            if ou_line:
                break
        
        if not ou_line:
            st.warning(f"Skipping {home_team} vs {away_team}: No OU_Line found from preferred bookmakers.")
            continue

        features = calculate_features_for_game(home_team, away_team, historical_df)
        
        if features is None:
            home_history_len = len(get_team_history(home_team, historical_df))
            away_history_len = len(get_team_history(away_team, historical_df))
            st.warning(f"Skipping {home_team} vs {away_team}: Not enough historical data (Home: {home_history_len}, Away: {away_history_len}).")
            continue

        feature_cols = [
            'Home_Avg_MOV', 'Home_Avg_Pts_For', 'Home_Avg_Pts_Against', 'Home_Avg_OU_Hit_Rate',
            'Away_Avg_MOV', 'Away_Avg_Pts_For', 'Away_Avg_Pts_Against', 'Away_Avg_OU_Hit_Rate',
            'Avg_MOV_Diff', 'Avg_Pts_For_Diff', 'Avg_Pts_Against_Diff', 'Avg_OU_Hit_Rate_Diff'
        ]
        feature_df = pd.DataFrame([features], columns=feature_cols)

        prediction_val = model.predict(feature_df)[0]
        prediction_proba = model.predict_proba(feature_df)[0]

        prediction_text = "Over" if prediction_val == 1 else "Under"
        probability = prediction_proba[1] if prediction_val == 1 else prediction_proba[0]

        predictions.append({
            'League': sport_key.replace('basketball_', '').upper(),
            'Match': f"{game['away_team']} at {game['home_team']}",
            'Prediction': f"{prediction_text} {ou_line}",
            'Probability': probability
        })

    st.success(f"Successfully generated {len(predictions)} predictions for {sport_key}.")
    return predictions


if __name__ == '__main__':
    all_predictions = []
    for league_name, sport_key in AVAILABLE_LEAGUES.items():
        predictions = generate_predictions(sport_key)
        if predictions:
            all_predictions.extend(predictions)
    
    if all_predictions:
        st.info("\n--- All Upcoming Predictions ---")
        pred_df = pd.DataFrame(all_predictions)
        st.dataframe(pred_df)
    else:
        st.info("\nNo predictions were generated for any league.")