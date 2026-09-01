import os
import json
import time
import requests
from datetime import datetime

# Define headers for HackerNews API requests
HEADERS = {
    "User-Agent": "TrendPulse/1.0"
}

# Category definition and keyword mapping for case-insensitive title matching
CATEGORY_KEYWORDS = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

def categorize_story(title):
    """
    Checks the title for keywords matching any defined category.
    Returns the first matching category name or None if no keywords match.
    """
    if not title:
        return None
        
    title_lower = title.lower()
    
    # Loop through categories and match word-level or substring keywords
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category
    return None

def fetch_top_stories():
    """
    Fetches top 500 story IDs from the HackerNews API.
    """
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    try:
        response = requests.get(top_stories_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        story_ids = response.json()
        return story_ids[:500]  # Get the top 500 story IDs
    except requests.RequestException as e:
        print(f"Failed to retrieve top story IDs: {e}")
        return []

def main():
    # Step 1: Fetch top 500 story IDs
    print("Fetching top story IDs from HackerNews API...")
    story_ids = fetch_top_stories()
    
    if not story_ids:
        print("No story IDs fetched. Exiting script.")
        return

    collected_stories = []

    # Step 2: Fetch individual story details and categorize them
    print("Fetching story details...")
    for story_id in story_ids:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        
        try:
            response = requests.get(item_url, headers=HEADERS, timeout=5)
            if response.status_code != 200:
                print(f"Failed to fetch story {story_id}, moving on...")
                continue
                
            story_data = response.json()
            if not story_data or story_data.get("type") != "story":
                continue

            # Extract fields safely using .get() to prevent missing key errors
            title = story_data.get("title", "")
            category = categorize_story(title)

            # Skip stories that do not match any defined category keywords
            if not category:
                continue

            # Construct the structured dictionary required
            story_record = {
                "post_id": story_data.get("id"),
                "title": title,
                "category": category,
                "score": story_data.get("score", 0),
                "num_comments": story_data.get("descendants", 0),
                "author": story_data.get("by", ""),
                "collected_at": datetime.now().isoformat()
            }
            
            collected_stories.append(story_record)

        except requests.RequestException as e:
            # Handle request failures gracefully without crashing the script
            print(f"Error fetching item {story_id}: {e}. Skipping...")
            continue

    # Step 3: Save results to the data/ directory in JSON format
    os.makedirs("data", exist_ok=True)
    
    date_str = datetime.now().strftime("%Y%m%d")
    file_path = f"data/trends_{date_str}.json"

    # Save collected list to JSON file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(collected_stories, f, indent=4)

    # Print summary output statement
    print(f"Collected {len(collected_stories)} stories. Saved to {file_path}")

    # Optional requirement delay if processing per-category loop iteration
    time.sleep(2)

if __name__ == "__main__":
    main()
