import pytest

from nerwhal.example_recognizers.phone_number_recognizer import PhoneNumberRecognizer


@pytest.fixture(scope="module")
def backend(setup_backend):
    recognizer = PhoneNumberRecognizer
    backend = setup_backend(recognizer.BACKEND)
    backend.register_recognizer(recognizer)
    return backend


# DIN 5008


def test_international_din_5008(backend, embed):
    text = "Meine Telefonnummer ist +49 30 12345-67."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine Telefonnummer ist PHONE."


def test_national_din_5008(backend, embed):
    text = "Meine Telefonnummer ist 01234 5678."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine Telefonnummer ist PHONE."


def test_national_din_5008_hyphenated_extension(backend, embed):
    text = "Meine Telefonnummer ist 030 12345-67."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine Telefonnummer ist PHONE."


def test_national_din_5008_value_added_service_with_code(backend, embed):
    text = "Meine Telefonnummer ist 0900 5 123456."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine Telefonnummer ist PHONE."


# Microsoft's canonical format


def test_microsofts_canonical_format(backend, embed):
    text = "Meine Telefonnummer ist +49 (30) 123456."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine Telefonnummer ist PHONE."


def test_microsofts_canonical_format_with_extension(backend, embed):
    text = "Meine Telefonnummer ist +49 (30) 12345 - 67."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine Telefonnummer ist PHONE."


def test_microsofts_canonical_format_with_extension_no_space(backend, embed):
    text = "Meine Telefonnummer ist +49 (30) 123456-78."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine Telefonnummer ist PHONE."


# E.123


def test_international_e_123(backend, embed):
    text = "Meine Telefonnummer ist +49 89 123 456 78."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine Telefonnummer ist PHONE."


def test_international_e_123_company_center(backend, embed):
    text = "Meine Telefonnummer ist +49 89 123 456 0."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine Telefonnummer ist PHONE."


def test_national_e_123(backend, embed):
    text = "Meine Telefonnummer ist (042) 123 4567."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine Telefonnummer ist PHONE."


def test_national_e_123_with_options(backend, embed):
    text = "Meine Telefonnummer ist (030) 12345 0 / 67."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine Telefonnummer ist PHONE."


# Others


def test_mobile_number(backend, embed):
    text = "Meine Telefonnummer ist 0160 1234567."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine Telefonnummer ist PHONE."


def test_freephone(backend, embed):
    text = "Meine Telefonnummer ist 0800 123456."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine Telefonnummer ist PHONE."


def test_freephone_without_zero(backend, embed):
    text = "Meine Telefonnummer ist 800 123456."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine Telefonnummer ist PHONE."


# Non-standard


def test_double_zero_international(backend, embed):
    text = "Meine Telefonnummer ist 0049 1234 56789."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine Telefonnummer ist PHONE."


def test_number_abbreviated(backend, embed):
    text = "Sie können uns erreichen unter tel.:+49-30-1234567."
    ents = backend.run(text)
    assert embed(text, ents) == "Sie können uns erreichen unter tel.:PHONE."


def test_dotted_format(backend, embed):
    text = "Meine Telefonnummer ist +49.3012345."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine Telefonnummer ist PHONE."


def test_national_not_standardized(backend, embed):
    text = "Meine Telefonnummer ist 0 30 / 12 34 56."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine Telefonnummer ist PHONE."


def test_international_not_standardized_optional_zero(backend, embed):
    text = "Meine Telefonnummer ist +49 (0) 30 12345-67."
    ents = backend.run(text)
    assert embed(text, ents) == "Meine Telefonnummer ist PHONE."


# US style


def test_local(backend, embed):
    text = "My number is 234-1234."
    ents = backend.run(text)
    assert embed(text, ents) == "My number is PHONE."


def test_domestic(backend, embed):
    text = "My number is (543) 234-1234."
    ents = backend.run(text)
    assert embed(text, ents) == "My number is PHONE."


def test_international_from_us(backend, embed):
    text = "My number is +1-543-234-1234."
    ents = backend.run(text)
    assert embed(text, ents) == "My number is PHONE."


def test_international_from_abroad(backend, embed):
    text = "My number is 001-543-234-1234."
    ents = backend.run(text)
    assert embed(text, ents) == "My number is PHONE."


# Not phone numbers


def test_credit_card(backend):
    # The matcher pattern that matches most tokens takes priority. So a credit card matcher will take priority over
    # two number matches in 1234 1234 1234 1234
    text = "Meine Kreditkarten-Nummer ist 1234123412341234, anders geschrieben 1234 1234 1234 1234."
    ents = backend.run(text)
    assert len(ents) == 0


def test_date(backend):
    text = "Heute ist der 12.12.2012."
    ents = backend.run(text)
    assert len(ents) == 0


def test_us_date(backend):
    text = "Today is the 01/02/2000."
    ents = backend.run(text)
    assert len(ents) == 0
