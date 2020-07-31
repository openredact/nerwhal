import pytest

from nerwhal.integrated_recognizers.email_recognizer import EmailRecognizer


@pytest.fixture
def backend(setup_backend):
    recognizer = EmailRecognizer
    backend = setup_backend(recognizer.BACKEND)
    backend.register_recognizer(recognizer)
    return backend


def test_simple_email(backend, embed):
    text = "Meine E-Mail Adresse ist obiwan@gmail.com."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine E-Mail Adresse ist EMAIL."


def test_dotted_email(backend, embed):
    text = "Meine E-Mail Adresse ist han.solo@example.com."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine E-Mail Adresse ist EMAIL."


def test_disposable_style_with_plus(backend, embed):
    text = "Meine E-Mail Adresse ist disposable.style.with+symbol@example.com und user.name+tag+sorting@example.com."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine E-Mail Adresse ist EMAIL und EMAIL."


def test_with_hyphen(backend, embed):
    text = "Meine E-Mail Adresse ist mail-with-hyphen@example.com."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine E-Mail Adresse ist EMAIL."


def test_one_letter_local_part(backend, embed):
    text = "Meine E-Mail Adresse ist x@example.com."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine E-Mail Adresse ist EMAIL."


def test_special_chars_in_local_part(backend, embed):
    text = "Meine E-Mail Adresse ist mailhost!user%example.com@example.org."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine E-Mail Adresse ist EMAIL."


def test_host_with_hyphen(backend, embed):
    text = "Meine E-Mail Adresse ist test@my-host.com."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine E-Mail Adresse ist EMAIL."


def test_one_letter_host(backend, embed):
    text = "Meine E-Mail Adresse ist test@x.com."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine E-Mail Adresse ist EMAIL."


def test_host_with_many_labels(backend, embed):
    text = "Meine E-Mail Adresse ist test@de.example.uk."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine E-Mail Adresse ist EMAIL."


def test_host_with_special_tld(backend, embed):
    text = "Meine E-Mail Adresse ist test@example.foundation."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine E-Mail Adresse ist EMAIL."


def test_no_at_character(backend, embed):
    text = "Meine E-Mail Adresse ist test.example.com."
    ents = backend.run(text)
    assert len(ents) == 0


def test_cannot_start_with_dot(backend, embed):
    text = "...mail@example.com..."
    ents = backend.run(text)
    assert embed(text, ents) == "...EMAIL..."
