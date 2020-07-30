from dataclasses import dataclass, field
from typing import List, Optional
import pydantic


@dataclass
class NamedEntity:
    start_char: int
    end_char: int
    tag: str
    text: str = None
    score: float = None
    recognizer: str = None
    start_tok: int = None
    end_tok: int = None


@pydantic.dataclasses.dataclass
class Config:
    language: str
    recognizer_paths: Optional[List[str]] = field(default_factory=list)
    use_statistical_ner: Optional[bool] = False
    load_example_recognizers: Optional[bool] = False
    context_word_confidence_boost_factor: Optional[int] = 1.2
