# AI Bet Analyzer

## Project Description
The AI Bet Analyzer is a Streamlit-based web application designed to provide daily Over/Under predictions for basketball matches across various leagues. It leverages historical game data, real-time odds from The Odds API, and a trained machine learning model to generate probabilistic predictions.

## Features
-   **Multi-League Support**: Provides predictions for NCAA, NBA, and WNBA basketball games.
-   **Real-time Odds Integration**: Fetches upcoming game data and odds from The Odds API.
-   **Machine Learning Predictions**: Utilizes a pre-trained ensemble model (XGBoost, LightGBM, Random Forest) for Over/Under predictions.
-   **Dynamic Feature Engineering**: Calculates relevant features for each game based on recent team performance.
-   **Robust Team Name Standardization**: Handles variations in team names across different data sources.
-   **Handling Limited Historical Data**: Implements strategies to generate predictions even for teams with limited historical game records.
-   **Interactive User Interface**: A Streamlit interface allows users to generate predictions, filter by league, and sort by prediction probability.

## How it Works
The prediction process involves several key steps:

1.  **Data Acquisition**:
    *   **Historical Data**: A `historical_basketball_data.csv` file (located in `data/raw/`) contains past game results, scores, and over/under lines for various leagues.
    *   **Upcoming Games & Odds**: The `src/api_client.py` module connects to The Odds API (requiring an API key) to fetch details of upcoming matches, including participating teams and their over/under lines from various bookmakers.

2.  **Team Name Standardization**:
    *   `src/predict.py` contains a `TEAM_NAME_MAP` and a `standardize_team_name` function. This is crucial for matching team names from The Odds API (which can vary) to the standardized names used in the historical data (Covers.com format). This ensures that historical performance can be correctly linked to upcoming games.

3.  **Feature Engineering**:
    *   For each upcoming game, the `calculate_features_for_game` function in `src/predict.py` extracts relevant features. These features describe the recent form of both the home and away teams.
    *   **Features calculated include**: Average Margin of Victory (MOV), Average Points For, Average Points Against, and Average Over/Under Hit Rate (how often a team's games go 'Over' the line).
    *   **Handling Insufficient History**: If a team has fewer than the standard `window_size` (e.g., 10) historical games, the system uses all available history for that team. If no history is found for a team, its average statistics are defaulted to 0, ensuring that predictions can still be made without omitting the game entirely. Difference features (e.g., `Avg_MOV_Diff`) are also computed.

4.  **Machine Learning Prediction**:
    *   The project uses a pre-trained ensemble machine learning model, specifically `xgb_lgbm_rf_stacking_model.joblib` (located in `models/`). This model is loaded by `src/predict.py`.
    *   The engineered features for each upcoming game are fed into this model.
    *   The model outputs a prediction (either "Over" or "Under" for the given O/U line) and a probability associated with that prediction.

5.  **Prediction Presentation**:
    *   The `app.py` Streamlit application orchestrates the entire process.
    *   It calls `generate_predictions` for all supported leagues (NCAA, NBA, WNBA).
    *   Predictions are displayed in an interactive table, allowing users to filter by league and sort by the predicted probability (highest probability first by default).

## Setup and Installation (locally) otherwise use the webapp [https://ai-bet-analyzer.streamlit.app](https://ai-bet-analyzer.streamlit.app)

### Prerequisites
- Python 3.8+
- An API Key from [The Odds API](https://theoddsapi.com/)

### Steps
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your_username/AI-Bet-Analyzer.git
    cd AI-Bet-Analyzer
    ```
    (Note: Replace `https://github.com/your_username/AI-Bet-Analyzer.git` with the actual repository URL if this project is hosted.)

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **API Key Configuration:**
    *   This project is configured to use a pre-set API key for The Odds API. Therefore, you do not need to set up your own `.env` file or provide an API key.

## Usage

1.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

2.  **Access the app:** Open your web browser and navigate to the local URL displayed in your terminal (usually `http://localhost:8501`).

3.  **Generate Predictions**: Click the "Generate Today's Predictions" button. The app will fetch live odds, process data, and display predictions.

4.  **Filter and Sort**: Use the "Filter by League" dropdown and "Sort Predictions By" selectbox to refine your view of the predictions.

