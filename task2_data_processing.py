import os
import glob
import pandas as pd

def find_latest_json_file(data_dir="data"):
    """
    Finds and returns the path of the latest JSON file matching 'trends_YYYYMMDD.json' 
    in the specified data directory.
    """
    json_files = glob.glob(os.path.join(data_dir, "trends_*.json"))
    if not json_files:
        raise FileNotFoundError("No JSON files matching 'data/trends_*.json' were found.")
    
    # Sort files by name/date to get the most recent file
    json_files.sort()
    return json_files[-1]

def main():
    # -------------------------------------------------------------
    # 1. Load the JSON File (4 marks)
    # -------------------------------------------------------------
    json_file_path = find_latest_json_file()
    
    # Load JSON file into a Pandas DataFrame
    df = pd.read_json(json_file_path)
    print(f"Loaded {len(df)} stories from {json_file_path}\n")

    # -------------------------------------------------------------
    # 2. Clean the Data (10 marks)
    # -------------------------------------------------------------
    # Duplicates — remove any rows with the same post_id
    df = df.drop_duplicates(subset=["post_id"])
    print(f"After removing duplicates: {len(df)}")

    # Missing values — drop rows where post_id, title, or score is missing
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # Low quality — remove stories where score is less than 5
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}\n")

    # Data types — make sure score and num_comments are integers
    df["score"] = df["score"].fillna(0).astype(int)
    df["num_comments"] = df["num_comments"].fillna(0).astype(int)

    # Whitespace — strip extra spaces from the title column
    df["title"] = df["title"].astype(str).str.strip()

    # -------------------------------------------------------------
    # 3. Save as CSV (6 marks)
    # -------------------------------------------------------------
    output_csv_path = "data/trends_clean.csv"
    
    # Ensure data directory exists before saving
    os.makedirs("data", exist_ok=True)
    
    # Save the cleaned DataFrame to CSV without the index column
    df.to_csv(output_csv_path, index=False)
    print(f"Saved {len(df)} rows to {output_csv_path}\n")

    # Print quick summary: number of stories per category
    print("Stories per category:")
    category_counts = df["category"].value_counts()
    for category, count in category_counts.items():
        print(f"  {category:<15} {count}")

if __name__ == "__main__":
    main()