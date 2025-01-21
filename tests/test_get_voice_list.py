# tests/test_get_voice_list.py
import pytest
from src.get_voice_list import extract_language_codes
import re

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