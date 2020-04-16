from pii_identifier.recognizers import PhoneNumberRecognizer


def test_international_din_5008(set_up_backend):
    recognizer = PhoneNumberRecognizer()
    backend = set_up_backend(recognizer)
    piis = backend.run("Das ist eine Telefonnummer: +49 (30) 123456")
    assert len(piis) == 1
    assert piis[0].type == "PHONE"
    assert piis[0].text == "+49 (30) 123456"
