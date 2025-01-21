import json
import os
import urllib.request

def load_voices_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_config_json(file_path, config):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4)

def download_file(url, file_path):
    urllib.request.urlretrieve(url, file_path)

def display_languages(voices):
    print("Select a language:")
    for i, voice in enumerate(voices):
        print(f"{i+1}. {voice['language_name']} ({voice['language_code']})")

def get_language_choice(voices):
    while True:
        try:
            language_index = int(input("Enter the number of your chosen language: ")) - 1
            if 0 <= language_index < len(voices):
                return language_index
            else:
                print("Invalid choice. Please enter a number between 1 and", len(voices))
        except ValueError:
            print("Invalid input. Please enter a number.")

def prioritize_languages(voices):
    priority_languages = ['en', 'es', 'fr']
    priority_voices = [voice for voice in voices if any(voice['language_code'].lower().startswith(lang + '_') for lang in priority_languages)]
    other_voices = [voice for voice in voices if not any(voice['language_code'].lower().startswith(lang + '_') for lang in priority_languages)]

    voices.clear()
    voices.extend(priority_voices)
    voices.extend(other_voices)

def display_models(voices, language_index):
    print("\nSelect a model:")
    for i, model in enumerate(voices[language_index]['models']):
        print(f"{i+1}. {model['model_name']}")

def get_model_choice(voices, language_index):
    while True:
        try:
            model_index = int(input("Enter the number of your chosen model: ")) - 1
            if 0 <= model_index < len(voices[language_index]['models']):
                return model_index
            else:
                print("Invalid choice. Please enter a number between 1 and", len(voices[language_index]['models']))
        except ValueError:
            print("Invalid input. Please enter a number.")

def create_config(voices, language_index, model_index):
    language_code = voices[language_index]['language_code']
    # language_name = voices[language_index]['language_name']
    model_name = voices[language_index]['models'][model_index]['model_name']
    # model_url = voices[language_index]['models'][model_index]['model_url']
    # config_url = voices[language_index]['models'][model_index]['model_config_url']

    config = {
        'voice_config': {
            language_code: {
                'model_name': model_name
            }
        }
    }

    return config

def download_model_and_config(voices, language_index, model_index):
    language_code = voices[language_index]['language_code']
    model_name = voices[language_index]['models'][model_index]['model_name']
    model_url = voices[language_index]['models'][model_index]['model_url']
    config_url = voices[language_index]['models'][model_index]['model_config_url']

    model_path = f'voicemodels/{language_code}/{model_name}.onnx'
    config_path = f'voicemodels/{language_code}/{model_name}.json'

    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    if not os.path.exists(model_path):
        print(f"Downloading model {model_name}...")
        download_file(model_url, model_path)
    else:
        print(f"Model {model_name} already exists, skipping download.")

    if not os.path.exists(config_path):
        print(f"Downloading config {model_name}...")
        download_file(config_url, config_path)
    else:
        print(f"Config {model_name} already exists, skipping download.")

def main():
    voices_json_path = 'metadata/voices.json'
    config_json_path = 'metadata/config.json'
    voices = load_voices_json(voices_json_path)

    prioritize_languages(voices)
    display_languages(voices)
    language_index = get_language_choice(voices)

    display_models(voices, language_index)
    model_index = get_model_choice(voices, language_index)

    config = create_config(voices, language_index, model_index)
    save_config_json(config_json_path, config)

    download_model_and_config(voices, language_index, model_index)

    print("\nConfig setup successfully!")

if __name__ == "__main__":
    main()