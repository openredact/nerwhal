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


@dataclass
class Token:
    """
    Fields:
        has_ws: whether or not the token is followed by whitespace (useful when reconstructing the text from tokens)
        br_count: some tokens represented breaks/newlines (e.g. "\n\n"), break count specifies how many breaks there are;
            defaults to 0 for all other tokens
    """

    text: str
    has_ws: bool
    br_count: int
    start_char: int
    end_char: int


@pydantic.dataclasses.dataclass
class Config:
    """The main config object.

    Fields:
        language: the language of the text; used for tokenization and statistical NER
        recognizer_paths: a list of paths that specify the (custom) recognizers to be used for recognition (optional)
        use_statistical_ner: whether to use statistical NER or not (optional)
        load_integrated_recognizers: whether to use all integrated recognizers for recognition (optional)
        context_word_confidence_boost_factor: the factor by which the score of named entities gets increased, if one of the
            context words is nearby (optional)
    """

    language: str
    recognizer_paths: Optional[List[str]] = field(default_factory=list)
    use_statistical_ner: Optional[bool] = False
    load_integrated_recognizers: Optional[bool] = False
    context_word_confidence_boost_factor: Optional[float] = 1.2
