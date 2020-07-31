from nerwhal import Config
import json


def test_minimal_config_from_json():
    config_json = """
    {
        "language": "de"
    }
    """
    config_dict = json.loads(config_json)
    config = Config(**config_dict)
    assert config.language == "de"
    assert config.recognizer_paths == []


def test_full_config_from_json():
    config_json = """
    {
        "language": "de",
        "recognizer_paths": ["foo/bar.py"],
        "use_statistical_ner": true,
        "load_example_recognizers": false
    }
    """
    config_dict = json.loads(config_json)
    config = Config(**config_dict)
    assert config.language == "de"
    assert config.recognizer_paths == ["foo/bar.py"]
    assert config.use_statistical_ner
    assert not config.load_example_recognizers
