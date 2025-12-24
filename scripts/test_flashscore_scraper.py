from flashscore_scraper import FlashscoreScraper

def test_scraper():
    """Tests the flashscore-scraper package for basketball data and odds."""
    print("--- Testing flashscore-scraper package ---")
    
    try:
        scraper = FlashscoreScraper()
        
        print("Scraper initialized. Attempting to get data for basketball...")

        matches = scraper.get_matches(
            sport="basketball", 
            country="china", 
            league="cba", 
            season="2022-2023"
        )
        
        if matches:
            print(f"Successfully fetched {len(matches)} matches.")
            print("--- Example Match ---")
            
            first_match = matches[0]
            print(first_match)
            
            if hasattr(first_match, 'odds'):
                print("SUCCESS: Odds data found in the match object!")
            else:
                print("FAILURE: Odds data NOT found in the match object.")

        else:
            print("Did not fetch any matches. The library might not support basketball out-of-the-box, or the parameters are incorrect.")

    except Exception as e:
        print(f"An error occurred while testing the scraper: {e}")
        print("This likely means the library does not support basketball out-of-the-box, or the usage is incorrect.")

if __name__ == '__main__':
    test_scraper()
