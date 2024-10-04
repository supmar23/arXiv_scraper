import arxiv
import pandas as pd
from tqdm import tqdm 
import os

# construct custom API client
client = arxiv.Client(
  page_size = 100,
  delay_seconds = 10,
  num_retries = 5
)

# create the search query
search = arxiv.Search(
  query = "ti:\"prompt tuning\" OR ti:\"prompt-tuning\" OR ti:\"prefix tuning\" OR ti:\"prefix-tuning\" OR ti:\"prompt learning\" OR ti:\"soft prompt*\" OR ti:\"prompt* optimization\"",
  max_results = float('inf'), #API's limit is 300,000 results.
  sort_by = arxiv.SortCriterion.SubmittedDate,
  sort_order=arxiv.SortOrder.Ascending
)

year_start = int(input("year to search from (YYYY): "))
year_end = int(input("year to search to (YYYY): "))

# Check if the JSONL file already exists
file_path = "papers.jsonl"
if os.path.exists(file_path):
  # Load existing data
  df = pd.read_json(file_path, orient="records", lines=True)
else:
  # Create an empty DataFrame with the columns we want
  df = pd.DataFrame(columns=["ID", "Updated", "Published", "Title", "Authors", "Summary", "Comment", "Journal", "Primary Category", "Links", "Categories", "Url"])

# Print the number of records before appending new records
initial_record_count = df.shape[0]
print(f"Number of records before appending: {initial_record_count}")

# Create a dataframe with all the papers that match the search query
results = client.results(search)

for r in tqdm(results):
  authors = []
  categories = []
  links = []

  for author in r.authors:
    authors.append(str(author))

  for category in r.categories:
    categories.append(str(category))

  for link in r.links:
    links.append(str(link))

  if (r.published.year >= year_start and r.published.year <= year_end):
    # Append the data to the DataFrame
    new_row = pd.DataFrame([{
      "ID": str(r.entry_id),
      "Updated": str(r.updated),
      "Published": str(r.published),
      "Title": str(r.title),
      "Authors": ", ".join(str(author) for author in authors),
      "Summary": str(r.summary),
      "Comment": str(r.comment),
      "Journal": str(r.journal_ref),
      "Primary Category": str(r.primary_category),
      "Categories": ", ".join(str(category) for category in categories),
      "Links": ", ".join(str(link) for link in r.links),
      "Url": str(r.pdf_url)
    }])

    # populate the DataFrame with the new row
    df = pd.concat([df, new_row], ignore_index=True).drop_duplicates().reset_index(drop=True)

# Print the number of records after appending new records
final_record_count = df.shape[0]
print(f"Number of records after appending: {final_record_count}")

# Print only the newly appended records
new_records = df.iloc[initial_record_count:]
print("Newly appended records:")
print(new_records)

# convert to jsonl file
# df.to_json("papers.jsonl", orient="records", lines=True)

# convert to csv file
df.to_csv("./datasets/arXiv-papers-2021-only.csv", index=False)