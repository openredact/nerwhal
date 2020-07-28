from dataclasses import dataclass
from typing import List


@dataclass
class NamedEntity:
    start_char: int
    end_char: int
    tag: str
    text: str = None
    score: float = None
    model: str = None
    start_tok: int = None
    end_tok: int = None


@dataclass
class Config:
    model_name: str
    recognizer_paths: List[str]
    load_examples: bool = False
