# Import necessary libraries
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import logging

# Step 1: Set up logging
logging.basicConfig(filename='race_related_analysis.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Script started')

# Step 2: Define the directory and file pattern
directory_path = "/cwork/bk203/cleaned_files"  # Update this path as needed
file_pattern = "*.csv"
all_files = glob.glob(os.path.join(directory_path, file_pattern))
logging.info(f'Found {len(all_files)} files to process')

# Step 3: Initialize an empty DataFrame to store results
all_data = pd.DataFrame()

# Step 4: Loop through all files to identify "race-related" papers and aggregate results
for file in all_files:
    try:
        # Load each file
        temp_df = pd.read_csv(file)
        logging.info(f"Processing file: {file}, Columns: {list(temp_df.columns)}")
        
        # Identify race-related papers using regular expressions
        race_related_pattern = r'advantaged-group[a-zA-Z]{0,1}|advantaged group[a-zA-Z]{0,1}|dominant group[a-zA-Z]{0,1}|dominant-group[a-zA-Z]{0,1}|people-of-colo[a-zA-Z]{0,1}r|non-white[a-zA-Z]{0,1}|colored[a-zA-Z]{0,1}|caste[a-zA-Z]{0,1}|disadvantaged minor[a-zA-Z]{0,5}|people of colo[a-zA-Z]{0,1}r|rac[a-zA-Z]{0,3}|person[a-zA-Z]{0,1} of color[a-zA-Z]{0,1}|ethnic[a-zA-Z]{0,4}|underrepresented minorit[a-zA-Z]{0,3}|non-western[a-zA-Z]{0,1}|african-american[a-zA-Z]{0,1}|african american[a-zA-Z]{0,1}|black[a-zA-Z]{0,1}|negro[a-zA-Z]{0,2}|black-american[a-zA-Z]{0,1}|black american[a-zA-Z]{0,1}'
        temp_df["is_race_related"] = temp_df["title"].str.contains(race_related_pattern, case=False, na=False)
        
        # Filter only race-related papers
        race_related_papers = temp_df[temp_df["is_race_related"]]
        
        # Group by publication year and count
        if "publication_year" in temp_df.columns:
            yearly_counts = temp_df.groupby("publication_year").size().reset_index(name="total_papers")
            race_related_counts = race_related_papers.groupby("publication_year").size().reset_index(name="race_related_count")
            yearly_data = pd.merge(yearly_counts, race_related_counts, on="publication_year", how="left").fillna(0)
            all_data = pd.concat([all_data, yearly_data], ignore_index=True)
            logging.info(f"Processed file: {file} - Race-related papers found: {len(race_related_papers)}")
        else:
            logging.warning(f"'publication_year' not found in file: {file}")
    except Exception as e:
        logging.error(f"Error processing file: {file}, Error: {e}")

# Step 5: Save all_data to a CSV file
if not all_data.empty:
    all_data.to_csv("all_race_related_data.csv", index=False)
    logging.info("Saved all race-related data to 'all_race_related_data.csv'")
else:
    logging.warning("No race-related data to save")

# Step 6: Aggregate counts across all files by publication year
if not all_data.empty:
    total_yearly_counts = all_data.groupby("publication_year").agg({"total_papers": "sum", "race_related_count": "sum"}).reset_index()
    total_yearly_counts["share_race_related"] = total_yearly_counts["race_related_count"] / total_yearly_counts["total_papers"]

    # Step 7: Plot the time trend of the share of race-related papers
    plt.figure(figsize=(10, 6))
    plt.plot(total_yearly_counts["publication_year"], total_yearly_counts["share_race_related"], marker='o')
    plt.xlabel('Publication Year')
    plt.ylabel('Share of Race-Related Papers')
    plt.title('')
    plt.xticks(total_yearly_counts["publication_year"], rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("race_related_papers_share_trend.png")  # Save the plot
    logging.info("Saved plot to 'race_related_papers_share_trend.png'")
    plt.show()
else:
    logging.warning("No race-related papers found in the available files.")

logging.info('Script finished')
