import pandas as pd
import numpy as np

def clean_data(df):
    """
    Cleans the raw scraped data.
    """
    df.dropna(subset=['HomeScore', 'AwayScore', 'OU_Line'], inplace=True)
    for col in ['HomeScore', 'AwayScore', 'OU_Line']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=['HomeScore', 'AwayScore', 'OU_Line'], inplace=True)
    df['TotalPoints'] = df['HomeScore'] + df['AwayScore']
    df['OU_Result'] = (df['TotalPoints'] > df['OU_Line']).astype(int)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def calculate_advanced_rolling_stats(df, window_size=10):
    """
    Calculates advanced rolling statistics for each team, including MOV and OU performance.
    """
    df = df.sort_values('Date').reset_index(drop=True)
    
    team_history = {}
    
    # Lists to store the calculated rolling stats
    rolling_stats = []

    for index, row in df.iterrows():
        home_team = row['HomeTeam']
        away_team = row['AwayTeam']
        
        home_stats = {'mov': np.nan, 'pts_for': np.nan, 'pts_against': np.nan, 'ou_hits': np.nan}
        away_stats = {'mov': np.nan, 'pts_for': np.nan, 'pts_against': np.nan, 'ou_hits': np.nan}

        # --- Calculate stats for Home Team ---
        if home_team in team_history and len(team_history[home_team]) >= window_size:
            history = team_history[home_team][-window_size:]
            home_stats['mov'] = np.mean([g['mov'] for g in history])
            home_stats['pts_for'] = np.mean([g['pts_for'] for g in history])
            home_stats['pts_against'] = np.mean([g['pts_against'] for g in history])
            home_stats['ou_hits'] = np.mean([g['ou_hit'] for g in history])
            
        # --- Calculate stats for Away Team ---
        if away_team in team_history and len(team_history[away_team]) >= window_size:
            history = team_history[away_team][-window_size:]
            away_stats['mov'] = np.mean([g['mov'] for g in history])
            away_stats['pts_for'] = np.mean([g['pts_for'] for g in history])
            away_stats['pts_against'] = np.mean([g['pts_against'] for g in history])
            away_stats['ou_hits'] = np.mean([g['ou_hit'] for g in history])

        rolling_stats.append({
            'Home_Avg_MOV': home_stats['mov'], 'Home_Avg_Pts_For': home_stats['pts_for'], 
            'Home_Avg_Pts_Against': home_stats['pts_against'], 'Home_Avg_OU_Hit_Rate': home_stats['ou_hits'],
            'Away_Avg_MOV': away_stats['mov'], 'Away_Avg_Pts_For': away_stats['pts_for'],
            'Away_Avg_Pts_Against': away_stats['pts_against'], 'Away_Avg_OU_Hit_Rate': away_stats['ou_hits']
        })

        # --- Update history for both teams ---
        ou_hit = 1 if (row['HomeScore'] + row['AwayScore']) > row['OU_Line'] else 0
        
        if home_team not in team_history: team_history[home_team] = []
        team_history[home_team].append({
            'mov': row['HomeScore'] - row['AwayScore'], 
            'pts_for': row['HomeScore'], 'pts_against': row['AwayScore'], 'ou_hit': ou_hit
        })
        
        if away_team not in team_history: team_history[away_team] = []
        team_history[away_team].append({
            'mov': row['AwayScore'] - row['HomeScore'], 
            'pts_for': row['AwayScore'], 'pts_against': row['HomeScore'], 'ou_hit': ou_hit
        })

    stats_df = pd.DataFrame(rolling_stats)
    df = pd.concat([df, stats_df], axis=1)
    
    df.dropna(inplace=True)
    return df

def main():
    """
    Main function to run the feature engineering pipeline.
    """
    print("Starting advanced feature engineering...")
    
    try:
        raw_df = pd.read_csv('data/raw/historical_basketball_data.csv')
        print(f"Loaded {len(raw_df)} games from raw data.")
    except FileNotFoundError:
        print("Error: 'data/raw/historical_basketball_data.csv' not found.")
        return

    cleaned_df = clean_data(raw_df.copy())
    print(f"Data cleaned. {len(cleaned_df)} games remaining.")
    
    featured_df = calculate_advanced_rolling_stats(cleaned_df.copy())
    print(f"Advanced rolling stats calculated. {len(featured_df)} games remaining.")
    
    # Add new difference features
    featured_df['Avg_MOV_Diff'] = featured_df['Home_Avg_MOV'] - featured_df['Away_Avg_MOV']
    featured_df['Avg_Pts_For_Diff'] = featured_df['Home_Avg_Pts_For'] - featured_df['Away_Avg_Pts_For']
    featured_df['Avg_Pts_Against_Diff'] = featured_df['Home_Avg_Pts_Against'] - featured_df['Away_Avg_Pts_Against']
    featured_df['Avg_OU_Hit_Rate_Diff'] = featured_df['Home_Avg_OU_Hit_Rate'] - featured_df['Away_Avg_OU_Hit_Rate']
    
    output_path = 'data/processed/featured_basketball_data_advanced.csv'
    featured_df.to_csv(output_path, index=False)
    
    print(f"Feature engineering complete. Processed data saved to '{output_path}'.")
    print("\nFinal DataFrame columns:")
    print(featured_df.columns)
    print("\nFirst 5 rows of the processed data:")
    print(featured_df.head())


if __name__ == "__main__":
    main()