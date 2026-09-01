import os
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # -------------------------------------------------------------
    # 1. Setup (2 marks)
    # -------------------------------------------------------------
    csv_file_path = "data/trends_analysed.csv"
    
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"Could not find {csv_file_path}. Please run Task 3 first.")
        
    df = pd.read_csv(csv_file_path)
    
    # Create output directory if it doesn't exist
    os.makedirs("outputs", exist_ok=True)

    # -------------------------------------------------------------
    # 2. Chart 1: Top 10 Stories by Score (6 marks)
    # -------------------------------------------------------------
    # Get top 10 stories by score and sort ascending for display in horizontal bar chart
    top10_df = df.nlargest(10, "score").sort_values("score", ascending=True)
    
    # Truncate titles longer than 50 characters
    shortened_titles = [
        title[:47] + "..." if len(str(title)) > 50 else str(title)
        for title in top10_df["title"]
    ]
    
    plt.figure(figsize=(10, 6))
    plt.barh(shortened_titles, top10_df["score"], color="skyblue")
    plt.title("Top 10 Stories by Score")
    plt.xlabel("Score (Upvotes)")
    plt.ylabel("Story Title")
    plt.tight_layout()
    
    # Save chart before showing
    plt.savefig("outputs/chart1_top_stories.png", dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 3. Chart 2: Stories per Category (6 marks)
    # -------------------------------------------------------------
    category_counts = df["category"].value_counts()
    categories = category_counts.index
    counts = category_counts.values
    
    # Distinct colors for each bar
    colors = ["#4c72b0", "#55a868", "#c44e52", "#8172b1", "#ccb974"]
    
    plt.figure(figsize=(8, 5))
    plt.bar(categories, counts, color=colors[:len(categories)])
    plt.title("Number of Stories per Category")
    plt.xlabel("Category")
    plt.ylabel("Story Count")
    plt.tight_layout()
    
    # Save chart before showing
    plt.savefig("outputs/chart2_categories.png", dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # 4. Chart 3: Score vs Comments (6 marks)
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 6))
    
    # Separate popular vs non-popular stories based on is_popular boolean column
    popular = df[df["is_popular"] == True]
    non_popular = df[df["is_popular"] == False]
    
    plt.scatter(non_popular["score"], non_popular["num_comments"], color="gray", alpha=0.6, label="Non-Popular")
    plt.scatter(popular["score"], popular["num_comments"], color="crimson", alpha=0.8, label="Popular")
    
    plt.title("Score vs. Number of Comments")
    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.legend()
    plt.tight_layout()
    
    # Save chart before showing
    plt.savefig("outputs/chart3_scatter.png", dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # Bonus — Dashboard (+3 marks)
    # -------------------------------------------------------------
    # Create 2x2 subplot layout to combine all 3 charts
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("TrendPulse Dashboard", fontsize=18, fontweight="bold")

    # Subplot 1: Top 10 Stories (Top-Left)
    axes[0, 0].barh(shortened_titles, top10_df["score"], color="skyblue")
    axes[0, 0].set_title("Top 10 Stories by Score")
    axes[0, 0].set_xlabel("Score (Upvotes)")
    axes[0, 0].set_ylabel("Story Title")

    # Subplot 2: Stories per Category (Top-Right)
    axes[0, 1].bar(categories, counts, color=colors[:len(categories)])
    axes[0, 1].set_title("Number of Stories per Category")
    axes[0, 1].set_xlabel("Category")
    axes[0, 1].set_ylabel("Story Count")

    # Subplot 3: Score vs Comments (Bottom-Left)
    axes[1, 0].scatter(non_popular["score"], non_popular["num_comments"], color="gray", alpha=0.6, label="Non-Popular")
    axes[1, 0].scatter(popular["score"], popular["num_comments"], color="crimson", alpha=0.8, label="Popular")
    axes[1, 0].set_title("Score vs. Number of Comments")
    axes[1, 0].set_xlabel("Score")
    axes[1, 0].set_ylabel("Number of Comments")
    axes[1, 0].legend()

    # Hide unused 4th subplot cell (Bottom-Right)
    axes[1, 1].axis("off")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Save combined dashboard
    plt.savefig("outputs/dashboard.png", dpi=300)
    plt.close()

    print("Successfully generated all visualisations:")
    print(" - outputs/chart1_top_stories.png")
    print(" - outputs/chart2_categories.png")
    print(" - outputs/chart3_scatter.png")
    print(" - outputs/dashboard.png (bonus)")

if __name__ == "__main__":
    main()