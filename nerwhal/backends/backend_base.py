from abc import ABC, abstractmethod


class NlpBackend(ABC):
    """NlpBackend are the engines behind the recognizers that drive the search for PIIs.

    Recognizers use the functionality provided by a backend to do their job. Each recognizer has to specify one backend
    that it operates on.
    """

    @abstractmethod
    def register_recognizer(self, recognizer):
        """Add the given recognizer to this backend instance.

        One backend can have several recognizers. Once added they cannot be removed anymore.
        To remove them create a new backend instance.
        """
        pass

    @abstractmethod
    def run(self, text):
        """Run the backend and all registered recognizers.

        :return: the list of PIIs that have been identified
        """
        pass
