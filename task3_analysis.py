import os
import numpy as np
import pandas as pd

def main():
    # -------------------------------------------------------------
    # 1. Load and Explore (4 marks)
    # -------------------------------------------------------------
    csv_file_path = "data/trends_clean.csv"
    
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"Could not find {csv_file_path}. Please run Task 2 first.")
        
    df = pd.read_csv(csv_file_path)
    
    # Print the shape of the DataFrame (rows and columns)
    print(f"Loaded data: {df.shape}\n")
    
    # Print the first 5 rows
    print("First 5 rows:")
    print(df.head())
    print()
    
    # Compute average score and comments using Pandas/NumPy
    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()
    
    print(f"Average score   : {avg_score:,.0f}")
    print(f"Average comments: {avg_comments:,.0f}\n")

    # -------------------------------------------------------------
    # 2. Basic Analysis with NumPy (8 marks)
    # -------------------------------------------------------------
    print("--- NumPy Stats ---")
    
    # Extract numerical series into NumPy arrays
    scores_array = df["score"].to_numpy()
    comments_array = df["num_comments"].to_numpy()
    
    # Calculate statistics using NumPy functions
    mean_score = np.mean(scores_array)
    median_score = np.median(scores_array)
    std_score = np.std(scores_array)
    max_score = np.max(scores_array)
    min_score = np.min(scores_array)
    
    print(f"Mean score     : {mean_score:,.0f}")
    print(f"Median score   : {median_score:,.0f}")
    print(f"Std deviation  : {std_score:,.0f}")
    print(f"Max score      : {max_score:,.0f}")
    print(f"Min score      : {min_score:,.0f}\n")
    
    # Find category with the most stories
    top_category = df["category"].mode()[0]
    top_category_count = (df["category"] == top_category).sum()
    print(f"Most stories in: {top_category} ({top_category_count} stories)\n")
    
    # Find story with the most comments
    max_comments_idx = np.argmax(comments_array)
    most_commented_story = df.iloc[max_comments_idx]
    most_commented_title = most_commented_story["title"]
    most_commented_count = most_commented_story["num_comments"]
    
    print(f'Most commented story: "{most_commented_title}" - {most_commented_count:,} comments\n')

    # -------------------------------------------------------------
    # 3. Add New Columns (5 marks)
    # -------------------------------------------------------------
    # Calculate engagement: num_comments / (score + 1)
    df["engagement"] = df["num_comments"] / (df["score"] + 1)
    
    # Calculate is_popular: True if score > average score, else False
    df["is_popular"] = df["score"] > mean_score

    # -------------------------------------------------------------
    # 4. Save the Result (3 marks)
    # -------------------------------------------------------------
    output_path = "data/trends_analysed.csv"
    df.to_csv(output_path, index=False)
    
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()