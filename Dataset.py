import pandas as pd
import html
import re

# Define the number of lines to read and clean (adjust as needed)
num_lines_to_clean = 900000  # Adjust as needed

# Load the CSV file into a DataFrame, reading only the specified number of lines
df = pd.read_csv('enwiki-20170820.csv', nrows=num_lines_to_clean)

# Drop rows with missing values in ARTICLE_ID or TITLE columns
df.dropna(subset=['ARTICLE_ID', 'TITLE'], inplace=True)

# Remove leading and trailing whitespaces from TITLE, SECTION_TITLE, and SECTION_TEXT columns
df['TITLE'] = df['TITLE'].str.strip()
df['SECTION_TITLE'] = df['SECTION_TITLE'].str.strip()
df['SECTION_TEXT'] = df['SECTION_TEXT'].str.strip()

# Clean text columns that may contain special characters or HTML entities
text_columns = ['TITLE', 'SECTION_TITLE', 'SECTION_TEXT']
for col in text_columns:
    df[col] = df[col].apply(lambda x: html.unescape(x) if isinstance(x, str) else x)
    df[col] = df[col].apply(lambda x: x.encode('latin1', errors='ignore').decode('utf8', errors='ignore') if isinstance(x, str) else x)
    df[col] = df[col].apply(lambda x: re.sub(r'[\u2018\u2019]', "'", x) if isinstance(x, str) else x)  # Replace curly quotes

# Remove duplicate rows again after cleaning
df.drop_duplicates(inplace=True)

# Remove patterns like "===Origins===", "'''''", ":''", and "* " from text columns using regular expressions
pattern1 = re.compile(r'=+\s*([^=]+)\s*=+')  # Remove ===Origins===
pattern2 = re.compile(r"''+")
pattern3 = re.compile(r':[ ]*')
pattern4 = re.compile(r'\* ')
pattern5 = re.compile(r'[^\x00-\x7F]+')  # Matches non-ASCII characters
for col in text_columns:
    df[col] = df[col].apply(lambda x: pattern1.sub(r'\1', x) if isinstance(x, str) else x)
    df[col] = df[col].apply(lambda x: pattern2.sub('', x) if isinstance(x, str) else x)  # Remove '''''
    df[col] = df[col].apply(lambda x: pattern3.sub('', x) if isinstance(x, str) else x)  # Remove : followed by spaces
    df[col] = df[col].apply(lambda x: pattern4.sub('', x) if isinstance(x, str) else x)  # Remove * followed by space
    df[col] = df[col].apply(lambda x: pattern5.sub('', x) if isinstance(x, str) else x)  # Remove non-ASCII characters

# Print the cleaned DataFrame
print("Cleaned DataFrame:")
print(df)

# Save the cleaned DataFrame back to a CSV file
df.to_csv('smaller_dataset.csv', index=False)

print("Cleaned DataFrame saved to 'smaller_dataset.csv'")
