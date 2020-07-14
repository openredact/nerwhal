from .de_phone_number_recognizer import DePhoneNumberRecognizer
from .de_state_recognizer import DeStateRecognizer
from .email_recognizer import EmailRecognizer
from .flair_statistical_recognizer import FlairStatisticalRecognizer
from .spacy_statistical_recognizer import SpacyStatisticalRecognizer

_recognizer_classes = (
    DePhoneNumberRecognizer,
    DeStateRecognizer,
    EmailRecognizer,
    FlairStatisticalRecognizer,
    SpacyStatisticalRecognizer,
)
__all__ = [recognizer.__name__ for recognizer in _recognizer_classes]
