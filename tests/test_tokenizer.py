from nerwhal.utils import _tokenize


def test_tokenize_line_breaks():
    # one single line break
    text = "Han Solo und Wookiee Chewbacca wurden Freunde.\nHan's E-Mail ist han.solo@imperium.com."
    tokens = _tokenize(text)

    print(f"Tokens: {tokens}")

    assert 1 == len([t for t in tokens if t["has_br"]])

    # one double line break
    text = "Han Solo und Wookiee Chewbacca wurden Freunde.\n\nHan's E-Mail ist han.solo@imperium.com."
    tokens = _tokenize(text)

    print(f"Tokens: {tokens}")

    assert 1 == len([t for t in tokens if t["has_br"]])

    # two single line breaks
    text = "Hi there!\nHan Solo und Wookiee Chewbacca wurden Freunde.\n\nHan's E-Mail ist han.solo@imperium.com."
    tokens = _tokenize(text)

    print(f"Tokens: {tokens}")

    assert 2 == len([t for t in tokens if t["has_br"]])
