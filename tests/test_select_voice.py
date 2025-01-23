# tests/test_select_voice.py

import pytest
import json
import os
from src.select_voice import prioritize_languages
from src.select_voice import save_config

# prioritize_languages

def test_priority_languages_first():
    voices = [
        {'language_code': 'en_US'},
        {'language_code': 'de_DE'},
        {'language_code': 'es_ES'},
        {'language_code': 'fr_FR'},
        {'language_code': 'it_IT'}
    ]
    expected_result = [
        {'language_code': 'en_US'},
        {'language_code': 'es_ES'},
        {'language_code': 'fr_FR'},
        {'language_code': 'de_DE'},
        {'language_code': 'it_IT'}
    ]
    prioritize_languages(voices)
    assert voices == expected_result

def test_no_priority_languages():
    voices = [
        {'language_code': 'de_DE'},
        {'language_code': 'it_IT'},
        {'language_code': 'pt_PT'}
    ]
    expected_result = [
        {'language_code': 'de_DE'},
        {'language_code': 'it_IT'},
        {'language_code': 'pt_PT'}
    ]
    prioritize_languages(voices)
    assert voices == expected_result

def test_empty_list():
    voices = []
    prioritize_languages(voices)
    assert voices == []

def test_none_input():
    voices = None
    with pytest.raises(ValueError):
        prioritize_languages(voices)


# save_config

def test_save_config_new_file():
    voices = [
        {'language_code': 'en', 'models': [{'model_name': 'model1'}]}
    ]
    language_index = 0
    model_index = 0
    file_path = 'test_config.json'

    save_config(voices, language_index, model_index, file_path)

    with open(file_path, 'r', encoding='utf-8') as file:
        config = json.load(file)

    assert config == {'voice_config': {'en': {'model_name': 'model1'}}}

    os.remove(file_path)

def test_save_config_existing_file():
    voices = [
        {'language_code': 'en', 'models': [{'model_name': 'model1'}]},
        {'language_code': 'es', 'models': [{'model_name': 'model2'}]}
    ]
    language_index = 0
    model_index = 0
    file_path = 'test_config.json'

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump({'voice_config': {'es': {'model_name': 'model2'}}}, file)

    save_config(voices, language_index, model_index, file_path)

    with open(file_path, 'r', encoding='utf-8') as file:
        config = json.load(file)

    assert config == {'voice_config': {'es': {'model_name': 'model2'}, 'en': {'model_name': 'model1'}}}

    os.remove(file_path)

def test_save_config_none_input():
    voices = None
    language_index = 0
    model_index = 0
    file_path = 'test_config.json'

    with pytest.raises(TypeError):
        save_config(voices, language_index, model_index, file_path)

def test_save_config_invalid_file_path():
    voices = [
        {'language_code': 'en', 'models': [{'model_name': 'model1'}]}
    ]
    language_index = 0
    model_index = 0
    file_path = '/invalid/path/test_config.json'

    with pytest.raises(FileNotFoundError):
        save_config(voices, language_index, model_index, file_path)