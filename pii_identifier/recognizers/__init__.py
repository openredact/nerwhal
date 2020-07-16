from .de_country_recognizer import DeCountryRecognizer
from .de_phone_number_recognizer import DePhoneNumberRecognizer
from .email_recognizer import EmailRecognizer
from .flair_statistical_recognizer import FlairStatisticalRecognizer
from .spacy_statistical_recognizer import SpacyStatisticalRecognizer

_recognizer_classes = (
    DePhoneNumberRecognizer,
    DeCountryRecognizer,
    EmailRecognizer,
    FlairStatisticalRecognizer,
    SpacyStatisticalRecognizer,
)
__all__ = [recognizer.__name__ for recognizer in _recognizer_classes]
__tags__ = set([tag for recognizer in _recognizer_classes for tag in recognizer.TAGS])
