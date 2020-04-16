from pii_identifier.recognizers._re_recognizer_base import ReRecognizer


class EmailRecognizer(ReRecognizer):
    # TODO WIP
    @property
    def regexp(self):
        return r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)"

    @property
    def entity(self):
        return "EMAIL"

    @property
    def precision(self):
        return 0.9
