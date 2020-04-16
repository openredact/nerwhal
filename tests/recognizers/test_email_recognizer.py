from pii_identifier.recognizers import EmailRecognizer


def test_simple_email(set_up_backend):
    recognizer = EmailRecognizer()
    backend = set_up_backend(recognizer)
    piis = backend.run("Meine E-Mail Adresse ist obiwan@gmail.com")
    assert len(piis) == 1
    assert piis[0].type == "EMAIL"
    assert piis[0].text == "obiwan@gmail.com"
