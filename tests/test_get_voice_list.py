# tests/test_get_voice_list.py
import pytest
from src.get_voice_list import extract_language_codes
from src.get_voice_list import extract_model_matches
from src.get_voice_list import convert_to_json

# extract_language_codes

def test_extract_language_codes_empty_markdown():
    markdown_content = ""
    language_codes = extract_language_codes(markdown_content)
    assert language_codes == {}

def test_extract_language_codes_single_language():
    markdown_content = "* English (`en_US`)\n"
    language_codes = extract_language_codes(markdown_content)
    assert language_codes == {
        "en_US": {"language_name": "English", "models": []}
    }

def test_extract_language_codes_multiple_languages():
    markdown_content = "* English (`en_US`)\n* Spanish (`es_ES`)\n"
    language_codes = extract_language_codes(markdown_content)
    assert language_codes == {
        "en_US": {"language_name": "English", "models": []},
        "es_ES": {"language_name": "Spanish", "models": []}
    }

def test_extract_language_codes_language_code_without_backticks():
    markdown_content = "* English (en_US)\n"
    language_codes = extract_language_codes(markdown_content)
    assert language_codes == {
        "en_US": {"language_name": "English", "models": []}
    }

def test_extract_language_codes_invalid_markdown():
    markdown_content = "Invalid markdown content"
    language_codes = extract_language_codes(markdown_content)
    assert language_codes == {}

# extract_model_matches

def test_extract_model_matches_empty_markdown():
    markdown_content = ""
    language_codes = {}
    updated_language_codes = extract_model_matches(markdown_content, language_codes)
    assert updated_language_codes == {}

def test_extract_model_matches_no_model_matches():
    markdown_content = "* English (`en_US`)\n"
    language_codes = {"en_US": {"language_name": "English", "models": []}}
    updated_language_codes = extract_model_matches(markdown_content, language_codes)
    assert updated_language_codes == language_codes

def test_extract_model_matches_single_model_match():
    markdown_content = "* English (`en_US`)\n* Model 1 - [[model](https://example.com/model1.onnx)] [[config](https://example.com/model1.json)]\n"
    language_codes = {"en_US": {"language_name": "English", "models": []}}
    updated_language_codes = extract_model_matches(markdown_content, language_codes)
    assert len(updated_language_codes["en_US"]["models"]) == 1
    assert updated_language_codes["en_US"]["models"][0]["model_name"] == "model1"
    assert updated_language_codes["en_US"]["models"][0]["model_url"] == "https://example.com/model1.onnx"
    assert updated_language_codes["en_US"]["models"][0]["model_config_url"] == "https://example.com/model1.json"

def test_extract_model_matches_multiple_model_matches():
    markdown_content = "* English (`en_US`)\n* Model 1 - [[model](https://example.com/model1.onnx)] [[config](https://example.com/model1.json)]\n* Model 2 - [[model](https://example.com/model2.onnx)] [[config](https://example.com/model2.json)]\n"
    language_codes = {"en_US": {"language_name": "English", "models": []}}
    updated_language_codes = extract_model_matches(markdown_content, language_codes)
    assert len(updated_language_codes["en_US"]["models"]) == 2
    assert updated_language_codes["en_US"]["models"][0]["model_name"] == "model1"
    assert updated_language_codes["en_US"]["models"][0]["model_url"] == "https://example.com/model1.onnx"
    assert updated_language_codes["en_US"]["models"][0]["model_config_url"] == "https://example.com/model1.json"
    assert updated_language_codes["en_US"]["models"][1]["model_name"] == "model2"
    assert updated_language_codes["en_US"]["models"][1]["model_url"] == "https://example.com/model2.onnx"
    assert updated_language_codes["en_US"]["models"][1]["model_config_url"] == "https://example.com/model2.json"

def test_extract_model_matches_multiple_languages():
    markdown_content = "* English (`en_US`)\n* Model 1 - [[model](https://example.com/model1.onnx)] [[config](https://example.com/model1.json)]\n* Spanish (`es_ES`)\n* Model 2 - [[model](https://example.com/model2.onnx)] [[config](https://example.com/model2.json)]\n"
    language_codes = {"en_US": {"language_name": "English", "models": []}, "es_ES": {"language_name": "Spanish", "models": []}}
    updated_language_codes = extract_model_matches(markdown_content, language_codes)
    assert len(updated_language_codes["en_US"]["models"]) == 1
    assert updated_language_codes["en_US"]["models"][0]["model_name"] == "model1"
    assert updated_language_codes["en_US"]["models"][0]["model_url"] == "https://example.com/model1.onnx"
    assert updated_language_codes["en_US"]["models"][0]["model_config_url"] == "https://example.com/model1.json"
    assert len(updated_language_codes["es_ES"]["models"]) == 1
    assert updated_language_codes["es_ES"]["models"][0]["model_name"] == "model2"
    assert updated_language_codes["es_ES"]["models"][0]["model_url"] == "https://example.com/model2.onnx"
    assert updated_language_codes["es_ES"]["models"][0]["model_config_url"] == "https://example.com/model2.json"

# convert_to_json

def test_convert_to_json_empty_language_codes():
    language_codes = {}
    json_data = convert_to_json(language_codes)
    assert json_data == []

def test_convert_to_json_single_language_code():
    language_codes = {
        "en_US": {
            "language_name": "English",
            "models": [
                {"model_name": "model1", "model_url": "https://example.com/model1.onnx", "model_config_url": "https://example.com/model1.json"}
            ]
        }
    }
    json_data = convert_to_json(language_codes)
    assert len(json_data) == 1
    assert json_data[0]["language_code"] == "en_US"
    assert json_data[0]["language_name"] == "English"
    assert len(json_data[0]["models"]) == 1
    assert json_data[0]["models"][0]["model_name"] == "model1"
    assert json_data[0]["models"][0]["model_url"] == "https://example.com/model1.onnx"
    assert json_data[0]["models"][0]["model_config_url"] == "https://example.com/model1.json"

def test_convert_to_json_multiple_language_codes():
    language_codes = {
        "en_US": {
            "language_name": "English",
            "models": [
                {"model_name": "model1", "model_url": "https://example.com/model1.onnx", "model_config_url": "https://example.com/model1.json"}
            ]
        },
        "es_ES": {
            "language_name": "Spanish",
            "models": [
                {"model_name": "model2", "model_url": "https://example.com/model2.onnx", "model_config_url": "https://example.com/model2.json"}
            ]
        }
    }
    json_data = convert_to_json(language_codes)
    assert len(json_data) == 2
    assert json_data[0]["language_code"] == "en_US"
    assert json_data[0]["language_name"] == "English"
    assert len(json_data[0]["models"]) == 1
    assert json_data[0]["models"][0]["model_name"] == "model1"
    assert json_data[0]["models"][0]["model_url"] == "https://example.com/model1.onnx"
    assert json_data[0]["models"][0]["model_config_url"] == "https://example.com/model1.json"
    assert json_data[1]["language_code"] == "es_ES"
    assert json_data[1]["language_name"] == "Spanish"
    assert len(json_data[1]["models"]) == 1
    assert json_data[1]["models"][0]["model_name"] == "model2"
    assert json_data[1]["models"][0]["model_url"] == "https://example.com/model2.onnx"
    assert json_data[1]["models"][0]["model_config_url"] == "https://example.com/model2.json"