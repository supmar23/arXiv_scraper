import pandas as pd
from tqdm import tqdm 
import os

# Load the dataset
dfArxiv2021 = pd.read_csv("./datasets/arXiv-papers-2021-only.csv")
dfScopus = pd.read_csv("./datasets/scopus-papers.csv")

print("number of arXiv papers: " + str(dfArxiv2021.shape[0]))
print("number of scopus paper: " + str(dfScopus.shape[0]))
print("total papers of two datasets before merging: ", str(dfArxiv2021.shape[0] + dfScopus.shape[0]))

print("\n")

print("duplicate papers:")
# Find duplicates based on the 'Title' column
duplicates_df = pd.concat([dfArxiv2021, dfScopus])
duplicates_df = duplicates_df[duplicates_df.duplicated(subset='Title', keep=False)]
print(duplicates_df["Title"])

# Merge the datasets based on the 'Title' column and remove duplicates
merged_df = pd.concat([dfArxiv2021, dfScopus]).drop_duplicates(subset='Title').reset_index(drop=True)

print("\n")

# Save the merged dataset to a new CSV file
merged_df.to_csv("./datasets/merged-papers.csv", index=False)
print("number of paper after merge: " + str(merged_df.shape[0]))

# Save the merged dataset to a new JSONL file
merged_df.to_json("./datasets/merged-papers.jsonl", orient="records", lines=True)