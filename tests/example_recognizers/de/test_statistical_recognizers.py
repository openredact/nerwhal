def test_simple_person(setup_backend, embed, stat_recognizer):
    backend = setup_backend(stat_recognizer)
    text = "Mein Lehrmeister war Yoda."
    ents = backend.run(text)
    assert embed(text, ents) == "Mein Lehrmeister war PER."


def test_simple_location(setup_backend, embed, stat_recognizer):
    backend = setup_backend(stat_recognizer)
    text = "Die Jedis kennen das schöne Deutschland nicht."
    ents = backend.run(text)
    assert embed(text, ents) == "Die Jedis kennen das schöne LOC nicht."


def test_simple_organization(setup_backend, embed, stat_recognizer):
    backend = setup_backend(stat_recognizer)
    text = "Die Firma Sienar-Flottensysteme denkt über einen neuen Todesstern nach."
    ents = backend.run(text)
    assert embed(text, ents) == "Die Firma ORG denkt über einen neuen Todesstern nach."


def test_simple_misc(setup_backend, embed, stat_recognizer):
    backend = setup_backend(stat_recognizer)
    text = "Diese Beispiele sind auf Deutsch."
    ents = backend.run(text)
    assert embed(text, ents) == "Diese Beispiele sind auf MISC."
