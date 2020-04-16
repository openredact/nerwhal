from pii_identifier.recognizers import SpacyStatisticalRecognizer

# TODO would it be a good idea to share the test cases for both statistical recognizer, using pytest parameterization?
# instead of requiring the models to work on one sentence, they should be tested on several and be required
# to score higher than a threshold (could be different for each model <- parameterization)


def test_simple_persons(set_up_backend):
    recognizer = SpacyStatisticalRecognizer()
    backend = set_up_backend(recognizer)
    piis = backend.run("Mein Lehrmeister war Yoda.")
    assert len(piis) == 1
    assert piis[0].type == "PER"
    assert piis[0].text == "Yoda"
