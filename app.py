import streamlit as st
import pandas as pd
from src.predict import generate_predictions
from src.api_client import AVAILABLE_LEAGUES
import os
import datetime

CACHE_FILE = "data/processed/cached_predictions.csv"

def get_all_predictions():
<<<<<<< HEAD
    """Runs the prediction pipeline for all available leagues, using file-based caching."""
    today = datetime.date.today()
    all_preds_from_cache = []

    if os.path.exists(CACHE_FILE):
        file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(CACHE_FILE)).date()
        if file_mod_time == today:
            st.info("Loading predictions from cache for today.")
            try:
                cached_df = pd.read_csv(CACHE_FILE)
                cached_df['Probability'] = pd.to_numeric(cached_df['Probability'], errors='coerce')
                all_preds_from_cache = cached_df.to_dict('records')
                if all_preds_from_cache:
                    return all_preds_from_cache
                else:
                    st.warning("Cache file was empty. Regenerating predictions.")
            except Exception as e:
                st.error(f"Error loading from cache: {e}. Regenerating predictions.")
        else:
            st.info(f"Cache file is from {file_mod_time}, regenerating predictions for {today}.")
    else:
        st.info("No cache file found. Generating new predictions.")

    all_preds_new = []
    for league_name, sport_key in AVAILABLE_LEAGUES.items():
        st.write(f"Fetching predictions for {league_name}...")
        preds = generate_predictions(sport_key)
        if preds:
            all_preds_new.extend(preds)

    if all_preds_new:
        cache_df = pd.DataFrame(all_preds_new)
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        cache_df.to_csv(CACHE_FILE, index=False)
        st.success(f"Generated and cached {len(all_preds_new)} new predictions.")
    else:
        st.warning("No predictions generated for any league today.")

    return all_preds_new

def main():
    """Streamlit application main function."""
    st.set_page_config(
        page_title="AI Bet Analyzer",
        page_icon="🏀",
        layout="wide"
    )
    all_preds = []
    for league_name, sport_key in AVAILABLE_LEAGUES.items():
        st.write(f"Fetching predictions for {league_name}...")
        preds = generate_predictions(sport_key)
        if preds:
            all_preds.extend(preds)
    return all_preds

def main():
    """
    The main function to run the Streamlit application.
    """
    st.set_page_config(
        page_title="AI Bet Analyzer",
        page_icon="🏀",
        layout="wide"
    )

    st.title("🏀 AI Bet Analyzer")
    st.write("Get daily Over/Under predictions for basketball matches, powered by a hybrid ML model.")

    if 'predictions' not in st.session_state:
        st.session_state['predictions'] = None
    
    col1, col2 = st.columns([1, 2])

    with col1:
        if st.button("Generate Today's Predictions", key="generate"):
            with st.spinner("🧠 Generating new predictions for all leagues... This may take a moment."):
                st.session_state['predictions'] = get_all_predictions()

    if st.session_state['predictions'] is not None:
        all_predictions_df = pd.DataFrame(st.session_state['predictions'])
        
        if not all_predictions_df.empty:
            sport_key_to_league_name = {v: k for k, v in AVAILABLE_LEAGUES.items()}
            
            display_league_names = ["All"] + sorted(AVAILABLE_LEAGUES.keys())
            selected_display_name = st.selectbox("Filter by League", display_league_names)

            st.header("Today's Predictions")
            
            if selected_display_name != "All":
                selected_sport_key = AVAILABLE_LEAGUES[selected_display_name]
                display_df = all_predictions_df[all_predictions_df['League'] == selected_sport_key.replace('basketball_', '').upper()]
            else:
                display_df = all_predictions_df
            
            sort_order = st.selectbox(
                "Sort Predictions By:",
                ["Highest Probability First", "Lowest Probability First", "Default Order"],
                index=0
            )

            if sort_order == "Highest Probability First":
                display_df = display_df.sort_values(by='Probability', ascending=False)
            elif sort_order == "Lowest Probability First":
                display_df = display_df.sort_values(by='Probability', ascending=True)

            if not display_df.empty:
                st.dataframe(display_df.style.format({'Probability': '{:.2%}'}), width='stretch')
            else:
                st.warning(f"No predictions available for {selected_display_name} in the generated data.")
        else:
            st.info("No predictions were available for any league today.")
    else:
        st.info("Click the 'Generate Today's Predictions' button to begin.")
=======
    # Initialize session state for predictions
    if 'predictions' not in st.session_state:
        st.session_state['predictions'] = None

    # --- Main content area with controls ---

    col1, col2 = st.columns([1, 2]) # Adjust column ratio as needed

    with col1:
        if st.button("Generate Today's Predictions", key="generate"):
            # Clear previous predictions and run the pipeline
            with st.spinner("🧠 Generating new predictions for all leagues... This may take a moment."):
                st.session_state['predictions'] = get_all_predictions()
            st.success("Predictions generated!") # Changed to st.success for visibility

    # --- Main content area ---
    if st.session_state['predictions'] is not None:
        all_predictions_df = pd.DataFrame(st.session_state['predictions'])

        if not all_predictions_df.empty:
            # Create a reverse mapping for display purposes
            sport_key_to_league_name = {v: k for k, v in AVAILABLE_LEAGUES.items()}

            # League selection dropdown in the main area, after the button
            display_league_names = ["All"] + sorted(AVAILABLE_LEAGUES.keys())
            selected_display_name = st.selectbox("Filter by League", display_league_names)

            st.header("Today's Predictions")

            # Filter DataFrame based on selection
            if selected_display_name != "All":
                selected_sport_key = AVAILABLE_LEAGUES[selected_display_name]
                # Ensure exact match for League column (e.g., 'NBA', 'NCAAB')
                display_df = all_predictions_df[all_predictions_df['League'] == selected_sport_key.replace('basketball_', '').upper()]
            else:
                display_df = all_predictions_df

            # Add sorting option
            sort_order = st.selectbox(
                "Sort Predictions By:",
                ["Highest Probability First", "Lowest Probability First", "Default Order"],
                index=0 # Default to "Highest Probability First"
            )

            # Apply sorting
            if sort_order == "Highest Probability First":
                display_df = display_df.sort_values(by='Probability', ascending=False)
            elif sort_order == "Lowest Probability First":
                display_df = display_df.sort_values(by='Probability', ascending=True)
            # Else: display_df remains as filtered, no explicit sort applied for "Default Order"

            if not display_df.empty:
                # Display the DataFrame without the index, ensuring Probability is formatted as percentage
                st.dataframe(display_df.style.format({'Probability': '{:.2%}'}), width='stretch')
            else:
                st.warning(f"No predictions available for {selected_display_name} in the generated data.")
        else:
            st.info("No predictions were available for any league today.")
    else:
        st.info("Click the 'Generate Today's Predictions' button to begin.")



if __name__ == "__main__":
    main()