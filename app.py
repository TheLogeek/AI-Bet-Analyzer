import streamlit as st
import pandas as pd
from datetime import date
from src.predict import generate_predictions
from src.api_client import AVAILABLE_LEAGUES


@st.cache_data(ttl=3600)  # Cache for 1 hour, date-aware
def get_all_predictions(today):
    """
    Runs the prediction pipeline for all available leagues.
    Cached per day to avoid stale or empty production data.
    """
    all_preds = []
    for _, sport_key in AVAILABLE_LEAGUES.items():
        preds = generate_predictions(sport_key)
        if preds:
            all_preds.extend(preds)
    return all_preds


def main():
    st.set_page_config(
        page_title="AI Bet Analyzer",
        page_icon="🏀",
        layout="wide"
    )

    st.title("🏀 AI Bet Analyzer")
    st.write("Get daily Over/Under predictions for basketball matches, powered by a hybrid ML model.")

    # Initialize session state
    if 'predictions' not in st.session_state:
        st.session_state['predictions'] = None

    col1, col2 = st.columns([1, 2])

    with col1:
        if st.button("Generate Today's Predictions", key="generate"):
            with st.spinner("🧠 Generating new predictions for all leagues... This may take a moment."):
                today = date.today().isoformat()
                st.session_state['predictions'] = get_all_predictions(today)
            st.success("Predictions generated!")

    # --- Main content area ---
    if st.session_state['predictions'] is not None:
        all_predictions_df = pd.DataFrame(st.session_state['predictions'])

        if not all_predictions_df.empty:

            display_league_names = ["All"] + sorted(AVAILABLE_LEAGUES.keys())
            selected_display_name = st.selectbox("Filter by League", display_league_names)

            st.header("Today's Predictions")

            # Safe league filtering (deployment-proof)
            if selected_display_name != "All":
                selected_sport_key = AVAILABLE_LEAGUES[selected_display_name]
                league_code = selected_sport_key.replace('basketball_', '').upper()

                display_df = all_predictions_df[
                    all_predictions_df['League'].str.contains(
                        league_code, case=False, na=False
                    )
                ]
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
                st.dataframe(
                    display_df.style.format({'Probability': '{:.2%}'}),
                    width='stretch'
                )
            else:
                st.warning(f"No predictions available for {selected_display_name}.")

        else:
            st.info("No predictions were available for any league today.")
    else:
        st.info("Click the 'Generate Today's Predictions' button to begin.")


if __name__ == "__main__":
    main()
