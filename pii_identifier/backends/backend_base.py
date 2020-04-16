from abc import ABC, abstractmethod


class NlpBackend(ABC):
    """
    Backend == pipeline + model
    """

    @abstractmethod
    def register_recognizer(self, recognizer):
        """
        This accumulates recognizers. They cannot be removed anymore. To remove them create a new instance.
        :param recognizer:
        :return:
        """
        pass

    @abstractmethod
    def run(self, text):
        pass
