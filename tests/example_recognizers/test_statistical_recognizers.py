def test_simple_person(set_up_backend, embed, stat_recognizer):
    backend = set_up_backend(stat_recognizer)
    text = "Mein Lehrmeister war Yoda."
    piis = backend.run(text)
    assert embed(text, piis) == "Mein Lehrmeister war PER."


def test_simple_location(set_up_backend, embed, stat_recognizer):
    backend = set_up_backend(stat_recognizer)
    text = "Die Jedis kennen das schöne Deutschland nicht."
    piis = backend.run(text)
    assert embed(text, piis) == "Die Jedis kennen das schöne LOC nicht."


def test_simple_organization(set_up_backend, embed, stat_recognizer):
    backend = set_up_backend(stat_recognizer)
    text = "Die Firma Sienar-Flottensysteme denkt über einen neuen Todesstern nach."
    piis = backend.run(text)
    assert embed(text, piis) == "Die Firma ORG denkt über einen neuen Todesstern nach."


def test_simple_misc(set_up_backend, embed, stat_recognizer):
    backend = set_up_backend(stat_recognizer)
    text = "Diese Beispiele sind auf Deutsch."
    piis = backend.run(text)
    assert embed(text, piis) == "Diese Beispiele sind auf MISC."
