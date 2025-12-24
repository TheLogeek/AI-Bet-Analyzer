from flashscore_scraper import FlashscoreScraper

def test_scraper():
    """
    Tests the flashscore-scraper package to see if it can fetch basketball data and odds.
    """
    print("--- Testing flashscore-scraper package ---")
    
    try:
        # Initialize the scraper
        # Based on the GitHub repo, it might require a config file or direct parameters.
        # Let's try to initialize it and call its main scraping function.
        # The library seems to be football-focused, so this might fail.
        
        scraper = FlashscoreScraper()
        
        print("Scraper initialized. Attempting to get data for basketball...")

        # The key is to find the right method and parameters.
        # Looking at the source code of the library is often necessary if docs are sparse.
        # Let's assume a method like `get_matches` or `scrape_season` might exist.
        # A common pattern is to specify sport, country, league, and season.
        
        # This is a speculative call. It will likely need adjustment.
        # We'll try to get data for the Chinese CBA for the 2022-2023 season.
        matches = scraper.get_matches(
            sport="basketball", 
            country="china", 
            league="cba", 
            season="2022-2023"
        )
        
        if matches:
            print(f"Successfully fetched {len(matches)} matches.")
            print("--- Example Match ---")
            
            # We need to inspect the structure of the returned match objects
            first_match = matches[0]
            print(first_match)
            
            # CRITICAL: Check if odds are included.
            if hasattr(first_match, 'odds'):
                print("\nSUCCESS: Odds data found in the match object!")
            else:
                print("\nFAILURE: Odds data NOT found in the match object.")

        else:
            print("Did not fetch any matches. The library might not support basketball out-of-the-box, or the parameters are incorrect.")

    except Exception as e:
        print(f"\nAn error occurred while testing the scraper: {e}")
        print("This likely means the library does not support basketball out-of-the-box, or the usage is incorrect.")

if __name__ == '__main__':
    test_scraper()
