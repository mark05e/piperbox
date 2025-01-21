import re
import json
import urllib.request

def download_markdown_content(url):
    metadata_folder = 'metadata'
    metadata_file = 'VOICES.md'
    metadata_path = f'{metadata_folder}/{metadata_file}'

    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
            print("Markdown content loaded from local file.")
            return markdown_content
    except FileNotFoundError:
        try:
            import os
            if not os.path.exists(metadata_folder):
                os.makedirs(metadata_folder)
            with urllib.request.urlopen(url) as f:
                markdown_content = f.read().decode('utf-8')
                with open(metadata_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(markdown_content)
                print("Markdown content downloaded and saved to local file.")
                return markdown_content
        except Exception as e:
            print("Error downloading markdown content:", str(e))
            exit(1)

def extract_language_codes(markdown_content):
    language_codes = {}
    for match in re.finditer(r'^\* ([^ ]+) \(([^)]+)\)', markdown_content, re.MULTILINE):
        # print("Language match found:", match.group(0))
        language_code_match = re.search(r'`([^`]+)`', match.group(2))
        if language_code_match:
            language_code = language_code_match.group(1)
        else:
            language_code = match.group(2).strip()
        language_name = match.group(1)
        language_codes[language_code] = {"language_name": language_name, "models": []}
        # print("Language code:", language_code)
        # print("Language name:", language_name)
    return language_codes

def extract_model_matches(markdown_content, language_codes):
    model_matches_found = False
    for match in re.finditer(r'^\* ([^ ]+) \(([^)]+)\)', markdown_content, re.MULTILINE):
        language_code_match = re.search(r'`([^`]+)`', match.group(2))
        if language_code_match:
            language_code = language_code_match.group(1)
        else:
            language_code = match.group(2).strip()
        language_section = markdown_content[match.end():]
        next_language_match = re.search(r'^\* ([^ ]+) \(([^)]+)\)', language_section, re.MULTILINE | re.DOTALL)
        if next_language_match:
            language_section = language_section[:next_language_match.start()]
        model_matches = re.findall(r'\* (.+) - \[\[model\]\(([^)]+)\)\] \[\[config\]\(([^)]+)\)\]', language_section)
        for model_match in model_matches:
            model_url = model_match[1]
            model_name = model_url.split("/")[-1].split("?")[0].split(".")[0]
            model_config_url = model_match[2]
            language_codes[language_code]["models"].append({
                "model_name": model_name,
                "model_url": model_url,
                "model_config_url": model_config_url
            })
            model_matches_found = True
    if not model_matches_found:
        print("No model matches found in markdown content.")
    return language_codes

def convert_to_json(language_codes):
    json_data = []
    for language_code, language_info in language_codes.items():
        # print("Language code:", language_code)
        # print("Language info:", language_info)
        json_data.append({
            "language_code": language_code,
            "language_name": language_info["language_name"],
            "models": language_info["models"]
        })
    # print("JSON data:")
    # print(json.dumps(json_data, indent=4, ensure_ascii=False))
    return json_data

def main():
    url = "https://raw.githubusercontent.com/rhasspy/piper/refs/heads/master/VOICES.md"
    markdown_content = download_markdown_content(url)
    language_codes = extract_language_codes(markdown_content)
    language_codes = extract_model_matches(markdown_content, language_codes)
    json_data = convert_to_json(language_codes)
    
    # Write JSON data to local file
    metadata_folder = 'metadata'
    import os
    if not os.path.exists(metadata_folder):
        os.makedirs(metadata_folder)
    with open(f'{metadata_folder}/voices.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()