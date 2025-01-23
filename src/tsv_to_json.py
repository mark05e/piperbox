import csv
import json

def tsv_to_json(tsv_file, json_file):
  """
  Converts a TSV file to a JSON file with static headers: 'language', 'filename', 'prompt_text'.

  Args:
    tsv_file: Path to the input TSV file.
    json_file: Path to the output JSON file.
  """
  data = []
  with open(tsv_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    headers = next(reader)  # Read the header row 
    for row in reader:
      entry = {
          'language': row[0], 
          'output_file': row[1], 
          'text': row[2]
      }
      data.append(entry)

  with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

if __name__ == "__main__":
  tsv_to_json('input.tsv', 'output.json')